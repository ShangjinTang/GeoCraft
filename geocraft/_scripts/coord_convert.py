#!/usr/bin/env python3

import argparse

from geocraft import CoordConverter


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "-i",
        "--input_type",
        required=True,
        type=str,
        choices=["wgs84", "wgs84mc", "bd09", "bd09mc", "gcj02", "gcj02mc"],
        help="Input coordinate system type",
    )
    parser.add_argument(
        "-o",
        "--output_type",
        required=True,
        type=str,
        choices=["wgs84", "wgs84mc", "bd09", "bd09mc", "gcj02", "gcj02mc"],
        help="Output coordinate system type",
    )
    parser.add_argument(
        "-c", "--coordinate", required=True, type=str, help="Input coordinate"
    )

    args = parser.parse_args()

    try:
        coord_converter = CoordConverter(args.input_type, args.output_type)
        lnglat = args.coordinate.strip().split(",")
        if len(lnglat) != 2:
            raise argparse.ArgumentError(args.coordinate, "must be size 2")
        lng, lat = float(lnglat[0].strip()), float(lnglat[1].strip())
        converted_coord = coord_converter.convert(lng, lat)
        print(converted_coord)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
