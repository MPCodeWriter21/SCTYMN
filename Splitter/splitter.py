#!/usr/bin/env python3
# CodeWriter21

# Used for formatting exceptions.
import traceback
from typing import List
# Used for logging and parsing commandline arguments.
from log21 import ColorizingArgumentParser, get_logger

# Defines a logger
logger = get_logger('Splitter', show_level=False)


def to_indexes(input_range: str) -> List[int]:
    """
    Takes a string representing some indexes and returns a list of integers containing the indexes.
    >>>
    >>> to_indexes('2, 5-8, 21')
    [2, 5, 6, 7, 8, 21]
    >>>

    :param input_range: str
    :return: List[int]: A list containing the numbers in the range.
    """
    input_range = input_range.replace(' ', '')
    if not set(input_range).issubset(set('1234567890,-')):
        raise SyntaxError(f"The following characters are not allowed: {set(input_range) - set('1234567890,-')}\n"
                          f"Only use numbers(0-9), comma(,) or dash(-)!")
    result = []
    for part in input_range.split(','):
        if '-' in part:
            a, b = part.split('-')
            result.extend(range(int(a), int(b) + 1))
        else:
            result.append(int(part))
    return result


# Main function of the script.
def main():
    # Define the command line argument parser.
    parser = ColorizingArgumentParser()
    parser.add_argument('FileName', action='store', type=str, help='File path to the target file.')
    parser.add_argument('SavePath', action='store', type=str, help='File path to save the output.')
    parser.add_argument('--splitter', '-s', action='store', type=str,
                        help="A splitter character to split columns in each row.")
    parser.add_argument('--columns', '-c', action='store', type=str, help="Columns to save into the output file.")

    # Parses the command line arguments
    args = parser.parse_args()

    # Converts the input columns string to a list of numbers
    if args.columns:
        columns = to_indexes(args.columns)
    else:
        columns = [1]
    # Sets splitter to ',' if the user did not specify splitter
    splitter = args.splitter or ','

    # Opens the input and output files
    input_file = open(args.FileName, 'r')
    output_file = open(args.SavePath, 'w')

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

        # Splits the data of the line
        data = [part.strip() for part in line[:-1].split(args.splitter)]

        try:
            txt = (splitter.join(data[index - 1] for index in columns))
            output_file.write(txt + '\r\n')
        # Handles the IndexError; Skips the line.
        except IndexError:
            logger.error(f'Line {line_number} has {len(data)} parts! requested parts: {columns}')
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
