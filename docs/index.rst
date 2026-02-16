================
Record Convertor
================

Rule-based record transformation for Python
============================================

**record-convertor** is a library that converts input dicts into desired output formats
using YAML or dict-based rule configurations. It normalizes records of the same data type
from different sources into a single validated structure.

.. list-table::
    :widths: 8 50
    :stub-columns: 1

    * - docs
      - |docs|
    * - package
      - |version| |supported-versions|

.. |docs| image:: https://readthedocs.org/projects/record-convertor/badge/?style=flat
    :target: https://record-convertor.readthedocs.io/
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/record-convertor.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/record-convertor

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/record-convertor.svg
    :alt: Supported versions
    :target: https://pypi.org/project/record-convertor

Installation
------------

::

    pip install record-convertor

Quick Example
-------------

.. code-block:: python

    from record_convertor import RecordConvertorWithRulesDict

    rules = {
        "name": "item.name",
        "brand": "item.brand.name",
        "price": "item.price",
    }

    convertor = RecordConvertorWithRulesDict(rule_dict=rules)

    input_record = {
        "item": {
            "name": "Widget",
            "brand": {"name": "Acme"},
            "price": 9.99,
        }
    }

    result = convertor.convert(input_record)
    # result: {"name": "Widget", "brand": "Acme", "price": 9.99}

Contents
--------

.. toctree::
   :maxdepth: 2

   usage
   field-convertors
   commands
   conditions
   date-convertors
   dataclass-processor
   api
   contributing
   authors
   changelog


Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
