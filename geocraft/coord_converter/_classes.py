from . import _converter


class CoordConverter:
    WGS84 = "wgs84"
    WGS84MC = "wgs84mc"
    GCJ02 = "gcj02"
    GCJ02MC = "gcj02mc"
    BD09 = "bd09"
    BD09MC = "bd09mc"

    _instances = {}

    def __new__(cls, src, target):
        key = f"{src}_{target}"
        if key not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[key] = instance
        return cls._instances[key]

    def __init__(self, src, target):
        self.src = src
        self.target = target

    def convert(self, lng, lat):
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
