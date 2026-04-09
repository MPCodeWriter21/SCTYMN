DNS Server
==========

This is a simple DNS server implemented in Python. It listens for DNS queries and
responds with the appropriate IP address based on a predefined mapping or forwards the
query to an upstream DNS server if the domain is not found in the mapping.

How it works
------------

The server uses the `dnslib` library to handle DNS requests and responses. It maintains
a mapping for each different query type (A, AAAA, CNAME, etc.). Each mapping is a
dictionary where the keys are RegEx patterns for domain names, and the values are the
corresponding RD values (e.g., IP addresses for A records).

When a DNS query is received, the server checks the query type and looks for a matching
pattern in the corresponding mapping.

- If one or more matches are found, the server adds them to the DNS record and sends the
  response back to the client.
- If no matches are found, the server forwards the query to an upstream DNS server.

Prerequisites
-------------

You need [Python3](https://Python.org) to run the script.

### Used Packages

- [dnslib](https://github.com/paulc/dnslib)
- [log21](https://github.com/MPCodeWriter21/log21)

_You can use `pip install -r requirements.txt` to install the required packages._

Usage
-----

```help
usage: dns.py [-h] [--address ADDRESS] [--port PORT] [--verbose]

A simple DNS server meant for overriding some records. For better control over different
values you can modify the script.

options:
  -h, --help
                        show this help message and exit
  --address ADDRESS, -a ADDRESS
                        The IP address to run the server on. (default: 127.0.0.1)
  --port PORT, -p PORT
                        The port to run the dns on. (default: 5353)
  --verbose, -v
                        Whether to write the debug logs to standard output.

```

### Example

```shell
uv run dns.py -a 127.0.0.1 -p 53

# Or
python dns.py -a 127.0.0.1 -p 53
```

About
-----

Author: CodeWriter21 (Mehrad Pooryoussof)

GitHub: [MPCodeWriter21](https://github.com/MPCodeWriter21)

Telegram Channel: [@CodeWriter21](https://t.me/CodeWriter21)
