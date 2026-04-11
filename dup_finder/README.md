DupFinder
=========

DupFinder is a python script that you can use to find duplicate files in one or more
directories.

Installation
------------

You need [Python3](https://Python.org) to run the script. [INSTALL PYTHON](https://Python.org)

### Used Packages

- [traceback](https://docs.python.org/3/library/traceback.html)
- [log21](https://github.com/MPCodeWriter21/log21)

_You can use `pip install -r requirements.txt` to install the required packages._

Usage
-----

```help
usage: dup_finder.py [-h] [--min-size MIN_SIZE] [--output OUTPUT] [--output-format
                     OUTPUT_FORMAT] [--quiet] [--verbose]
                     [paths ...]

Find duplicate files.

positional arguments:
  paths             Directories to scan for duplicate files in.

options:
  -h, --help
                        show this help message and exit
  --min-size MIN_SIZE, -m MIN_SIZE
                        Files smaller than this size will be ignored. (Default: 100KiB)
  --output OUTPUT, -o OUTPUT
                        Path to save the results of the scan.
  --output-format OUTPUT_FORMAT, -O OUTPUT_FORMAT
                        The format to output the results (normal or json)
  --quiet, -q
                        Write less to the standard output.
  --verbose, -v
                        Write more logs to the standard output.

```

### Example

```bash
uv run dup_finder.py ./docs -O normal -v -m "5MB"

# Or 

python dup_finder.py ./docs -O normal -v -m "5MB"
```

About
-----

Author: CodeWriter21 (Mehrad Pooryoussof)

GitHub: [MPCodeWriter21](https://github.com/MPCodeWriter21)

Telegram Channel: [@CodeWriter21](https://t.me/CodeWriter21)
