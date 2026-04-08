#!/usr/bin/env python3

# Used for formatting exceptions.
import traceback

# Used for normalization.
import unicodedata
import re

# Used for logging and parsing commandline arguments.
from log21 import ColorizingArgumentParser, get_logger

# Defines a logger
logger = get_logger('Splitter', show_level=False)


def strip_accents(text: str) -> str:
    """
    Strips the accent characters in the input text.

    :param text: str: The input text.
    :return: str
    """
    # Normalizes the text: https://unicode.org/reports/tr15/#Norm_Forms
    # Removes the Nonspacing Marks(Mn): http://www.unicode.org/reports/tr44/#GC_Values_Table
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    text = text.replace('Đ', 'D')
    text = text.replace('đ', 'd')
    text = text.replace('Ł', 'L')
    text = re.sub(u'[ß§]', 'S', text)
    return text


# Main function of the script.
def main():
    # Define the command line argument parser.
    parser = ColorizingArgumentParser()
    parser.add_argument('FileName', action='store', type=str, help='File path to the target file.')
    parser.add_argument('SavePath', action='store', type=str, help='File path to save the output.')

    # Parses the command line arguments
    args = parser.parse_args()

    # Opens the input and output files
    input_file = open(args.FileName, 'r', encoding='utf-8')
    output_file = open(args.SavePath, 'w', encoding='utf-8')

    line_number = 1
    logger.info('Starting...')
    while True:
        try:
            line = input_file.readline()
        # Handles the UnicodeDecodeError; Skips the line.
        except UnicodeDecodeError:
            logger.error('Line', line_number, ':', traceback.format_exc())
            line_number += 1
            continue

        # Checks if it's the end of the file and breaks the loop
        if not line:
            break

        # Writes the progress to the console
        if line_number % 100 == 0:
            logger.info('Processing line', line_number, end='')
            logger.handlers[0].flush()

        try:
            output_file.write(strip_accents(line))
        except UnicodeDecodeError:
            logger.error('Line', line_number, ':', traceback.format_exc())
        line_number += 1
    logger.info('')
    logger.info('Done')

    # Closes the input and output streams.
    input_file.close()
    output_file.close()


if __name__ == "__main__":
    main()
