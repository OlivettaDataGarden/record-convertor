"""
Module to define record conversion functionality.

Classes:
    - RecordConverter: Public class to be used to convert records based upon
                       provide rules.

usage:
>>> converted_record: dict = \
>>>     RecordConvertor(rules: Rules).convert(record: dict)
"""

from typing import Any, Optional

import jmespath
from jmespath.exceptions import ParseError

from .package_settings import (
    EvaluateConditions,
    keys_in_lower_case,
    RecConvKeys,
    SkipConvKeys,
    SkipRuleDict,
    FieldConvertorProtocol,
    DateFormatProtocol
)
from .rules_generator import RulesFromYAML

from .field_convertors import BaseFieldConvertor, DateFieldConvertor


class RecordConvertor:
    RULE_CLASS = RulesFromYAML
    EVALUATE_CLASS = EvaluateConditions
    KEYS_IN_LOWER_CASE: bool = False
    DEFAULT_VALUE: dict = {}
    DEFAULT_FIELD_CONVERTOR_CLASS: type[FieldConvertorProtocol] = BaseFieldConvertor
    DEFAULT_DATE_FORMAT_CLASS: type[DateFormatProtocol] = DateFieldConvertor


    def __init__(
        self,
        rule_source: RULE_CLASS.RULE_SOURCE_TYPE,
        field_convertor: Optional[type[FieldConvertorProtocol]] = None,
        date_formatter: Optional[type[DateFormatProtocol]] = None 
    ):
        self._rules = self.RULE_CLASS(rule_source=rule_source).rules
        # set instance of given or default field convertor class
        self._field_convertor: FieldConvertorProtocol = \
            (field_convertor or self.DEFAULT_FIELD_CONVERTOR_CLASS)()
        # set instance of given or default date format class
        self._date_formatter: DateFormatProtocol = \
            (date_formatter or self.DEFAULT_DATE_FORMAT_CLASS)()

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
            # check if the rule determines that the given record can be skipped
            if self._skip_this_record(rule):
                return self.DEFAULT_VALUE

            # check if the rule triggers a field conversion in the input record
            if self._convert_field_rule(rule):
                _, rule_dict = rule
                self._record = self._field_convertor.convert_field(
                    record=self._record, conversion_rule=rule_dict
                )
                continue

            # check if the rule triggers a field date conversion in the input record
            if self._format_date_rule(rule):
                _, rule_dict = rule
                self._record = self._date_formatter.format_date_field(
                    record=self._record, conversion_rule=rule_dict
                )
                continue

        return record

    def _convert_field_rule(self, rule: tuple) -> bool:
        rule_key, _ = rule
        return "$convert" in rule_key

    def _format_date_rule(self, rule: tuple) -> bool:
        rule_key, _ = rule
        return "$format_date" in rule_key

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

    def _get_field(self, key: Optional[str]) -> Any:
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
