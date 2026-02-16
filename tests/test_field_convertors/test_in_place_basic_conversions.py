"""Tests for InPlaceBasicConversions mixin via BaseFieldConvertor."""

from copy import deepcopy

from record_convertor.field_convertors import BaseFieldConvertor

convertor = BaseFieldConvertor()


# --- _get_float_from_field_value (via divide_by) with non-numeric type ---

PARAMS_DIVIDE_BY_LIST = {
    "record": {"val": [1, 2, 3]},
    "conversion_rule": {
        "fieldname": "val",
        "actions": [{"divide_by": 10}],
    },
}


def test_divide_by_with_list_field_value():
    """A list field value causes _get_float_from_field_value to return None."""
    result = convertor.convert_field(**deepcopy(PARAMS_DIVIDE_BY_LIST))
    assert result["val"] is None


# --- round ---

PARAMS_ROUND_ZERO = {
    "record": {"val": 1.7},
    "conversion_rule": {
        "fieldname": "val",
        "actions": [{"round": 0}],
    },
}

PARAMS_ROUND_TWO = {
    "record": {"val": 1.567},
    "conversion_rule": {
        "fieldname": "val",
        "actions": [{"round": 2}],
    },
}

PARAMS_ROUND_NONE = {
    "record": {"val": None},
    "conversion_rule": {
        "fieldname": "val",
        "actions": [{"round": 2}],
    },
}


def test_round_with_action_value_zero():
    """Round with action_value=0 returns an int (not float like 2.0)."""
    result = convertor.convert_field(**deepcopy(PARAMS_ROUND_ZERO))
    assert result["val"] == 2
    assert isinstance(result["val"], int)


def test_round_with_action_value_two():
    """Round with action_value=2 returns a float rounded to 2 decimals."""
    result = convertor.convert_field(**deepcopy(PARAMS_ROUND_TWO))
    assert result["val"] == 1.57


def test_round_with_none_field():
    """Round with None field returns None."""
    result = convertor.convert_field(**deepcopy(PARAMS_ROUND_NONE))
    assert result["val"] is None


# --- str_to_dict ---

PARAMS_STR_TO_DICT_NONE = {
    "record": {"data": None},
    "conversion_rule": {
        "fieldname": "data",
        "actions": [{"str_to_dict": None}],
    },
}


def test_str_to_dict_with_none_field():
    """str_to_dict with None field returns empty dict."""
    result = convertor.convert_field(**deepcopy(PARAMS_STR_TO_DICT_NONE))
    assert result["data"] == {}


# --- remove_params_from_url ---

PARAMS_REMOVE_URL_NON_STRING = {
    "record": {"url": 12345},
    "conversion_rule": {
        "fieldname": "url",
        "actions": [{"remove_params_from_url": None}],
    },
}


def test_remove_params_from_url_with_non_string():
    """remove_params_from_url with a non-string field returns None."""
    result = convertor.convert_field(**deepcopy(PARAMS_REMOVE_URL_NON_STRING))
    assert result["url"] is None


# --- string_begin ---

PARAMS_STRING_BEGIN_VALID = {
    "record": {"text": "hello world"},
    "conversion_rule": {
        "fieldname": "text",
        "actions": [{"string_begin": 5}],
    },
}

PARAMS_STRING_BEGIN_NON_STRING = {
    "record": {"text": 12345},
    "conversion_rule": {
        "fieldname": "text",
        "actions": [{"string_begin": 3}],
    },
}


def test_string_begin_with_valid_string():
    """string_begin returns the first N characters of the string."""
    result = convertor.convert_field(**deepcopy(PARAMS_STRING_BEGIN_VALID))
    assert result["text"] == "hello"


def test_string_begin_with_non_string():
    """string_begin with a non-string field returns None."""
    result = convertor.convert_field(**deepcopy(PARAMS_STRING_BEGIN_NON_STRING))
    assert result["text"] is None
