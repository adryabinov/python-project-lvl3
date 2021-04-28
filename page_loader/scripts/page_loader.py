#!/usr/bin/env python
import logging
import sys

import page_loader.args as args
from page_loader.page import download


def main():
    try:
        arguments = args.parse()
        print(download(arguments.url, arguments.output))
    except Exception as error:
        logging.error(error)
        sys.exit(1)


if __name__ == '__main__':
    main()
