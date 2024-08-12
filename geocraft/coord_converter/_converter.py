"""
_converter.py

This module provides functions for converting coordinates between different coordinate systems commonly used in mapping applications.

Coordinate Systems:

- wgs84: Standard GPS coordinates, see [EPSG:4326](https://spatialreference.org/ref/epsg/4326/).
- wgs84mc: Standard GPS mercator coordinates, see [EPSG:3857](https://spatialreference.org/ref/epsg/3857/).

- gcj02: Coordinates used by [Amap](https://ditu.amap.com/) and [Tencent Map](https://map.qq.com/).
- gcj02mc: Mercator coordinates used by [Amap](https://ditu.amap.com/) and [Tencent Map](https://map.qq.com/).

- bd09: Coordinates used by [Baidu Map](https://map.baidu.com/).
- bd09mc: Mercator coordinates used by [Baidu Map](https://map.baidu.com/).

"""

import math

x_PI: float = 3.14159265358979324 * 3000.0 / 180.0
PI: float = 3.1415926535897932384626
a: float = 6378245.0
ee: float = 0.00669342162296594323


def bd09_to_gcj02(lng: float, lat: float) -> tuple[float, float]:
    x: float = lng - 0.0065
    y: float = lat - 0.006
    z: float = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_PI)
    theta: float = math.atan2(y, x) - 0.000003 * math.cos(x * x_PI)
    gg_lng: float = z * math.cos(theta)
    gg_lat: float = z * math.sin(theta)
    return gg_lng, gg_lat


def gcj02_to_bd09(lng: float, lat: float) -> tuple[float, float]:
    z: float = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_PI)
    theta: float = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_PI)
    bd_lng: float = z * math.cos(theta) + 0.0065
    bd_lat: float = z * math.sin(theta) + 0.006
    return bd_lng, bd_lat


def wgs84_to_gcj02(lng: float, lat: float) -> tuple[float, float]:
    if out_of_china(lng, lat):
        return lng, lat
    else:
        dlat: float = transformlat(lng - 105.0, lat - 35.0)
        dlng: float = transformlng(lng - 105.0, lat - 35.0)
        radlat: float = lat / 180.0 * PI
        magic: float = math.sin(radlat)
        magic: float = 1 - ee * magic * magic
        sqrtmagic: float = math.sqrt(magic)
        dlat: float = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * PI)
        dlng: float = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * PI)
        mglat: float = lat + dlat
        mglng: float = lng + dlng
        return mglng, mglat


def gcj02_to_wgs84(lng: float, lat: float) -> tuple[float, float]:
    if out_of_china(lng, lat):
        return lng, lat
    else:
        dlat: float = transformlat(lng - 105.0, lat - 35.0)
        dlng: float = transformlng(lng - 105.0, lat - 35.0)
        radlat: float = lat / 180.0 * PI
        magic: float = math.sin(radlat)
        magic: float = 1 - ee * magic * magic
        sqrtmagic: float = math.sqrt(magic)
        dlat: float = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * PI)
        dlng: float = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * PI)
        mglat: float = lat + dlat
        mglng: float = lng + dlng
        return lng * 2 - mglng, lat * 2 - mglat


def transformlat(lng: float, lat: float) -> float:
    ret: float = (
        -100.0
        + 2.0 * lng
        + 3.0 * lat
        + 0.2 * lat * lat
        + 0.1 * lng * lat
        + 0.2 * math.sqrt(abs(lng))
    )
    ret += (
        (20.0 * math.sin(6.0 * lng * PI) + 20.0 * math.sin(2.0 * lng * PI)) * 2.0 / 3.0
    )
    ret += (20.0 * math.sin(lat * PI) + 40.0 * math.sin(lat / 3.0 * PI)) * 2.0 / 3.0
    ret += (
        (160.0 * math.sin(lat / 12.0 * PI) + 320 * math.sin(lat * PI / 30.0))
        * 2.0
        / 3.0
    )
    return ret


def transformlng(lng: float, lat: float) -> float:
    ret: float = (
        300.0
        + lng
        + 2.0 * lat
        + 0.1 * lng * lng
        + 0.1 * lng * lat
        + 0.1 * math.sqrt(abs(lng))
    )
    ret += (
        (20.0 * math.sin(6.0 * lng * PI) + 20.0 * math.sin(2.0 * lng * PI)) * 2.0 / 3.0
    )
    ret += (20.0 * math.sin(lng * PI) + 40.0 * math.sin(lng / 3.0 * PI)) * 2.0 / 3.0
    ret += (
        (150.0 * math.sin(lng / 12.0 * PI) + 300.0 * math.sin(lng / 30.0 * PI))
        * 2.0
        / 3.0
    )
    return ret


