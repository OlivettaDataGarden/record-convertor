================
Record Convertor
================

.. image:: https://img.shields.io/pypi/v/record-convertor.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/record-convertor

.. image:: https://img.shields.io/pypi/pyversions/record-convertor.svg
    :alt: Supported versions
    :target: https://pypi.org/project/record-convertor

.. image:: https://readthedocs.org/projects/record-convertor/badge/?style=flat
    :target: https://record-convertor.readthedocs.io/
    :alt: Documentation Status

A rule-based record transformation library for Python. Converts input dicts into desired
output formats using YAML or dict-based rule configurations. Designed to normalize records
of the same data type from different sources into a single validated structure.

Features
--------

- Map fields using simple string paths or JMESPath expressions for nested access
- Transform field values in-place with 25+ built-in conversion actions (string ops, math, URL cleanup, phone parsing, etc.)
- Compute output values with command processors (GeoJSON points, joins, splits, list transforms)
- Convert between date formats (Unix timestamps, DD-MM-YYYY, YYYY_MM_DD, etc.)
- Run records through Pydantic models or dataclasses with optional method invocation
- Conditionally execute rules or skip entire records
- Extend with custom field convertors, date formatters, and command classes via protocols

Installation
------------

::

    pip install record-convertor

Quick Start
-----------

.. code-block:: python

    from record_convertor import RecordConvertorWithRulesDict

    rules = {
        "name": "item.name",
        "brand": "item.brand.name",
        "price": "item.price",
    }

    convertor = RecordConvertorWithRulesDict(rule_dict=rules)

    result = convertor.convert({
        "item": {
            "name": "Widget",
            "brand": {"name": "Acme"},
            "price": 9.99,
        }
    })
    # {"name": "Widget", "brand": "Acme", "price": 9.99}

Documentation
-------------

Full documentation is available at https://record-convertor.readthedocs.io/

License
-------

LGPL-3.0-or-later
