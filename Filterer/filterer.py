#!/usr/bin/env python
# CodeWriter21

# Used for pattern matching.
import re
# Used for formatting exceptions.
import traceback
# Used for logging and parsing commandline arguments.
from log21 import ColorizingArgumentParser, get_logger, get_colors as gc

# Defines a logger
logger = get_logger('Replacer', show_level=False)


# Main function of the script.
def main():
    # Define the command line argument parser.
    parser = ColorizingArgumentParser(colors={'values': 'Yellow'})
    parser.add_argument('FileName', action='store', type=str, help='File path to the target file.')
    parser.add_argument('SavePath', action='store', type=str, help='File path to save the output.')
    parser.add_argument('--in', '-i', action='store', type=str, dest='in_',
                        help='Only save the lines that have this word.')
    parser.add_argument('--not-in', '-n', action='store', type=str,
                        help="Only save the lines that don't have this word.")
    parser.add_argument('--startswith', '-s', action='store', type=str,
                        help='Only save the lines that start with this word.')
    parser.add_argument('--endswith', '-e', action='store', type=str,
                        help="Only save the lines that end with this word.")
    parser.add_argument('--only', '-o', action='store', type=str,
                        help='Save the lines that only have these characters.')
    parser.add_argument('--no', '-no', action='store', type=str,
                        help="Save the lines that don't have these characters.")
    parser.add_argument('--regex-match', '-m', action='store', type=str, help="Use regular expression match function.")
    parser.add_argument('--regex-full-match', '-M', action='store', type=str,
                        help="Use regular expression full match function.")

    # Parses the command line arguments
    args = parser.parse_args()

    if not any([args.in_, args.not_in, args.only, args.no, args.startswith, args.endswith, args.regex_match,
                args.regex_full_match]):
        logger.error(gc('lr') + 'No mode chosen!')
        logger.error(gc('lm') + 'Please chose a mode' + gc('lr') + ': ' + gc('lc') + '--in' + gc('lr') + ', ' +
                     gc('lc') + '--not-in' + gc('lr') + ', ' + gc('lc') + '--startswith' + gc('lr') + ', ' + gc('lc') +
                     '--endswith' + gc('lr') + ', ' + gc('lc') + '--only' + gc('lr') + ', ' + gc('lc') + '--regex-match'
                     + gc('lr') + ', ' + gc('lc') + '--regex-full-match' + gc('lr') + ', ' + gc('lc') + '--no')
        exit()

    # Opens the input and output files
    input_file = open(args.FileName, 'r')
    output_file = open(args.SavePath, 'w')

    logger.info('Starting...')
    line_number = 1

    # Defines the condition
    condition = ''
    if args.in_:
        condition += '(args.in_ in line)'
    if args.not_in:
        if condition:
            condition += ' and '
        condition += '(args.not_in not in line)'
    if args.startswith:
        if condition:
            condition += ' and '
        condition += '(line.startswith(args.startswith))'
    if args.endswith:
        if condition:
            condition += ' and '
        condition += '(line[:-1].endswith(args.endswith))'
    if args.only:
        if condition:
            condition += ' and '
        condition += '(set(line[:-1]).issubset(set(args.only)))'
    if args.no:
        if condition:
            condition += ' and '
        condition += '(len(set(args.no).difference(set(line))) == len(set(args.no)))'
    if args.regex_match:
        if condition:
            condition += ' and '
        condition += '(re.match(args.regex_match, line[:-1]))'
    if args.regex_full_match:
        if condition:
            condition += ' and '
        condition += '(re.fullmatch(args.regex_full_match, line[:-1]))'

    # Reads the input lines
    # Checks if the condition is True for each line
    # Writes the lines that match the condition to the output file
    while True:
        try:
            line = input_file.readline()
        # Handles the UnicodeDecodeError; Skips the line.
        except UnicodeDecodeError:
            logger.print('Line', line_number, ':', traceback.format_exc())
            line_number += 1
            continue

        # Checks if it's the end of the file and breaks the loop
        if not line:
            break

        # Writes the line to the output file
        if eval(condition):
            output_file.write(line)
        line_number += 1
    logger.info('Done!')

    # Closes the input and output files
    input_file.close()
    output_file.close()


if __name__ == "__main__":
    main()
