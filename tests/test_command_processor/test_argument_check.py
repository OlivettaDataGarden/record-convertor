"""Tests for argument_check helper functions."""

import pytest
from record_convertor.command_processor.command_helper.argument_check import (
    process_args_is_dict,
    process_args_is_list,
)
from record_convertor.package_settings import (
    ProcessArgsMustBeOfTypeDict,
    ProcessArgsMustBeOfTypeList,
)


def test_process_args_is_list_with_valid_list():
    """A valid list is returned as-is."""
    result = process_args_is_list([1, 2, 3])
    assert result == [1, 2, 3]


def test_process_args_is_list_with_non_list():
    """A non-list argument raises ProcessArgsMustBeOfTypeList."""
    with pytest.raises(ProcessArgsMustBeOfTypeList):
        process_args_is_list("not a list")


def test_process_args_is_dict_with_valid_dict():
    """A valid dict is returned as-is."""
    result = process_args_is_dict({"key": "value"})
    assert result == {"key": "value"}


def test_process_args_is_dict_with_non_dict():
    """A non-dict argument raises ProcessArgsMustBeOfTypeDict."""
    with pytest.raises(ProcessArgsMustBeOfTypeDict):
        process_args_is_dict([1, 2])
