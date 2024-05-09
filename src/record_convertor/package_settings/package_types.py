from enum import Enum
from typing import Optional, TypedDict, Union

from .conditions import ConditionsDict

__all__ = [
    "RecConvKeys",
    "BaseRuleDict",
    "RulesDict",
    "BaseConvertorKeys",
    "FormatDateRuleDict",
    "FormatDateConvKeys",
    "SkipConvKeys",
    "SkipRuleDict",
    "DataClassRuleKeys",
    "DataClassRuleDict",
]


class RecConvKeys:
    SKIP = "$skip"
    CONVERT = "$convert"


class BaseConvertorKeys(Enum):
    CONDITION = "condition"
    FIELDNAME = "fieldname"
    ACTIONS = "actions"
    ACTIONTYPE = "action_type"
    ACTIONVALUE = "action_value"


class FormatDateConvKeys(Enum):
    CONDITION = "condition"
    FORMAT = "format"
    DATEFIELD = "date_field"


class SkipConvKeys(Enum):
    CONDITION = "condition"
    FIELDNAME = "fieldname"


class DataClassRuleKeys:
    NAME = "data_class_name"
    RECORD_CONVERSION_ARGUMENTS = "params"
    METHODS = "methods"


class BaseRuleDict(TypedDict):
    condition: Optional[ConditionsDict]
    format: Optional[str]  # used by date convertor
    fieldname: Optional[str]
    actions: Optional[dict]
    action_type: Optional[str]  # tbd if these are still needed
    action_value: Union[str, dict]  # tbd if these are still needed


class FormatDateRuleDict(TypedDict):
    condition: Optional[ConditionsDict]
    format: str
    date_field: str


class SkipRuleDict(TypedDict):
    condition: ConditionsDict
    fieldname: str


class DataClassRuleDict(TypedDict):
    data_class_name: str
    params: dict
    methods: list[dict]


RulesDict = Union[
    BaseRuleDict,
    FormatDateRuleDict,
    SkipRuleDict,
    DataClassRuleDict,
    dict[
        str,
        Union[
            str,
            BaseRuleDict,
            FormatDateRuleDict,
            SkipRuleDict,
            DataClassRuleDict,
        ],
    ],
]
