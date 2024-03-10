import pytest
from dataclasses import dataclass
from copy import deepcopy
from record_convertor.dataclass_processor import DataClassProcessor
from record_convertor.package_settings import DataClassRuleKeys, DataClassRuleDict


@dataclass
class DataClassTest: ...


@dataclass
class DataClassTestTwo: ...


base_data_class_rule: DataClassRuleDict = {
    DataClassRuleKeys.NAME: "data_class_name",
    DataClassRuleKeys.RECORD_CONVERSION_ARGUMENTS: {"field1": "field2"},
    DataClassRuleKeys.METHODS: [
        {"rule_key1": "rule_value1", "rule_key2": "rule_value2"}
    ],
}


def test_dataclass_processor_class_exists():
    assert DataClassProcessor()


def test_dataclass_processor_raises_exception_for_non_dataclass():
    class TestClass: ...

    with pytest.raises(ValueError):
        DataClassProcessor().register_dataclass(TestClass)


def test_private_register_dataclass_method_adds_a_dataclass_to_the_class():
    """
    Test the private method _register_dataclass adds an attribute holding the
    dataclass to the dataclass processor.
    """
    data_class_processor = DataClassProcessor()
    data_class_processor._register_dataclass("test_class", DataClassTest)
    assert "test_class" in dir(data_class_processor)
    assert getattr(data_class_processor, "test_class") is DataClassTest


def test_register_dataclass_method_adds_an_attribute_in_snake_case_holding_the_dataclass_processor():
    """
    Test the public method register_dataclass adds a dataclass as an attribute to the dataclass
    processor where the attribute name is the same as the added dataclass name but then in snakecase.
    """
    data_class_processor = DataClassProcessor()
    data_class_processor.register_dataclass(DataClassTest)
    assert "data_class_test" in dir(data_class_processor)
    assert getattr(data_class_processor, "data_class_test") is DataClassTest


def test_register_data_classes_method_adds_multiple_attributes():
    """
    Test the public method register_data_classes adds multiple given
    dataclasses as attributes to the dataclass processor each with
    their own snake_case attribute name.
    """
    data_class_processor = DataClassProcessor()
    data_class_processor.register_data_classes([DataClassTest, DataClassTestTwo])
    assert "data_class_test" in dir(data_class_processor)
    assert "data_class_test_two" in dir(data_class_processor)
    assert getattr(data_class_processor, "data_class_test") is DataClassTest
    assert getattr(data_class_processor, "data_class_test_two") is DataClassTestTwo


def test_register_dict_of_data_classes_method():
    """
    Test the public method register_dict_of_data_classes adds
    multiple given dataclasses as attributes to the dataclass
    processor each with dict their key as attribute name.
    """
    dict_of_data_classes = {
        "dataclassone": DataClassTest,
        "datackasstwo": DataClassTestTwo,
    }

    data_class_processor = DataClassProcessor()
    data_class_processor.register_dict_of_data_classes(dict_of_data_classes)
    assert "dataclassone" in dir(data_class_processor)
    assert "datackasstwo" in dir(data_class_processor)
    assert getattr(data_class_processor, "dataclassone") is DataClassTest
    assert getattr(data_class_processor, "datackasstwo") is DataClassTestTwo


def test_dataclass_name_setter_method():
    data_class_processor = DataClassProcessor()
    data_class_processor.register_dataclass(DataClassTest)
    rule = deepcopy(base_data_class_rule)
    rule[DataClassRuleKeys.NAME] = "data_class_test"
    data_class_processor._set_dataclass_to_use(rule)

    assert data_class_processor._data_class_to_use is DataClassTest


def test_dataclass_name_setter_raises_value_error_when_dataclass_name_not_known():
    data_class_processor = DataClassProcessor()
    with pytest.raises(ValueError):
        data_class_processor._set_dataclass_to_use(base_data_class_rule)


def test_dataclass_set_record_convertor_arguments_method():
    data_class_processor = DataClassProcessor()
    data_class_processor._set_record_covertor_arguments(base_data_class_rule)
    assert (
        data_class_processor._record_convertor_args
        == base_data_class_rule[DataClassRuleKeys.RECORD_CONVERSION_ARGUMENTS]
    )


def test_dataclass_set_dataclass_methods_method():
    data_class_processor = DataClassProcessor()
    data_class_processor._set_dataclass_methods(base_data_class_rule)
    assert (
        data_class_processor._data_class_methods
        == base_data_class_rule[DataClassRuleKeys.METHODS]
    )


def test_prepare_data_class_settings_method():
    """Test that all relevant attributes are set to run the processing the dataclass"""
    data_class_processor = DataClassProcessor()
    data_class_processor.register_dataclass(DataClassTest)
    rule = deepcopy(base_data_class_rule)
    rule[DataClassRuleKeys.NAME] = "data_class_test"
    data_class_processor._prepare_data_class_settings(rule)
    assert data_class_processor._data_class_to_use is DataClassTest
    assert (
        data_class_processor._record_convertor_args
        == base_data_class_rule[DataClassRuleKeys.RECORD_CONVERSION_ARGUMENTS]
    )
    assert (
        data_class_processor._data_class_methods
        == base_data_class_rule[DataClassRuleKeys.METHODS]
    )
