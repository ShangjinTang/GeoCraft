import json

import requests

from ..coord_converter import CoordConverter
from ..coord_type import CoordType

bd09mc_to_bd09_converter = CoordConverter(src=CoordType.BD09MC, target=CoordType.BD09)
bd09_to_wgs84_converter = CoordConverter(src=CoordType.BD09, target=CoordType.WGS84)


def fetch_json_data(url, retries=3):
    for _ in range(retries):
        response = requests.get(url)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print(f"Connection error code {response.status_code} with url: {url}")
    return None


def parse_polygon(uid):
    def get_data_by_uid(uid: str):
        return f"https://map.baidu.com/?newmap=1&qt=ext&uid={uid}&ext_ver=new&ie=utf-8&l=11"

    url = get_data_by_uid(uid)
    data = fetch_json_data(url)

    if data:
        geo_data = data.get("content", {}).get("geo", None)
        if geo_data:
            points_bd09mc = geo_data.split("|")[-1].split("-")[-1][:-1].split(",")
            if len(points_bd09mc) % 2 != 0:
                print("geo polygon data is not in pairs")
                return
            points_wgs84 = []
            for i in range(int(len(points_bd09mc) / 2)):
                bd09mc_lng, bd09mc_lat = float(points_bd09mc[2 * i]), float(
                    points_bd09mc[2 * i + 1]
                )
                bd09_lng, bd09_lat = bd09mc_to_bd09_converter.convert(
                    bd09mc_lng, bd09mc_lat
                )
                wgs84_lng, wgs84_lat = bd09_to_wgs84_converter.convert(
                    bd09_lng, bd09_lat
                )
                points_wgs84.append([wgs84_lng, wgs84_lat])

            return points_wgs84

    else:
        print(f"Connection error to {url}")
        return


def parse_geojson(uid):
    points_wgs84 = parse_polygon(uid)
    geojson_dict = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {"coordinates": [points_wgs84], "type": "Polygon"},
            }
        ],
    }
    return json.dumps(geojson_dict)
