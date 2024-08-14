#!/usr/bin/env python3

import argparse

from geocraft.unstable import parse_baidumap_geojson, parse_baidumap_polygon


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
        choices=["default", "geojson"],
        default="default",
        help="Output Type",
    )

    args = parser.parse_args()

    try:
        if args.output_type == "default":
            print(parse_baidumap_polygon(args.input_uid))
        elif args.output_type == "geojson":
            print(parse_baidumap_geojson(args.input_uid))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
