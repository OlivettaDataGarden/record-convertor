from typing import Protocol

from .package_types import BaseRuleDict

__all__ = ["RecordConvertorProtocol", "FieldConvertorProtocol"]


class RecordConvertorProtocol(Protocol):
    def convert(self, record: dict) -> dict: ...


class FieldConvertorProtocol(Protocol):
    def convert_field(self, record: dict, conversion_rule: BaseRuleDict) -> dict: ...
