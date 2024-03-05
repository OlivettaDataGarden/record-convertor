from record_convertor import RecordConvertor

TEST_RULES = {"rule1": "test"}


class RuleConvertorTest:
    RULE_SOURCE_TYPE = str
    DEFAULT_RULE = TEST_RULES

    def __init__(self, rule_source: RULE_SOURCE_TYPE): ...

    @property
    def rules(self) -> dict:
        return self.DEFAULT_RULE


class EmptyRuleConvertorTest(RuleConvertorTest):
    DEFAULT_RULE = {}


def test_record_convertor_class_exits():
    """Tests the existence of the `RecordConvertor` class to ensure it is correctly defined and importable."""
    assert RecordConvertor


def test_record_sets_rules_source():
    """Tests that the `RecordConvertorTest` class correctly sets and utilizes the `_rules` attribute."""

    class RecordConvertorTest(RecordConvertor):
        RULE_CLASS = RuleConvertorTest

    assert RecordConvertorTest(rule_source="test")._rules == TEST_RULES


def test_record_convert_sets_keys_to_lower_case():
    class RecordConvertorTest(RecordConvertor):
        RULE_CLASS = EmptyRuleConvertorTest
        KEYS_IN_LOWER_CASE = True

    record_convertor = RecordConvertorTest(rule_source="test")
    test_record = {"KEY1": 1}
    record_convertor.convert(record=test_record)
    assert record_convertor._record == {"key1": 1}


def test_record_convert_does_not_set_keys_to_lower_case_by_default():
    class RecordConvertorTest(RecordConvertor):
        RULE_CLASS = EmptyRuleConvertorTest

    record_convertor = RecordConvertorTest(rule_source="test")
    test_record = {"KEY1": 1}
    record_convertor.convert(record=test_record)
    assert record_convertor._record == {"KEY1": 1}
