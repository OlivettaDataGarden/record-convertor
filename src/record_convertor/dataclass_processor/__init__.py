from typing import Type

from ..package_settings import class_name_in_snake_case, DataClassRuleDict, DataClassRuleKeys
from dataclasses import is_dataclass

class DataClassProcessor():
    _data_classes: dict[str, Type] = {}

    def register_dict_of_data_classes(self, dataclasses: dict[str, Type]):
        for dataclass_name, dataclass in dataclasses.items():
            self._register_dataclass(
                dataclass_name=dataclass_name,
                dataclass=dataclass)

    def register_data_classes(self, dataclasses: list[Type]):
        for dataclass in dataclasses:
            self.register_dataclass(dataclass=dataclass)

    def register_dataclass(self, dataclass: Type):
        data_class_name_snake_case = class_name_in_snake_case(dataclass.__name__)
        self._register_dataclass(
            dataclass_name=data_class_name_snake_case,
            dataclass=dataclass)

    def _register_dataclass(self, dataclass_name: str, dataclass: Type):
        """Method to actually set define dataclass as an attribute of the dataclass processor."""
        if not is_dataclass(dataclass):
            raise ValueError(f"class '{dataclass.__name__}' is not a dataclass")
        setattr(self, dataclass_name, dataclass)     
        

    def _prepare_data_class_settings(self, rules: DataClassRuleDict):
        self._set_dataclass_to_use(rules)    
        self._set_record_covertor_arguments(rules)
        self._set_dataclass_methods(rules)

    def  _set_record_covertor_arguments(self, rules: DataClassRuleDict):
        self._record_convertor_args: dict = rules.get(
            DataClassRuleKeys.RECORD_CONVERSION_ARGUMENTS)
    
    def _set_dataclass_methods(self, rules: DataClassRuleDict):
        self._data_class_methods: list[dict] = rules.get(
            DataClassRuleKeys.METHODS)

    def _set_dataclass_to_use(self, rules: DataClassRuleDict):
        data_class_name = rules.get(DataClassRuleKeys.NAME)
        try:
            self._data_class_to_use: str = getattr(self, data_class_name)
        except AttributeError:
            raise ValueError(f"Unknown dataclass '{data_class_name} defines in rules")
        
