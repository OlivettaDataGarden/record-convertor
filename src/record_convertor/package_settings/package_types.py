from typing import Dict, Optional, TypedDict, Union

from .conditions import ConditionsDict

__all__ = ["RuleDict", "RulesDict"]


class RuleDict(TypedDict):
    condition: Optional[ConditionsDict]
    format: Optional[str] # used by date convertor
    fieldname: Optional[str]
    action_type: Optional[str] # tbd if these are still needed
    action_value: Union[str, dict] # tbd if these are still needed


RulesDict = Dict[str, RuleDict] 