def out_of_china(lng: float, lat: float) -> bool:
    return not (73.66 < lng < 135.05 and 3.86 < lat < 53.55)


def bd09_to_wgs84(lng: float, lat: float) -> tuple[float, float]:
    gcj02 = bd09_to_gcj02(lng, lat)
    result = gcj02_to_wgs84(gcj02[0], gcj02[1])
    return result


def wgs84_to_bd09(lng: float, lat: float) -> tuple[float, float]:
    gcj02 = wgs84_to_gcj02(lng, lat)
    result = gcj02_to_bd09(gcj02[0], gcj02[1])
    return result


def ll_to_mc(lng: float, lat: float) -> tuple[float, float]:
    x = lng * 20037508.34 / 180
    y = math.log(math.tan((90 + lat) * math.pi / 360)) / (math.pi / 180)
    y = y * 20037508.34 / 180
    return x, y


wgs84_to_wgs84mc = ll_to_mc
gcj02_to_gcj02mc = ll_to_mc


def mc_to_ll(lng: float, lat: float) -> tuple[float, float]:
    x = lng / 20037508.34 * 180
    y = lat / 20037508.34 * 180
    y = 180 / math.pi * (2 * math.atan(math.exp(y * math.pi / 180)) - math.pi / 2)
    return x, y


wgs84mc_to_wgs84 = mc_to_ll
gcj02mc_to_gcj02 = mc_to_ll


def bd09_to_bd09mc(lng: float, lat: float) -> tuple[float, float]:
    BD09LL_BAND = [75, 60, 45, 30, 15, 0]
    BD09LL_TO_BD09MC_PARAMS = [
        [
            -0.0015702102444,
            111320.7020616939,
            1704480524535203,
            -10338987376042340,
            26112667856603880,
            -35149669176653700,
            26595700718403920,
            -10725012454188240,
            1800819912950474,
            82.5,
        ],
        [
            0.0008277824516172526,
            111320.7020463578,
            647795574.6671607,
            -4082003173.641316,
            10774905663.51142,
            -15171875531.51559,
            12053065338.62167,
            -5124939663.577472,
            913311935.9512032,
            67.5,
        ],
        [
            0.00337398766765,
            111320.7020202162,
            4481351.045890365,
            -23393751.19931662,
            79682215.47186455,
            -115964993.2797253,
            97236711.15602145,
            -43661946.33752821,
            8477230.501135234,
            52.5,
        ],
        [
            0.00220636496208,
            111320.7020209128,
            51751.86112841131,
            3796837.749470245,
            992013.7397791013,
            -1221952.21711287,
            1340652.697009075,
            -620943.6990984312,
            144416.9293806241,
            37.5,
        ],
        [
            -0.0003441963504368392,
            111320.7020576856,
            278.2353980772752,
            2485758.690035394,
            6070.750963243378,
            54821.18345352118,
            9540.606633304236,
            -2710.55326746645,
            1405.483844121726,
            22.5,
        ],
        [
            -0.0003218135878613132,
            111320.7020701615,
            0.00369383431289,
            823725.6402795718,
            0.46104986909093,
            2351.343141331292,
            1.58060784298199,
            8.77738589078284,
            0.37238884252424,
            7.45,
        ],
    ]

    def get_range(val: float, low: float, high: float) -> float:
        if low is not None:
            val = max(val, low)
        if high is not None:
            val = min(val, high)
        return val

    def get_loop(val: float, low: float, high: float) -> float:
        while val > high:
            val -= high - low
        while val < low:
            val += high - low
        return val

    def convertor(
        coord_dict: dict[str, float], param: list[float]
    ) -> tuple[float, float]:
        converted_lng = param[0] + param[1] * abs(coord_dict["lng"])
        base_val = abs(coord_dict["lat"]) / param[9]
        converted_lat = (
            param[2]
            + param[3] * base_val
            + param[4] * base_val * base_val
            + param[5] * base_val * base_val * base_val
            + param[6] * base_val * base_val * base_val * base_val
            + param[7] * base_val * base_val * base_val * base_val * base_val
            + param[8] * base_val * base_val * base_val * base_val * base_val * base_val
        )
        converted_lng *= -1 if coord_dict["lng"] < 0 else 1
        converted_lat *= -1 if coord_dict["lat"] < 0 else 1
        return converted_lng, converted_lat

    def convert_bd09ll_to_bd09mc(coord_dict: dict[str, float]) -> tuple[float, float]:
        coord_dict["lng"] = get_loop(coord_dict["lng"], -180, 180)
        coord_dict["lat"] = get_range(coord_dict["lat"], -74, 74)
        param = None
        for index in range(len(BD09LL_BAND)):
            if coord_dict["lat"] >= BD09LL_BAND[index]:
                param = BD09LL_TO_BD09MC_PARAMS[index]
                break
        if not param:
            for index in range(len(BD09LL_BAND) - 1, -1, -1):
                if coord_dict["lat"] <= -BD09LL_BAND[index]:
                    param = BD09LL_TO_BD09MC_PARAMS[index]
                    break
        if not param:
            raise ValueError("param shouldn't be None")
        return convertor(coord_dict, param)

    return convert_bd09ll_to_bd09mc({"lng": lng, "lat": lat})


