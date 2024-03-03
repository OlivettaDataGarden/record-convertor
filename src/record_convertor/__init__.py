"""
Module to define record conversion functionality.

Classes:
    - RecordConverter: Public class to be used to convert records based upon
                       provide rules.

usage:
>>> converted_record: dict = \
>>>     RecordConvertor(rules: Rules).convert(record: dict)
"""

from .package_settings import ConvertRecordProtocol


class RecordConvertor:
    """
    Class that coverts a input record to a format as defined by a yaml file
    provided when creating the class instance.


    public methods:
        - convert: converts record according to provided rules via the rules class

    """

    CONVERTOR: type[ConvertRecordProtocol]

    def convert(self, record: dict) -> dict:
        """
        Primary public method to run the actual conversion of the record.

        Args:
            record (dict): input record

        Returns:
            dict: converted record
        """
        return self.CONVERTOR().convert(record=record)
