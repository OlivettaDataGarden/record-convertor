"""
Module to define customer excpetions for record_convertor package

exceptions
- ProcessArgsMustBeOfTypeList
"""

from typing import Any


class ProcessArgsMustBeOfTypeList(Exception):
    def __init__(self, process_args: Any):
        super().__init__(
            f"process_args must be of <type> list but is of type `{type(process_args)}"
        )


class ProcessArgsMustBeOfTypeDict(Exception):
    def __init__(self, process_args: Any):
        super().__init__(
            f"process_args must be of type <dict> but is of type `{type(process_args)}"
        )
