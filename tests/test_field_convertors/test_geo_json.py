"""Tests for the geo_json helper module."""

import pytest

from record_convertor.command_processor.command_helper.geo_json import (
    _operate,
    lat_lon_to_geojson_point,
)


def test_basic_conversion():
    """Valid lat/lon produces a GeoJSON Point dict."""
    result = lat_lon_to_geojson_point(52.37403, 4.88969)
    assert result == {
        "type": "Point",
        "coordinates": [4.88969, 52.37403],
    }


def test_with_divide_operator():
    """The divide operator divides lat/lon by the specified value."""
    result = lat_lon_to_geojson_point(52374, 4889, operator="divide_1000")
    assert result["type"] == "Point"
    assert result["coordinates"][0] == round(4889 / 1000, 5)
    assert result["coordinates"][1] == round(52374 / 1000, 5)


def test_invalid_lat_lon_strings():
    """Non-numeric strings return None."""
    assert lat_lon_to_geojson_point("abc", "def") is None


def test_none_latitude():
    """None latitude returns None."""
    assert lat_lon_to_geojson_point(None, 4.88969) is None


def test_none_longitude():
    """None longitude returns None."""
    assert lat_lon_to_geojson_point(52.37403, None) is None


def test_custom_digits():
    """The digits parameter controls rounding precision."""
    result = lat_lon_to_geojson_point(52.123456789, 4.123456789, digits=3)
    assert result["coordinates"] == [4.123, 52.123]


def test_string_numeric_values():
    """Numeric strings are converted successfully."""
    result = lat_lon_to_geojson_point("52.37403", "4.88969")
    assert result == {
        "type": "Point",
        "coordinates": [4.88969, 52.37403],
    }


def test_operate_divide():
    """_operate with divide operator divides by the given value."""
    assert _operate(1000, "divide_10") == 100.0


def test_operate_unknown_operator():
    """_operate with an unknown operator raises ValueError."""
    with pytest.raises(ValueError, match="Unkown operator"):
        _operate(100, "multiply_10")
