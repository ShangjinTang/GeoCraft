from ._baidumap_parser import parse_geojson, parse_polygon
from .polygon_output_type import PolygonOutputType


class BaidumapParser:
    _instances = {}

    def __new__(cls, output_type: PolygonOutputType = PolygonOutputType.DEFAULT):
        key = f"{output_type.value}"
        if key not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[key] = instance
        return cls._instances[key]

    def __init__(self, output_type: PolygonOutputType = PolygonOutputType.DEFAULT):
        self.output_type = output_type

    def parse(self, uid: str):
        if self.output_type == PolygonOutputType.DEFAULT:
            return parse_polygon(uid)
        elif self.output_type == PolygonOutputType.GEOJSON:
            return parse_geojson(uid)