def bd09mc_to_bd09(lng: float, lat: float) -> tuple[float, float]:
    BD09MC_BAND = [12890594.86, 8362377.87, 5591021, 3481989.83, 1678043.12, 0]
    BD09MC_TO_BD09LL_PARAMS = [
        [
            1.410526172116255e-8,
            0.00000898305509648872,
            -1.9939833816331,
            200.9824383106796,
            -187.2403703815547,
            91.6087516669843,
            -23.38765649603339,
            2.57121317296198,
            -0.03801003308653,
            17337981.2,
        ],
        [
            -7.435856389565537e-9,
            0.000008983055097726239,
            -0.78625201886289,
            96.32687599759846,
            -1.85204757529826,
            -59.36935905485877,
            47.40033549296737,
            -16.50741931063887,
            2.28786674699375,
            10260144.86,
        ],
        [
            -3.030883460898826e-8,
            0.00000898305509983578,
            0.30071316287616,
            59.74293618442277,
            7.357984074871,
            -25.38371002664745,
            13.45380521110908,
            -3.29883767235584,
            0.32710905363475,
            6856817.37,
        ],
        [
            -1.981981304930552e-8,
            0.000008983055099779535,
            0.03278182852591,
            40.31678527705744,
            0.65659298677277,
            -4.44255534477492,
            0.85341911805263,
            0.12923347998204,
            -0.04625736007561,
            4482777.06,
        ],
        [
            3.09191371068437e-9,
            0.000008983055096812155,
            0.00006995724062,
            23.10934304144901,
            -0.00023663490511,
            -0.6321817810242,
            -0.00663494467273,
            0.03430082397953,
            -0.00466043876332,
            2555164.4,
        ],
        [
            2.890871144776878e-9,
            0.000008983055095805407,
            -3.068298e-8,
            7.47137025468032,
            -0.00000353937994,
            -0.02145144861037,
            -0.00001234426596,
            0.00010322952773,
            -0.00000323890364,
            826088.5,
        ],
    ]

    def convertor(
        coord_dict: dict[str, float], param: list[float]
    ) -> tuple[float, float]:
        converted_lng = param[0] + param[1] * abs(coord_dict["lng"])
        base_val = abs(coord_dict["lat"]) / param[9]
        converted_lat = (
            param[2]
            + param[3] * base_val
            + param[4] * base_val * base_val
            + param[5] * base_val * base_val * base_val
            + param[6] * base_val * base_val * base_val * base_val
            + param[7] * base_val * base_val * base_val * base_val * base_val
            + param[8] * base_val * base_val * base_val * base_val * base_val * base_val
        )
        converted_lng *= -1 if coord_dict["lng"] < 0 else 1
        converted_lat *= -1 if coord_dict["lat"] < 0 else 1
        return converted_lng, converted_lat

    def convert_bd09mc_to_bd09ll(coord_dict: dict[str, float]) -> tuple[float, float]:
        abs_coord_dict = {"lng": abs(coord_dict["lng"]), "lat": abs(coord_dict["lat"])}
        param = None
        for cD in range(len(BD09MC_BAND)):
            if abs_coord_dict["lat"] >= BD09MC_BAND[cD]:
                param = BD09MC_TO_BD09LL_PARAMS[cD]
                break
        if not param:
            for cD in range(len(BD09MC_BAND) - 1, -1, -1):
                if abs_coord_dict["lat"] <= -BD09MC_BAND[cD]:
                    param = BD09MC_TO_BD09LL_PARAMS[cD]
                    break
        if not param:
            raise ValueError("param shouldn't be None")
        T = convertor(coord_dict, param)
        return T

    return convert_bd09mc_to_bd09ll({"lng": lng, "lat": lat})
