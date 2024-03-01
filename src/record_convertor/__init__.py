"""
Module to define record conversion functionality.

Classes:
    - RecordConverter: Public class to be used to convert records based upon
                       provide rules.

usage:
>>> converted_record: dict = \
>>>     RecordConvertor(rules: Rules).convert(record: dict)
"""


class RecordConvertor():
    """
    Class that coverts a input record to a format as defined by a yaml file
    provided when creating the class instance.


    public methods:
        - convert: converts record according to provided rules via the rules class

    """
    pass