from record_convertor import RecordConvertor


TEST_RULES = {'rule1': 'test'}

class RuleConvertorTest():
    RULE_SOURCE_TYPE = str

    def __init__(self, rule_source: RULE_SOURCE_TYPE):
        ...

    @property
    def rules(self) -> dict:
        return TEST_RULES


class RecordConvertorTest(RecordConvertor) :
    """Basic convertor that returns input. Only for testing purposes."""
    RULE_CLASS = RuleConvertorTest
    

def test_record_convertor_class_exits():
    """Tests the existence of the `RecordConvertor` class to ensure it is correctly defined and importable."""
    assert RecordConvertor


def test_record_sets_rules_source():
    """Tests that the `RecordConvertorTest` class correctly sets and utilizes the `_rules` attribute."""
    assert RecordConvertorTest(rule_source="test")._rules == TEST_RULES
