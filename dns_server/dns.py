#!/usr/bin/env python3

import re
import time
import socket
from math import floor
from datetime import timedelta

import log21
from dnslib import RR, PTR, QTYPE, A, DNSRecord, DNSQuestion
from dnslib.server import DNSServer, DNSHandler, BaseResolver

# Proxied domains - will be processed and added to OVERRIDE
PROXIED_DOMAINS = {
    (
        # This will be expanded to "*.ytimg.com" and "ytimg.com"
        r"ytimg\.com",
        r"googlevideo\.com",
        r"youtube\.com",
        r"gstatic\.com",
        r"googleusercontent\.com",
    ): A("186.206.229.109")
}

# Override domains
OVERRIDE: dict = {
    QTYPE.A: {
        re.compile(r"^.*\.localhost$"): A("127.0.0.1"),
        re.compile(r"^codewriter21\.local$"): A("127.0.0.1"),
    },
    QTYPE.PTR: {
        re.compile(r"1\.0\.0\.127\.in-addr\.arpa"): PTR("CodeWriter21.DNS.local")
    },
}

# Process PROXIED_DOMAINS values and add them to OVERRIDE
for domains, rdata in PROXIED_DOMAINS.items():
    proxied_pattern = "^"
    for domain in domains:
        proxied_pattern += f"({domain})|(.*\\.{domain})|"
    proxied_pattern = proxied_pattern.rstrip("|") + "$"
    OVERRIDE[QTYPE.A][re.compile(proxied_pattern)] = rdata

# Upstream DNS Hosts
UPSTREAM_HOSTS = [
    "8.8.8.8",  # Google
    "1.1.1.1",  # Cloudflare
    "193.186.32.32",  # Bertina - ir.bertinadns.com
    "194.225.152.10",  # IPM - ns1.iranet.ir
    "217.218.127.127",  # TIC
    "78.157.42.100",  # Electro - dns.electro
    "178.22.122.101",  # Shecan
    "185.51.200.1",  # Shecan - 185.51.200.1.shahrad.net
    "87.107.110.109",  # DNS Pro
    "5.202.100.100",  # Pishgaman - dns.pishgaman.net
    "5.202.100.101",  # Pishgaman
    "10.112.129.6",
]
UPSTREAM_REQUEST_TIMEOUT = 2


class UpstreamIndexNotFoundError(IndexError): ...


def ttl_gen(delta: timedelta) -> int:
    return floor(time.time() / delta.total_seconds())


class CustomResolver(BaseResolver):
    def __init__(self):
        super().__init__()
        self._upstream_cache = {}

    def call_upstream(self, request: DNSRecord, index: int = 0) -> DNSRecord:
        """Request DNS Record from an upstream DNS server.

        Will return cached values when available.

        :param request: The DNS Record
        :param index: The index of desired upstream server in UPSTREAM_HOSTS array
        :returns: The response from upstream or cache as
        :raises UpstreamIndexNotFoundError: This is raised when the input index is out
            of range
        """
        req = bytes(request.pack())

        # Invalidate the whole cache every 30 minutes
        ttl = ttl_gen(timedelta(minutes=30))
        if (cache := self._upstream_cache.get(ttl, None)) is None:
            log21.debug("Clearing upstream cache...")
            self._upstream_cache = {ttl: {}}
            cache = self._upstream_cache[ttl]

        # Try to get the query results from the cache
        if data := cache.get((req, index)):
            return data

        # Send the request to the upstream server
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(UPSTREAM_REQUEST_TIMEOUT)
            # Raw DNS request
            sock.sendto(req, (UPSTREAM_HOSTS[index], 53))
            data, _ = sock.recvfrom(4096)
            sock.close()
            if data:
                cache[(req, index)] = data
                return DNSRecord.parse(data)
            raise ValueError("No data was recieved from the upstream.")
        except Exception as e:
            log21.error(
                "Failed to retrieve IP from upstream server[%d]: %s, %s",
                args=(index, e.__class__.__name__, e),
            )
            index += 1
            if index >= len(UPSTREAM_HOSTS):
                raise UpstreamIndexNotFoundError("Upstream index out of range.")
            return self.call_upstream(request, index)

    def resolve(self, request: DNSRecord, handler: DNSHandler):
        question: DNSQuestion = request.q
        domain = str(question.qname).rstrip(".")
        log21.debug(
            "Requested %s for `%s`",
            args=(
                QTYPE.get(question.qtype),
                domain,
            ),
        )

        # Pattern matching
        for pattern, rdata in OVERRIDE.get(question.qtype, {}).items():
            if pattern.match(domain):
                log21.debug(
                    "Adding %s for `%s`",
                    args=(
                        rdata,
                        domain,
                    ),
                )
                request.add_answer(RR(domain, question.qtype, ttl=60, rdata=rdata))

        # print("------------------------------------------------------------")
        # print(request)
        # print("------------------------------------------------------------")

        # Return the result if any patterns were matched
        # "a" is no. answers
        if request.header.a > 0:
            return request

        # Request IP from the upstream server
        try:
            data = self.call_upstream(request)
            request = data
        except UpstreamIndexNotFoundError:
            pass
        except Exception as e:
            log21.error(
                "Failed to retrieve IP from upstream servers: %s, %s",
                args=(e.__class__.__name__, e),
            )
        finally:
            return request


def main(address: str = "127.0.0.1", port: int = 5353, verbose: bool = False):
    """A simple DNS server meant for overriding some records.

    For better control over different values you can modify the script.

    :param address: The IP address to run the server on. (default: 127.0.0.1)
    :param port: The port to run the dns on. (default: 5353)
    :param verbose: Whether to write the debug logs to standard output.
    """
    if verbose:
        log21.basic_config(level="DEBUG")

    resolver = CustomResolver()
    server = DNSServer(resolver, port=port, address=address)
    log21.info("DNS server running on '%s:%d'", args=(address, port))
    server.start()


if __name__ == "__main__":
    try:
        log21.argumentify(main)
    except KeyboardInterrupt:
        log21.critical("KeyboardInterrupt: Exiting...")
