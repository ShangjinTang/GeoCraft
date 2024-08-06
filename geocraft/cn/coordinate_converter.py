"""
coordinate_converter.py

This module provides functions for converting coordinates between different coordinate systems commonly used in mapping applications.

Coordinate Systems:
- BD09: Coordinates used by [Baidu Map](https://map.baidu.com/).
- GCJ02: Coordinates used by [Amap](https://ditu.amap.com/) and [Tencent Map](https://map.qq.com/).
- WGS84: Standard GPS coordinates.

"""

import math

x_PI: float = 3.14159265358979324 * 3000.0 / 180.0
PI: float = 3.1415926535897932384626
a: float = 6378245.0
ee: float = 0.00669342162296594323


def bd09_to_gcj02(lng: float, lat: float) -> tuple[float, float]:
    lng = float(lng)
    lat = float(lat)
    x: float = lng - 0.0065
    y: float = lat - 0.006
    z: float = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_PI)
    theta: float = math.atan2(y, x) - 0.000003 * math.cos(x * x_PI)
    gg_lng: float = z * math.cos(theta)
    gg_lat: float = z * math.sin(theta)
    return gg_lng, gg_lat


def gcj02_to_bd09(lng: float, lat: float) -> tuple[float, float]:
    lat = float(lat)
    lng = float(lng)
    z: float = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_PI)
    theta: float = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_PI)
    bd_lng: float = z * math.cos(theta) + 0.0065
    bd_lat: float = z * math.sin(theta) + 0.006
    return bd_lng, bd_lat


def wgs84_to_gcj02(lng: float, lat: float) -> tuple[float, float]:
    lat = float(lat)
    lng = float(lng)
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
    lat = float(lat)
    lng = float(lng)
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
