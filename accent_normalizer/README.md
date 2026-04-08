AccentNormalizer
================

AccentNormalizer is a python script that you can use to replace each accent character in
your file with regular character.

Installation
------------

You need [Python3](https://Python.org) to run the script. [INSTALL PYTHON](https://Python.org)

### Used Packages

- [traceback](https://docs.python.org/3/library/traceback.html)
- [unicodedata](https://docs.python.org/3/library/unicodedata.html)
- [re](https://docs.python.org/3/library/re.html)
- [log21](https://github.com/MPCodeWriter21/log21)

_You can use `pip install -r requirements.txt` to install the required packages._

Usage
-----

```
usage: normalizer.py [-h] FileName SavePath

positional arguments:
  FileName          File path to the target file.
  SavePath          File path to save the output.

options:
  -h, --help
                        show this help message and exit
```

### Example

```shell
python normalizer.py example-input.txt output.txt
```

About
-----

Author: CodeWriter21 (Mehrad Pooryoussof)

GitHub: [MPCodeWriter21](https://github.com/MPCodeWriter21)

Telegram Channel: [@CodeWriter21](https://t.me/CodeWriter21)

