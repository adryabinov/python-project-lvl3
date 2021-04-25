#!/usr/bin/env python
import logging
import sys

from page_loader.argparse import parse_arguments
from page_loader.comparator import download


def main():
    try:
        args = parse_arguments()
        print(download(args.url, args.output))
    except Exception as error:
        logging.error(error)
        sys.exit(1)


if __name__ == '__main__':
    main()
