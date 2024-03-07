from typing import Protocol

from .package_types import BaseRuleDict, FormatDateRuleDict

__all__ = ["RecordConvertorProtocol", "FieldConvertorProtocol", "DateFormatProtocol"]


class RecordConvertorProtocol(Protocol):
    def convert(self, record: dict) -> dict: ...


class FieldConvertorProtocol(Protocol):
    def convert_field(self, record: dict, conversion_rule: BaseRuleDict) -> dict: ...


class DateFormatProtocol(Protocol):
    def format_date_field(
        self, record: dict, conversion_rule: FormatDateRuleDict
    ) -> dict: ...
