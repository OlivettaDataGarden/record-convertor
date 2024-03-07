from typing import Optional
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


def basic_test_convertor(
        rule_class: type[RuleConvertorTest] = RuleConvertorTest,
        evaluate_class: type[EvaluateConditions] = EveluateConditionsAlwaysToTrue,
) -> RecordConvertor:
    class RecordConvertorTest(RecordConvertor):
        RULE_CLASS = rule_class
        EVALUATE_CLASS = evaluate_class
        _record = {}

    return RecordConvertorTest(rule_source="test")


def test_record_convertor_class_exits():
    """Tests the existence of the `RecordConvertor` class to ensure it is correctly defined and importable."""
    assert RecordConvertor


def test_record_convertor_sets_rules_source():
    """Tests that instances (subclasses of) `RecordConvertor` class correctly sets and utilizes the `_rules` attribute."""
    record_covertor = basic_test_convertor(rule_class=RuleConvertorTest)
    assert isinstance(record_covertor, RecordConvertor)
    assert basic_test_convertor()._rules == RuleConvertorTest(rule_source="").rules


def test_record_convertor_sets_field_convertor():
    """Tests that the `RecordConvertorTest` class correctly sets and utilizes the `_rules` attribute."""

    class TestFieldConvertor: ...

    class RecordConvertorTest(RecordConvertor):
        RULE_CLASS = RuleConvertorTest
        DEFAULT_FIELD_CONVERTOR_CLASS: type[TestFieldConvertor] = TestFieldConvertor

    assert isinstance(
        RecordConvertorTest(rule_source="test")._field_convertor, TestFieldConvertor
    )


######################################################
#### Test the set record keys to lower case logic ####
######################################################


def test_record_convert_sets_keys_to_lower_case():
    class RecordConvertorTest(RecordConvertor):
        RULE_CLASS = EmptyRuleConvertorTest
        KEYS_IN_LOWER_CASE = True

    record_convertor = RecordConvertorTest(rule_source="test")
    test_record = {"KEY1": 1}
    record_convertor.convert(record=test_record)
    assert record_convertor._record == {"key1": 1}


def test_record_convert_does_not_set_keys_to_lower_case_by_default():
    record_convertor = basic_test_convertor(rule_class=EmptyRuleConvertorTest)
    test_record = {"KEY1": 1}
    record_convertor.convert(record=test_record)
    assert record_convertor._record == {"KEY1": 1}


####################################
#### Test the skip record logic ####
####################################


def test_skip_method_returns_false_if_skip_not_in_key():
    record_convertor = basic_test_convertor(rule_class=EmptyRuleConvertorTest)
    assert not record_convertor._skip_this_record(rule=("$NOT_SKIP", SKIP_RULE))


def test_skip_method_returns_true_if_skip_in_key_and_confition_is_true():
    record_convertor = basic_test_convertor(rule_class=EmptyRuleConvertorTest)
    assert record_convertor._skip_this_record(rule=("$SKIP", SKIP_RULE))


def test_skip_method_returns_false_if_skip_in_key_and_confition_is_false():
    record_convertor = basic_test_convertor(rule_class=EmptyRuleConvertorTest)
    record_convertor.__class__.EVALUATE_CLASS = EveluateConditionsAlwaysToFalse
    assert not record_convertor._skip_this_record(rule=("$SKIP", SKIP_RULE))
