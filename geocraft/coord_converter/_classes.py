from typing import Literal

from . import _converter

CoordType = Literal["wgs84", "wgs84mc", "bd09", "bd09mc", "gcj02", "gcj02mc"]


class CoordConverter:
    _instances = {}

    def __new__(cls, src: CoordType, target: CoordType):
        key = f"{src}_{target}"
        if key not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[key] = instance
        return cls._instances[key]

    def __init__(self, src: CoordType, target: CoordType):
        self.src = src
        self.target = target

    def convert(self, lng: float, lat: float):
        conversion_func_name = f"{self.src}_to_{self.target}"
        conversion_func = getattr(_converter, conversion_func_name, None)

        if conversion_func:
            result_lng, result_lat = conversion_func(lng, lat)
            return result_lng, result_lat
        else:
            if self.src == self.target:
                raise RuntimeError(
                    "Source coordinate system and target coordinate system are identical."
                )
            else:
                raise RuntimeError(
                    f"Unsupported coordinate conversion from {self.src} to {self.target}."
                )
