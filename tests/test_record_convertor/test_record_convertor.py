from record_convertor import RecordConvertor as RC
from record_convertor.package_settings import ConvertRecordProtocol


class BasicConvertor:
    """Basic convertor that returns input. Only for testing purposes."""

    def convert(self, record: dict) -> dict:
        return record


def test_record_convertor_class_exits():
    """Assert that RecordConvertor class exist."""
    assert RC()


def test_record_convertor_convert_method():
    """Assert that RecordConvertor convert method coverts the record."""

    class TestRC(RC):
        CONVERTOR: type[ConvertRecordProtocol] = BasicConvertor

    test_record = {"test": 1}
    assert TestRC().convert(test_record) == test_record
