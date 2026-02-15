"""Tests for custom exception classes."""

from record_convertor.package_settings.exceptions import (
    FormatNotImplementedException,
    NoDateFieldException,
    ProcessArgsMustBeOfTypeDict,
    ProcessArgsMustBeOfTypeList,
)


def test_process_args_must_be_of_type_list():
    """ProcessArgsMustBeOfTypeList message contains 'list'."""
    exc = ProcessArgsMustBeOfTypeList("bad_arg")
    assert "list" in str(exc)


def test_process_args_must_be_of_type_dict():
    """ProcessArgsMustBeOfTypeDict message contains 'dict'."""
    exc = ProcessArgsMustBeOfTypeDict("bad_arg")
    assert "dict" in str(exc)


def test_format_not_implemented_exception():
    """FormatNotImplementedException message includes the format string."""
    exc = FormatNotImplementedException("CUSTOM_FORMAT")
    assert "CUSTOM_FORMAT" in str(exc)


def test_no_date_field_exception():
    """NoDateFieldException message contains 'dateformat'."""
    exc = NoDateFieldException()
    assert "dateformat" in str(exc)
