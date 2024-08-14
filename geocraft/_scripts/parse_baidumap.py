#!/usr/bin/env python3

import argparse

from geocraft.unstable import BaidumapParser, PolygonOutputType


def get_enum_from_string(enum_str):
    try:
        return PolygonOutputType[enum_str.upper()]
    except KeyError:
        raise ValueError("Invalid enum value")


def main():
    valid_polygon_output_type_strs = [e.value for e in PolygonOutputType]
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
        default="default",
        choices=valid_polygon_output_type_strs,
        help="Output Polygon Type",
    )

    args = parser.parse_args()

    try:
        parser = BaidumapParser(output_type=get_enum_from_string(args.output_type))
        print(parser.parse(args.input_uid))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
