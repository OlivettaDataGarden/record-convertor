"""Tests for the RulesFromDict class."""

import pytest

from record_convertor.rules_generator.from_dict import RulesFromDict


def test_type_error_on_string_input():
    """Passing a string to RulesFromDict raises TypeError."""
    with pytest.raises(TypeError, match="rule_source not of type"):
        RulesFromDict("not a dict")


def test_type_error_on_int_input():
    """Passing an int to RulesFromDict raises TypeError."""
    with pytest.raises(TypeError, match="rule_source not of type"):
        RulesFromDict(42)


def test_valid_dict():
    """A valid dict is stored and returned via the rules property."""
    rules_input = {"output_field": {"field": "input_field"}}
    result = RulesFromDict(rules_input)
    assert result.rules == rules_input


def test_empty_dict():
    """An empty dict is accepted and returned via the rules property."""
    result = RulesFromDict({})
    assert result.rules == {}


def test_error_property_raises_value_error():
    """When _error is set, accessing rules raises ValueError."""
    rules = RulesFromDict({"key": "value"})
    rules._error = "forced error"
    with pytest.raises(ValueError, match="error"):
        rules.rules
