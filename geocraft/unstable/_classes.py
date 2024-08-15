from typing import Literal

from ._baidumap_parser import parse_geojson, parse_polygon

OutputType = Literal["", "geojson"]


class BaidumapParser:
    _instances = {}

    def __new__(cls, output_type: OutputType = ""):
        key = f"{output_type}"
        if key not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[key] = instance
        return cls._instances[key]

    def __init__(self, output_type: OutputType = ""):
        self.output_type = output_type

    def parse(self, uid: str):
        if self.output_type == "":
            return parse_polygon(uid)
        elif self.output_type == "geojson":
            return parse_geojson(uid)
