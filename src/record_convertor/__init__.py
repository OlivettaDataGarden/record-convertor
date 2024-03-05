"""
Module to define record conversion functionality.

Classes:
    - RecordConverter: Public class to be used to convert records based upon
                       provide rules.

usage:
>>> converted_record: dict = \
>>>     RecordConvertor(rules: Rules).convert(record: dict)
"""

from .package_settings import ConvertRecordProtocol
from .rules_generator import RulesFromYAML


class RecordConvertor:
    RULE_CLASS = RulesFromYAML
    CONVERTOR: type[ConvertRecordProtocol]

    def __init__(self, rule_source: RULE_CLASS.RULE_SOURCE_TYPE):
        self._rules = self.RULE_CLASS(rule_source=rule_source).rules

    def convert(self, record: dict) -> dict:
        """
        Primary public method to run the actual conversion of the record.

        Args:
            record (dict): input record

        Returns:
            dict: converted record
        """
        ...