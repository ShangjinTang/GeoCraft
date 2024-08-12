import pytest

from geocraft import CoordConverter, CoordType


def test_convert_from_bd09():
    converter = CoordConverter(src=CoordType.BD09, target=CoordType.GCJ02)
    assert converter.convert(116.404, 39.915) == (116.39762729119315, 39.90865673957631)


def test_coordconverter_2():
    converter = CoordConverter(src=CoordType.BD09, target=CoordType.WGS84)
    assert converter.convert(116.404, 39.915) == (116.3913836995125, 39.907253214522164)


def test_coordconverter_3():
    converter = CoordConverter(src=CoordType.GCJ02, target=CoordType.BD09)
    assert converter.convert(116.404, 39.915) == (116.41036949371029, 39.92133699351021)


def test_coordconverter_4():
    converter = CoordConverter(src=CoordType.GCJ02, target=CoordType.WGS84)
    assert converter.convert(116.404, 39.915) == (116.39775550083061, 39.91359571849836)


def test_coordconverter_5():
    converter = CoordConverter(src=CoordType.WGS84, target=CoordType.BD09)
    assert converter.convert(116.404, 39.915) == (
        116.41662724378733,
        39.922699552216216,
    )


def test_coordconverter_6():
    converter = CoordConverter(src=CoordType.WGS84, target=CoordType.GCJ02)
    assert converter.convert(116.404, 39.915) == (116.41024449916938, 39.91640428150164)


def test_coordconverter_unsupported():
    for coord_type in [
        CoordType.WGS84,
        CoordType.WGS84MC,
        CoordType.GCJ02,
        CoordType.GCJ02MC,
        CoordType.BD09,
        CoordType.BD09MC,
    ]:
        converter = CoordConverter(src=coord_type, target=coord_type)
        with pytest.raises(RuntimeError):
            converter.convert(116.404, 39.915)
