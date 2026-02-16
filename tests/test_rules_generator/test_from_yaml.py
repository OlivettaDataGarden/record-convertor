"""Tests for the RulesFromYAML class."""

import pytest

from record_convertor.rules_generator.from_yaml import RulesFromYAML


def test_type_error_on_non_string_input():
    """Passing a non-string (dict) to RulesFromYAML raises TypeError."""
    with pytest.raises(TypeError, match="rule_source not of type"):
        RulesFromYAML({"key": "value"})


def test_type_error_on_int_input():
    """Passing an int to RulesFromYAML raises TypeError."""
    with pytest.raises(TypeError, match="rule_source not of type"):
        RulesFromYAML(42)


def test_valid_yaml_file(tmp_path):
    """A valid YAML file is parsed and returned as a dict via the rules property."""
    yaml_file = tmp_path / "rules.yaml"
    yaml_file.write_text("output_field:\n  field: input_field\n")

    result = RulesFromYAML(str(yaml_file))
    assert result.rules == {"output_field": {"field": "input_field"}}


def test_invalid_yaml_syntax(tmp_path):
    """Malformed YAML sets _error and rules property raises ValueError."""
    yaml_file = tmp_path / "bad.yaml"
    yaml_file.write_text("key: value\n\tbad_indent: value\n")

    result = RulesFromYAML(str(yaml_file))
    assert result._error
    with pytest.raises(ValueError, match="error"):
        result.rules


def test_filename_property(tmp_path):
    """The _filename property returns the rule_source string."""
    yaml_file = tmp_path / "rules.yaml"
    yaml_file.write_text("key: value\n")

    path_str = str(yaml_file)
    result = RulesFromYAML(path_str)
    assert result._filename == path_str


def test_file_not_found():
    """A non-existent file path raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        RulesFromYAML("/nonexistent/path/rules.yaml")
