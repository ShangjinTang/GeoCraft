#!/usr/bin/env python3

import argparse

from geocraft import CoordConverter, CoordType


def get_enum_from_string(enum_str):
    try:
        return CoordType[enum_str.upper()]
    except KeyError:
        raise ValueError("Invalid enum value")


def main():
    valid_type_strs = [e.value for e in CoordType]
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "-i",
        "--input_type",
        required=True,
        type=str,
        choices=valid_type_strs,
        help="Input coordinate system type",
    )
    parser.add_argument(
        "-o",
        "--output_type",
        required=True,
        type=str,
        choices=valid_type_strs,
        help="Output coordinate system type",
    )
    parser.add_argument(
        "-c", "--coordinate", required=True, type=str, help="Input coordinate"
    )

    args = parser.parse_args()

    try:
        coord_converter = CoordConverter(
            get_enum_from_string(args.input_type),
            get_enum_from_string(args.output_type),
        )
        lnglat = args.coordinate.strip().split(",")
        if len(lnglat) != 2:
            raise argparse.ArgumentError("--coordinate must be size 2")
        lng, lat = float(lnglat[0].strip()), float(lnglat[1].strip())
        converted_coord = coord_converter.convert(lng, lat)
        print(converted_coord)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
