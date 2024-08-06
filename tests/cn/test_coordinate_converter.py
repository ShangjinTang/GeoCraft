from coordinate_converter import (bd09_to_gcj02, gcj02_to_bd09, gcj02_to_wgs84,
                                  wgs84_to_gcj02)


def test_bd09_to_gcj02():
    assert bd09_to_gcj02(116.404, 39.915) == (116.39762729119315, 39.90865673957631)


def test_gcj02_to_bd09():
    assert gcj02_to_bd09(116.404, 39.915) == (116.41036949371029, 39.92133699351021)


def test_wgs84_to_gcj02():
    assert wgs84_to_gcj02(116.404, 39.915) == (116.41024449916938, 39.91640428150164)


def test_gcj02_to_wgs84():
    assert gcj02_to_wgs84(116.404, 39.915) == (116.39775550083061, 39.91359571849836)
