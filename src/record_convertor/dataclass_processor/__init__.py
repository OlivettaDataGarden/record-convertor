from typing import Type

from ..package_settings import (
    class_name_in_snake_case,
    DataClassRuleDict,
    DataClassRuleKeys,
    RecordConvertorProtocol,
    DataclassInstance,
)
from dataclasses import is_dataclass, asdict


class DataClassProcessor:
    def data_from_dataclass(
        self,
        record: dict,
        rules: DataClassRuleDict,
        record_convertor: RecordConvertorProtocol,
    ) -> dict:
        self._record = record
        self._record_covertor = record_convertor
        self._prepare_dataclass_settings(rules=rules)
        return self._create_return_dict(rules=rules)

    def register_dict_of_data_classes(
        self, dataclasses: dict[str, Type[DataclassInstance]]
    ):
        for dataclass_name, dataclass in dataclasses.items():
            self._register_dataclass(dataclass_name=dataclass_name, dataclass=dataclass)

    def register_data_classes(self, dataclasses: list[Type[DataclassInstance]]):
        for dataclass in dataclasses:
            self.register_dataclass(dataclass=dataclass)

    def register_dataclass(self, dataclass: Type[DataclassInstance]):
        data_class_name_snake_case = class_name_in_snake_case(dataclass.__name__)
        self._register_dataclass(
            dataclass_name=data_class_name_snake_case, dataclass=dataclass
        )

    def _register_dataclass(
        self, dataclass_name: str, dataclass: Type[DataclassInstance]
    ):
        """Method to actually set define dataclass as an attribute of the dataclass processor."""
        if not is_dataclass(dataclass):
            raise ValueError(f"class '{dataclass.__name__}' is not a dataclass")
        setattr(self, dataclass_name, dataclass)

    def _prepare_dataclass_settings(self, rules: DataClassRuleDict):
        self._set_dataclass_to_use(rules)
        self._set_record_covertor_arguments(rules)
        self._set_dataclass_methods(rules)

    def _set_record_covertor_arguments(self, rules: DataClassRuleDict):
        self._record_convertor_args: dict = rules.get(
            DataClassRuleKeys.RECORD_CONVERSION_ARGUMENTS
        )

    def _set_dataclass_methods(self, rules: DataClassRuleDict):
        self._data_class_methods: list[dict] = rules.get(DataClassRuleKeys.METHODS)

    def _set_dataclass_to_use(self, rules: DataClassRuleDict):
        data_class_name = rules.get(DataClassRuleKeys.NAME)
        try:
            self._dataclass_to_be_used: Type = getattr(self, data_class_name)
        except AttributeError:
            raise ValueError(f"Unknown dataclass '{data_class_name} defines in rules")

    def _get_dataclass_content(self, rules: DataClassRuleDict) -> dict:
        """Convert input record into dataclass content using provided rules set."""
        dataclass_content_creator = (
            self._record_covertor.get_record_convertor_copy_with_new_rules(
                new_rules=rules
            )
        )
        return dataclass_content_creator.convert(record=self._record)

    def _create_return_dict(self, rules: DataClassRuleDict) -> dict:
        dataclass_content = self._get_dataclass_content(rules)
        dataclass_instance = self._get_dataclass_instance(dataclass_content)
        return asdict(dataclass_instance)

    def _get_dataclass_instance(self, dataclass_content: dict) -> DataclassInstance:
        dataclass_instance = self._dataclass_to_be_used(**dataclass_content)
        dataclass_instance = self._update_dataclass_with_provided_methods(
            dataclass_instance
        )
        return dataclass_instance

    def _update_dataclass_with_provided_methods(
        self, dataclass_instance: DataclassInstance
    ) -> DataclassInstance:
        for method in self._data_class_methods:
            [[method, method_argument_rules]] = method.items()
            method_arguments = self._get_method_arguments(method_argument_rules)
            for method_argument in method_arguments:
                getattr(dataclass_instance, method)(**method_argument)
        return dataclass_instance

    def _get_method_arguments(self, method_argument_rules: dict) -> list[dict]:
        method_arguments = (
            self._record_covertor.get_record_convertor_copy_with_new_rules(
                new_rules=method_argument_rules
            ).convert(self._record)
        )
        return (
            method_arguments
            if isinstance(method_arguments, list)
            else [method_arguments]
        )
