================
Record Convertor
================

A toolbox for rule based conversion of input records to desired output formats using a YAML config file as input.
Package was created to convert records of same data type from different sources (and thus different structures)
to a singel validated stucture.

.. start-badges

.. list-table::
    :widths: 8 50
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |travis| |requires| |codecov|
    * - package
      - |version| |wheel| |supported-versions| |commits-since|
  
.. |docs| image:: https://readthedocs.org/projects/errors/badge/?style=flat
    :target: https://errors.readthedocs.io/
    :alt: Documentation Status

.. |codecov| image:: https://codecov.io/gh/MaartendeRuyter/errors/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/MaartendeRuyter/errors

.. |version| image:: https://img.shields.io/pypi/v/error-manager.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/record-convertor

.. |wheel| image:: https://img.shields.io/pypi/wheel/error-manager.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/record-convertor

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/error-manager.svg
    :alt: Supported versions
    :target: https://pypi.org/project/record-convertor

.. |commits-since| image:: https://img.shields.io/github/commits-since/MaartendeRuyter/record-convertor/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/OlivettaDataGarden/record-convertor/compare/v0.1.0...master


.. end-badges


* Free software: GNU Lesser General Public License v3 or later (LGPLv3+)

Installation
============

::

    pip install record-convertor



Main usecases
=============
The record-convertor package provides s 
 
    # retrieve customer defined ErrorCode object form ``ListErrors`` class
    >>> from errors import ListErrors
    >>> error = ListErrors.COULD_NOT_FIND_ERROR_CODE
    >>> error
    ErrorCode(code='ER_GETERROR_00001', description='Could not find requested 
    error code', error_data=<class 'dict'>)
    
    # add custom error data to error message when you want to persist or log
    # the error
    >>> from errors import add_error_data   
    >>> error_with_data = add_error_data(error, {'key': 'Example error data'})
    >>> error_with_data 
    ErrorCode(code='ER_GETERROR_00001', description='Could not find requested error code', error_data={'key': 'Example error data'})


Documentation
=============

https://errors.readthedocs.io/
