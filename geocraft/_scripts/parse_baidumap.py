#!/usr/bin/env python3

import argparse

from geocraft.unstable import BaidumapParser


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "-i",
        "--input_uid",
        required=True,
        type=str,
        help="BaiduMap UID",
    )
    parser.add_argument(
        "-o",
        "--output_type",
        required=False,
        type=str,
        default="",
        choices=["", "geojson"],
        help="Output Polygon Type",
    )

    args = parser.parse_args()

    try:
        parser = BaidumapParser(output_type=args.output_type)
        print(parser.parse(args.input_uid))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
