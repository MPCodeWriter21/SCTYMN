#!/usr/bin/env python3

import sys
import json
from typing import Literal, TypeAlias
from hashlib import sha256
from pathlib import Path

from log21 import (
    RequiredArgumentError,
    IncompatibleArgumentsError,
    get_logger,
    argumentify,
)
from log21.helper_types import FileSize

logger = get_logger("DupFinder", show_level=False)

StrPath: TypeAlias = str
StrHash: TypeAlias = str

size_mapping: dict[int, list[Path]] = {}
hash_mapping: dict[tuple[int, StrHash], list[StrPath]] = {}


def traverse_directory(path: Path, min_size: int = -1) -> None:
    """Traverse a directory and populate the size_mapping dictionary.

    :param path: The path to traverse
    :param min_size: The minimum file-size to add to size_mapping dictionary (in bytes)
    """

    # Check if the input path exists
    if not path.exists():
        logger.error("`%s` does not exist! Skipping...", args=(path,))

    # If it is an actual directory, traverse it further
    elif path.is_dir():
        # logger.debug("Traversing `%s`...", args=(path,))
        for item in path.iterdir():
            traverse_directory(item, min_size)

    # If the path is a file, add it to the size mapping
    elif path.is_file():
        size = path.stat().st_size
        if size < min_size:
            return
        if size not in size_mapping:
            size_mapping[size] = []
        size_mapping[size].append(path)

    # Should not happen, I think...
    else:
        logger.error("`%s` is neither a file nor a directory!", args=(path,))


def main(
    *paths: Path,
    min_size: FileSize = FileSize("100 KiB"),
    output: Path | None = None,
    output_format: Literal["normal", "json"] = "normal",
    quiet: bool = False,
    verbose: bool = False,
):
    """Find duplicate files.

    :param paths: Directories to scan for duplicate files in.
    :param min_size: Files smaller than this size will be ignored. (Default: 100KiB)
    :param output: Path to save the results of the scan.
    :param output_format: The format to output the results (normal or json)
    :param quiet: Write less to the standard output.
    :param verbose: Write more logs to the standard output.
    """

    if len(paths) < 1:
        raise RequiredArgumentError("paths")
    if verbose and quiet:
        raise IncompatibleArgumentsError("verbose", "quiet")

    if verbose:
        logger.setLevel("DEBUG")
    if quiet:
        logger.setLevel("ERROR")

    if min_size > 0:
        logger.debug(f"Files smaller than {min_size!s} will be ignored.")

    # Populate the size_mapping dictionary
    for path in paths:
        logger.info("Checking `%s`...", args=(path,))
        if not path.exists():
            logger.error("`%s` does not exist! Skipping...", args=(path,))
        traverse_directory(path, int(min_size))

    logger.info("Traversing done.")

    s = len(size_mapping)
    # Find the files with the same size and populate hash_mapping dictionary
    for i, (size, files) in enumerate(size_mapping.items()):
        # Skip sizes that have less than 2 files assigned to them
        if len(files) < 2:
            continue

        logger.debug("\r%d/%d...", args=(i, s), end="")

        # Compare the files of the same size by their sha256 hash value
        for file_path in files:
            h = sha256()
            with file_path.open(mode="rb") as file:
                while data := file.read(4096):
                    h.update(data)
            key = (size, h.hexdigest())
            if key not in hash_mapping:
                hash_mapping[key] = []
            hash_mapping[key].append(str(file_path.absolute()))
    logger.debug("\r%d/%d...", args=(i, s))

    logger.info("Hashing done.")

    output_file = sys.stdout
    if output:
        output_file = output.open(mode="w", encoding="utf-8")

    if output_format == "normal":
        # Log the path of the duplicate files
        for key, files in hash_mapping.items():
            if len(files) < 2:
                continue

            print(key[0], key[1], file=output_file)
            for file_path in files:
                print(file_path, file=output_file)
            print(file=output_file)
    elif output_format == "json":
        results = [
            {"size": key[0], "sha256": key[1], "paths": value}
            for key, value in hash_mapping.items()
            if len(value) > 1
        ]

        json.dump(results, output_file)

    if output:
        output_file.close()


if __name__ == "__main__":
    try:
        argumentify(main)
    except KeyboardInterrupt:
        logger.critical("KeyboardInterrupt! Exiting...")
