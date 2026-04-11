#!/usr/bin/env python
# CodeWriter21

# Used for formatting exceptions.
import traceback
# Used for logging and parsing commandline arguments.
from log21 import ColorizingArgumentParser, get_logger

# Defines a logger
logger = get_logger('Replacer', show_level=False)


# Main function of the script.
def main():
    # Define the command line argument parser.
    parser = ColorizingArgumentParser()
    parser.add_argument('FileName', action='store', type=str, help='File path to the target file.')
    parser.add_argument('SavePath', action='store', type=str, help='File path to save the output.')
    parser.add_argument('Old', action='store', type=str, help="The Old word to be replaced.")
    parser.add_argument('New', action='store', type=str, help="The New word to replace.")

    # Parses the command line arguments
    args = parser.parse_args()

    # Opens the input and output files
    input_file = open(args.FileName, 'r')
    output_file = open(args.SavePath, 'w')

    line_number = 1
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
        output_file.write(line.replace(args.Old, args.New))
        line_number += 1

    # Closes the input and output files
    input_file.close()
    output_file.close()


if __name__ == "__main__":
    main()
