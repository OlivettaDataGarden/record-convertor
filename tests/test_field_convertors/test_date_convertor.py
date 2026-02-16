"""Module to test the field converter class from the record convertor module"""

import pytest
from data.data_date_convertor_tests import (
    BASE_PARAMS,
    BASE_PARAMS_DOTTED,
    BASE_PARAMS_NESTED_DATE_FIELD,
    BASE_PARAMS_NONE_DATE,
    BASE_PARAMS_UNIX_DT_STAMP,
    BASE_PARAMS_YYYY_MM_DD,
    BASE_PARAMS_YYYY_MM_DD_UNDERSCORE,
    BASE_PARAMS_YYYY_MM_DD_Time,
)
from record_convertor.field_convertors import DateFieldConvertor


def test_convert_yyyy_mm_dd():
    """test conversion from YYYY_DD_MM to YYYY_MM_DD success"""
    convertor = DateFieldConvertor()
    assert convertor.format_date_field(**BASE_PARAMS_YYYY_MM_DD)["date"] == "2021-02-21"  # type:ignore # NOQA: E501


def test_nested_convert_dd_mm_yyyy():
    """test conversion from DD_MM_YYYY to YYYY_MM_DD success"""
    convertor = DateFieldConvertor()
    assert (
        convertor.format_date_field(**BASE_PARAMS_NESTED_DATE_FIELD)["date"][
            "nested_date"
        ]
        == "2021-02-21"
    )


def test_convert_dd_mm_yyyy():
    """test conversion from DD_MM_YYYY to YYYY_MM_DD success"""
    convertor = DateFieldConvertor()
    assert convertor.format_date_field(**BASE_PARAMS)["date"] == "2021-02-21"  # type:ignore # NOQA: E501


def test_convert_dd_mm_yyyy_dotted():
    """test conversion from DD.MM.YYYY to YYYY_MM_DD success"""
    convertor = DateFieldConvertor()
    assert convertor.format_date_field(**BASE_PARAMS_DOTTED)["date"] == "2021-02-21"  # type:ignore # NOQA: E501


def test_convert_yyyy_mm_dd_underscore():
    """test conversion from YYYY_MM_DD to YYYY_MM_DD success"""
    convertor = DateFieldConvertor()
    assert (
        convertor.format_date_field(**BASE_PARAMS_YYYY_MM_DD_UNDERSCORE)["date"]  # type:ignore # NOQA: E501
        == "2021-02-21"
    )


def test_convert_yyyy_mm_dd_time():
    """test conversion from YYYY_MM_DD:Time to YYYY_MM_DD success"""
    convertor = DateFieldConvertor()
    assert (
        convertor.format_date_field(**BASE_PARAMS_YYYY_MM_DD_Time)["date"]  # type:ignore # NOQA: E501
        == "2021-02-21"
    )


def test_convert_unix_date_time_stamp():
    """test conversion from YYYY_MM_DD:Time to YYYY_MM_DD success"""
    convertor = DateFieldConvertor()
    assert (
        convertor.format_date_field(**BASE_PARAMS_UNIX_DT_STAMP)["date"] == "2021-02-21"  # type:ignore # NOQA: E501
    )


def test_convert_no_date_field():
    """test conversion where input field is None also returns None"""
    convertor = DateFieldConvertor()
    assert convertor.format_date_field(**BASE_PARAMS_NONE_DATE)["date"] is None


def test_format_date_field_with_condition():
    """test format_date_field with a condition that evaluates to True"""
    convertor = DateFieldConvertor()
    params = {
        "record": {"date": "21-02-2021"},
        "conversion_rule": {
            "date_field": "date",
            "format": "DD-MM-YYYY",
            "condition": {"field_does_exist": None},
        },
    }
    result = convertor.format_date_field(**params)
    assert result["date"] == "2021-02-21"


def test_format_date_field_with_false_condition():
    """test format_date_field skips conversion when condition is False"""
    convertor = DateFieldConvertor()
    params = {
        "record": {"date": "21-02-2021"},
        "conversion_rule": {
            "date_field": "date",
            "format": "DD-MM-YYYY",
            "condition": {"equals": "other_value"},
        },
    }
    result = convertor.format_date_field(**params)
    assert result["date"] == "21-02-2021"


def test_update_field_with_date_nested_missing_parent():
    """test update_field_with_date returns None when parent field is None"""
    convertor = DateFieldConvertor()
    convertor._record = {"other_field": "value"}
    convertor.date_field_key_name = "missing_parent.date"
    result = convertor.update_field_with_date("2021-02-21")
    assert result is None


def test_update_field_with_date_deeply_nested():
    """test update_field_with_date works for 3-level nesting"""
    convertor = DateFieldConvertor()
    convertor._record = {"level1": {"level2": {"date": "old_date"}}}
    convertor.date_field_key_name = "level1.level2.date"
    convertor.update_field_with_date("2021-02-21")
    assert convertor._record["level1"]["level2"]["date"] == "2021-02-21"


def test_unsupported_date_format_raises_exception():
    """test _get_date_formatter_method_name raises FormatNotImplementedException"""
    from record_convertor.package_settings import FormatNotImplementedException

    convertor = DateFieldConvertor()
    params = {
        "record": {"date": "2021-02-21"},
        "conversion_rule": {
            "date_field": "date",
            "format": "UNSUPPORTED_FORMAT",
        },
    }
    with pytest.raises(FormatNotImplementedException):
        convertor.format_date_field(**params)
