from typing import Dict, Optional, TypedDict, Union

from .conditions import ConditionsDict

__all__ = [
    "BaseRuleDict",
    "RulesDict",
    "BaseConvertorKeys",
    "FormatDateRuleDict",
    "FormatDateConvKeys",
]


class GenericRuleKeys:
    # generic fields
    CONDITION = "condition"


class BaseConvertorKeys(GenericRuleKeys):
    FIELDNAME = "fieldname"
    ACTIONS = "actions"
    ACTIONTYPE = "action_type"
    ACTIONVALUE = "action_value"


class FormatDateConvKeys(GenericRuleKeys):
    FORMAT = "format"
    DATEFIELD = "date_field"


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


RulesDict = Dict[str, BaseRuleDict]
