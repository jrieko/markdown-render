#!/usr/bin/python3

import sys
import argparse
import logging
import md.dom

def main(input):
    dom = md.dom.DOM()
    dom.parse(input)
    return dom.render().getvalue()

def main_open(path, mode='r'):
    if isinstance(path, str):
        return open(path, mode)
    return path


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="enable debug logging", action="store_true")
    parser.add_argument("-v", "--verbose", help="enable info logging", action="store_true")
    parser.add_argument("-i", "--input", help="source Markdown file. Read from stdin if not specified.", default=sys.stdin)
    parser.add_argument("-o", "--output", help="destination HTML file. Write to stdout if not specified.", default=sys.stdout)
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif args.verbose:
        logging.basicConfig(level=logging.INFO)

    with main_open(args.input) as inputFile:
        html = main(inputFile.read())
    with main_open(args.output, 'w') as outputFile:
        outputFile.write(html)

