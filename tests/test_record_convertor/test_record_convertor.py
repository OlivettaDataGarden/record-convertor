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


##################################
#### This skip record section ####
##################################
def test_skip_method_returns_false_if_skip_not_in_key():
    class RecordConvertorTest(RecordConvertor):
        RULE_CLASS = EmptyRuleConvertorTest

    record_convertor = RecordConvertorTest(rule_source="test")
    assert not record_convertor._skip_this_record(rule=("$NOT_SKIP", SKIP_RULE))


def test_skip_method_returns_true_if_skip_in_key_and_confition_is_true():
    class RecordConvertorTest(RecordConvertor):
        RULE_CLASS = EmptyRuleConvertorTest
        EVALUATE_CLASS = EveluateConditionsAlwaysToTrue
        _record = {}

    record_convertor = RecordConvertorTest(rule_source="test")
    assert record_convertor._skip_this_record(rule=("$SKIP", SKIP_RULE))


def test_skip_method_returns_false_if_skip_in_key_and_confition_is_false():
    class RecordConvertorTest(RecordConvertor):
        RULE_CLASS = EmptyRuleConvertorTest
        EVALUATE_CLASS = EveluateConditionsAlwaysToFalse
        _record = {}

    record_convertor = RecordConvertorTest(rule_source="test")
    assert not record_convertor._skip_this_record(rule=("$SKIP", SKIP_RULE))
