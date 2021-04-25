import argparse
import os


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Downloads html page with resources"
    )
    parser.add_argument(
        "--output",
        "-o",
        default=os.getcwd(),
        help="set output dir"
    )
    parser.add_argument("url")
    return parser.parse_args()
