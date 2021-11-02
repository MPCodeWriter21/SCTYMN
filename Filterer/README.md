Filterer
========

Filterer is a python script that you can use inorder to filter each line of your file and save only the lines that match
your filter.

Installation
------------

You need [Python3](https://Python.org) inorder to run the script. [INSTALL PYTHON](https://Python.org)

#### Required Packages

- [re](https://docs.python.org/3/library/re.html) (Comes with Python core.)
- [traceback](https://docs.python.org/3/library/traceback.html) (Comes with Python core.)
- [log21](https://github.com/MPCodeWriter21/log21) (Install using `python3 -m pip install log21`)

_You can use `pip install -r requirements.txt` to install the required packages._

Usage
-----

```
usage: filterer.py [-h] [--in IN_] [--not-in NOT_IN] [--startswith STARTSWITH] [--endswith
                   ENDSWITH] [--only ONLY] [--no NO] [--regex-match REGEX_MATCH]
                   [--regex-full-match REGEX_FULL_MATCH]
                   FileName SavePath

positional arguments:
  FileName          File path to the target file.
  SavePath          File path to save the output.

options:
  -h, --help
                        show this help message and exit
  --in IN_, -i IN_
                        Only save the lines that have this word.
  --not-in NOT_IN, -n NOT_IN
                        Only save the lines that don't have this word.
  --startswith STARTSWITH, -s STARTSWITH
                        Only save the lines that start with this word.
  --endswith ENDSWITH, -e ENDSWITH
                        Only save the lines that end with this word.
  --only ONLY, -o ONLY
                        Save the lines that only have these characters.
  --no NO, -no NO
                        Save the lines that don't have these characters.
  --regex-match REGEX_MATCH, -m REGEX_MATCH
                        Use regular expression match function.
  --regex-full-match REGEX_FULL_MATCH, -M REGEX_FULL_MATCH
                        Use regular expression full match function.
```

### Example

You can try ;D

+ IN: Saves only the lines that contain the input word

```shell
python filterer.py InputFile.txt OutputFile1.txt -i 21
```

+ NOT IN: Saves only the lines that do not contain the input word

```shell
python filterer.py InputFile.txt OutputFile2.txt -n er
```

+ STARTSWITH: Saves only lines that start with the input phrase

```shell
python filterer.py InputFile.txt OutputFile3.txt -s C
```

+ ENDSWITH: Saves only lines that end with the input phrase

```shell
python filterer.py InputFile.txt OutputFile4.txt -e t
```

+ ONLY: Saves only lines that consist of the desired characters

```shell
python filterer.py InputFile.txt OutputFile5.txt -o abcdef1234567890
```

+ NO: Saves only lines that don't contain the desired characters

```shell
python filterer.py InputFile.txt OutputFile6.txt -no abcdef1234567890
```

+ REGEX MATCH: Saves only lines that match the regex pattern

```shell
python filterer.py InputFile.txt OutputFile7.txt -m "\w+"
```

+ REGEX FULL MATCH: Saves only lines that fully match the regex pattern

```shell
python filterer.py InputFile.txt OutputFile8.txt -M "\w+"
```

About
-----

Author: CodeWriter21 (Mehrad Pooryoussof)

GitHub: [MPCodeWriter21](https://github.com/MPCodeWriter21)

Telegram Channel: [@CodeWriter21](https://t.me/CodeWriter21)

Aparat Channel: [CodeWriter21](https://www.aparat.com/CodeWriter21)