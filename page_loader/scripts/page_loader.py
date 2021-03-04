#!/usr/bin/env python
from page_loader.argparse import parse_arguments
from page_loader.comparator import download

def main():
    args = parse_arguments()
    print(download(args.url, args.output))


if __name__ == '__main__':
    main()
