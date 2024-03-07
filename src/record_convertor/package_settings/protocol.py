from typing import Protocol

from .package_types import BaseRuleDict

__all__ = ["ConvertRecordProtocol", "FieldConvertorProtocol"]


class ConvertRecordProtocol(Protocol):
    def convert(self, record: dict) -> dict: ...


class FieldConvertorProtocol(Protocol):
    def __init__(self, record: dict, conversion_rule: BaseRuleDict): ...
    def convert_field(self) -> dict: ...
