Splitter
========

Splitter is a python script that you can use in order to split each line of your file
into some parts and save some parts into another file.

Installation
------------

You need [Python3](https://Python.org) in order to run the script. [INSTALL PYTHON](https://Python.org)

### Used Packages

- [traceback](https://docs.python.org/3/library/traceback.html)
- [typing](https://docs.python.org/3/library/typing.html)
- [log21](https://github.com/MPCodeWriter21/log21)

_You can use `pip install -r requirements.txt` to install the required packages._

Usage
-----

```
usage: splitter.py [-h] [--splitter SPLITTER] [--columns COLUMNS] FileName SavePath

positional arguments:
  FileName          File path to the target file.
  SavePath          File path to save the output.

options:
  -h, --help
                        show this help message and exit
  --splitter SPLITTER, -s SPLITTER
                        A splitter character to split columns in each row.
  --columns COLUMNS, -c COLUMNS
                        Columns to save into the output file.
```

### Example

```shell
python splitter.py example-input.txt example-output.txt -s , -c 1,3-5
```

About
-----

Author: CodeWriter21 (Mehrad Pooryoussof)

GitHub: [MPCodeWriter21](https://github.com/MPCodeWriter21)

Telegram Channel: [@CodeWriter21](https://t.me/CodeWriter21)
