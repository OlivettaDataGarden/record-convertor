import jmespath
import pytest

from jmespath.exceptions import ParseError
from record_convertor import RecordConvertor, EvaluateConditions

TEST_RULES = {"rule1": "test"}
SKIP_RULE = {"fieldname": "field1", "condition": {"does_not_equal": "test"}}


class EveluateConditionsAlwaysToTrue(EvaluateConditions):
    def evaluate(self) -> bool:
        return True


class EveluateConditionsAlwaysToFalse(EvaluateConditions):
    def evaluate(self) -> bool:
        return False


class RuleConvertorTest:
    RULE_SOURCE_TYPE = str
    DEFAULT_RULE = TEST_RULES

    def __init__(self, rule_source: RULE_SOURCE_TYPE): ...

    @property
    def rules(self) -> dict:
        return self.DEFAULT_RULE


class EmptyRuleConvertorTest(RuleConvertorTest):
    DEFAULT_RULE = {}


def basic_test_convertor() -> RecordConvertor:
    class RecordConvertorTest(RecordConvertor):
        RULE_CLASS = EmptyRuleConvertorTest
        EVALUATE_CLASS = EveluateConditionsAlwaysToTrue
        _record = {}

    return RecordConvertorTest(rule_source="test")


def test_get_field_method_returns_correct_value():
    class RecordConvertorTest(RecordConvertor):
        RULE_CLASS = RuleConvertorTest
        _record = {"test_key": "test_value"}

    rc = RecordConvertorTest(rule_source="test")
    assert rc._get_field("test_key") == "test_value"


def test_get_field_method_returns_correct_nested_field_value():
    class RecordConvertorTest(RecordConvertor):
        RULE_CLASS = RuleConvertorTest
        _record = {"test_key": {"nested_key": "nested_test_value"}}

    rc = RecordConvertorTest(rule_source="test")
    assert rc._get_field("test_key.nested_key") == "nested_test_value"


def test_get_field_method_returns_none_if_field_not_found():
    class RecordConvertorTest(RecordConvertor):
        RULE_CLASS = RuleConvertorTest
        _record = {"test_key": {"nested_key": "nested_test_value"}}

    rc = RecordConvertorTest(rule_source="test")
    assert rc._get_field("non_existing_field") is None


def test_get_field_method_returns_none_if_None_key_is_provided():
    class RecordConvertorTest(RecordConvertor):
        RULE_CLASS = RuleConvertorTest
        _record = {"test_key": {"nested_key": "nested_test_value"}}

    rc = RecordConvertorTest(rule_source="test")
    assert rc._get_field(key=None) is None


def test_get_field_method_fixes_parse_error_with_int_keys_as_str():
    class RecordConvertorTest(RecordConvertor):
        RULE_CLASS = RuleConvertorTest
        _record = {"1": "test_value"}

    with pytest.raises(ParseError):
        jmespath.search("1", RecordConvertorTest._record)

    rc = RecordConvertorTest(rule_source="test")
    assert rc._get_field(key="1") == "test_value"


#############################################
#### Test the _convert_field_rule method ####
#############################################


def test_convert_field_rule_method_returns_false_when_convert_not_in_rule_key():
    assert not basic_test_convertor()._convert_field_rule(("$do_not_convert", "test"))


def test_convert_field_rule_method_returns_true_when_convert_in_rule_key():
    assert basic_test_convertor()._convert_field_rule(("$convert1", "test"))


#############################################
#### Test the _convert_field_rule method ####
#############################################


def test_format_date_rule_method_returns_false_when_convert_not_in_rule_key():
    assert not basic_test_convertor()._format_date_rule(("$do_not_format_date", "test"))


def test_format_date_rule_method_returns_true_when_convert_in_rule_key():
    assert basic_test_convertor()._format_date_rule(("$format_date", "test"))
