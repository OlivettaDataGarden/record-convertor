"""Tests for DataStructureConversions mixin via BaseFieldConvertor."""

from copy import deepcopy

import pytest
from record_convertor.field_convertors import BaseFieldConvertor

convertor = BaseFieldConvertor()


# --- add_data_from_dict ---

PARAMS_ADD_DATA_FROM_DICT_NONE_FIELD = {
    "record": {"source_dict": {"a": 1, "b": 2}, "target": None},
    "conversion_rule": {
        "fieldname": "target",
        "actions": [{"add_data_from_dict": "source_dict"}],
    },
}

PARAMS_ADD_DATA_FROM_DICT_MISSING_ACTION_FIELD = {
    "record": {"target": {"existing": 1}},
    "conversion_rule": {
        "fieldname": "target",
        "actions": [{"add_data_from_dict": "nonexistent_field"}],
    },
}


def test_add_data_from_dict_with_none_field_value():
    """When field_value is None, result starts empty and gets the source dict."""
    result = convertor.convert_field(**deepcopy(PARAMS_ADD_DATA_FROM_DICT_NONE_FIELD))
    assert result["target"] == {"a": 1, "b": 2}


def test_add_data_from_dict_with_missing_action_field():
    """
    When the action points to a nonexistent field, original dict is returned unchanged.
    """
    result = convertor.convert_field(
        **deepcopy(PARAMS_ADD_DATA_FROM_DICT_MISSING_ACTION_FIELD)
    )
    assert result["target"] == {"existing": 1}


# --- add_data_from_list_of_dict ---

PARAMS_LIST_OF_DICT_EMPTY_LIST = {
    "record": {"items": []},
    "conversion_rule": {
        "fieldname": "items",
        "actions": [
            {"add_data_from_list_of_dict": {"key_key": "name", "value_key": "val"}}
        ],
    },
}

PARAMS_LIST_OF_DICT_MISSING_KEYS = {
    "record": {"items": [{"name": "a", "val": 1}]},
    "conversion_rule": {
        "fieldname": "items",
        "actions": [{"add_data_from_list_of_dict": {}}],
    },
}

PARAMS_LIST_OF_DICT_VALID = {
    "record": {
        "items": [
            {"name": "width", "val": 100},
            {"name": "height", "val": 200},
        ]
    },
    "conversion_rule": {
        "fieldname": "items",
        "actions": [
            {"add_data_from_list_of_dict": {"key_key": "name", "value_key": "val"}}
        ],
    },
}


def test_add_data_from_list_of_dict_empty_list():
    """An empty list field returns an empty dict."""
    result = convertor.convert_field(**deepcopy(PARAMS_LIST_OF_DICT_EMPTY_LIST))
    assert result["items"] == {}


def test_add_data_from_list_of_dict_missing_keys():
    """Missing key_key or value_key in action_value raises KeyError."""
    with pytest.raises(KeyError):
        convertor.convert_field(**deepcopy(PARAMS_LIST_OF_DICT_MISSING_KEYS))


def test_add_data_from_list_of_dict_valid():
    """Valid list of dicts is converted into a single dict."""
    result = convertor.convert_field(**deepcopy(PARAMS_LIST_OF_DICT_VALID))
    assert result["items"] == {"width": 100, "height": 200}


# --- convert_data_from_html_fragment_to_list ---

PARAMS_HTML_FRAGMENT_NONE = {
    "record": {"html": None},
    "conversion_rule": {
        "fieldname": "html",
        "actions": [{"convert_data_from_html_fragment_to_list": None}],
    },
}

PARAMS_HTML_FRAGMENT_VALID = {
    "record": {"html": "<p>first</p><p>second</p>"},
    "conversion_rule": {
        "fieldname": "html",
        "actions": [{"convert_data_from_html_fragment_to_list": None}],
    },
}


def test_convert_data_from_html_fragment_to_list_none():
    """A None field returns an empty list."""
    result = convertor.convert_field(**deepcopy(PARAMS_HTML_FRAGMENT_NONE))
    assert result["html"] == []


def test_convert_data_from_html_fragment_to_list_valid():
    """HTML fragment is parsed into a list of text items."""
    result = convertor.convert_field(**deepcopy(PARAMS_HTML_FRAGMENT_VALID))
    assert result["html"] == ["first", "second"]
