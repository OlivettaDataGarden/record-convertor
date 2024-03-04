from typing import Dict, Optional, TypedDict, Union

from .conditions import ConditionsDict

__all__ = ["RuleDict", "RulesDict", "RuleKeys"]


class RuleKeys:
    CONDITION = "condition"
    FORMAT = "format"
    FIELDNAME = "fieldname"
    DATEFIELD = "date_field"
    ACTIONS = "actions"
    ACTIONTYPE = "action_type"
    ACTIONVALUE = "action_value"


class RuleDict(TypedDict):
    condition: Optional[ConditionsDict]
    format: Optional[str]  # used by date convertor
    fieldname: Optional[str]
    actions: Optional[dict]
    action_type: Optional[str]  # tbd if these are still needed
    action_value: Union[str, dict]  # tbd if these are still needed


RulesDict = Dict[str, RuleDict]
