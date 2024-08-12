from ..coord_type import CoordType
from . import _converter


class CoordConverter:
    _instances = {}

    def __new__(cls, src: CoordType, target: CoordType):
        key = f"{src.value}_{target.value}"
        if key not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[key] = instance
        return cls._instances[key]

    def __init__(self, src: CoordType, target: CoordType):
        self.src = src
        self.target = target

    def convert(self, lng: float, lat: float):
        conversion_func_name = f"{self.src.value}_to_{self.target.value}"
        conversion_func = getattr(_converter, conversion_func_name, None)

        if conversion_func:
            result_lng, result_lat = conversion_func(lng, lat)
            return result_lng, result_lat
        else:
            if self.src.value == self.target.value:
                raise RuntimeError(
                    "Source coordinate system and target coordinate system are identical."
                )
            else:
                raise RuntimeError(
                    f"Unsupported coordinate conversion from {self.src.value} to {self.target.value}."
                )
