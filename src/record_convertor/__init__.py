"""
Module to define record conversion functionality.

Classes:
    - RecordConverter: Public class to be used to convert records based upon
                       provide rules.

usage:
>>> converted_record: dict = \
>>>     RecordConvertor(rules: Rules).convert(record: dict)
"""

from typing import Any

import jmespath
from jmespath.exceptions import ParseError

from .package_settings import (
    ConvertRecordProtocol,
    EvaluateConditions,
    keys_in_lower_case,
    RecConvKeys,
    SkipConvKeys,
    SkipRuleDict,
)
from .rules_generator import RulesFromYAML


class RecordConvertor:
    RULE_CLASS = RulesFromYAML
    CONVERTOR: type[ConvertRecordProtocol]
    EVALUATE_CLASS = EvaluateConditions
    KEYS_IN_LOWER_CASE: bool = False
    DEFAULT_VALUE: dict = {}

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
        self._record = keys_in_lower_case(record) if self.KEYS_IN_LOWER_CASE else record
        for rule in self._rules.items():
            if self._skip_this_record(rule):
                return self.DEFAULT_VALUE

        return record

    def _skip_this_record(self, rule: tuple) -> bool:
        rule_key, rule_value = rule
        if not rule_key.lower() == RecConvKeys.SKIP:
            return False
        skip_rule: SkipRuleDict = rule_value
        conditions = skip_rule.get(SkipConvKeys.CONDITION)
        fieldname = skip_rule.get(SkipConvKeys.FIELDNAME)
        field_value = self._get_field(fieldname)

        return (
            True if self.EVALUATE_CLASS(conditions, field_value).evaluate() else False
        )

    def _get_field(self, key: str) -> Any:
        if key:
            # key elemenets in nested keys are surround with "". For exmample
            # key.example-1 becomes "key"."example-1".
            # Needed for jmespath can hande special characters in the keys
            nested_keys = key.split(".")
            nested_key = ".".join(['"' + key + '"' for key in nested_keys])
            try:
                return jmespath.search(nested_key, self._record)
            except ParseError:
                pass

        return None
