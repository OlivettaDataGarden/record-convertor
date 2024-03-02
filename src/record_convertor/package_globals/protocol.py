from typing import Protocol

__all__ = ["ConvertRecordProtocol"]


class ConvertRecordProtocol(Protocol):
    def convert(self, record: dict) -> dict: ...
