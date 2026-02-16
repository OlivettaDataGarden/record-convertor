=====
Usage
=====

Installation
------------

Install from PyPI::

    pip install record-convertor

Import the main classes:

.. code-block:: python

    from record_convertor import RecordConvertor, RecordConvertorWithRulesDict


Basic Concepts
--------------

A **rules dict** maps output field names to instructions for how to derive their values
from the input record. The simplest rule is a direct field mapping:

.. code-block:: python

    rules = {
        "output_field": "input_field",
    }

For nested input data, use dot-separated paths (powered by JMESPath):

.. code-block:: python

    rules = {
        "brand_name": "item.brand.name",       # nested dict access
        "first_tag": "item.tags[0]",            # list index access
    }

Beyond simple mappings, rules can include:

- **Field conversions** (``$convert``) — transform values in-place on the input record
- **Date formatting** (``$format_date``) — convert between date formats
- **Commands** (``$fixed_value``, ``$join``, ``$point``, etc.) — compute output values
- **Dataclass processing** (``$dataclass``) — run records through Pydantic/dataclass models
- **Skip rules** (``$skip``) — conditionally skip the entire record
- **Conditions** — control when conversions or commands execute


Using Dict Rules
----------------

The simplest approach uses ``RecordConvertorWithRulesDict`` with a plain dict:

.. code-block:: python

    from record_convertor import RecordConvertorWithRulesDict

    rules = {
        "name": "item.name",
        "city": "address.city",
    }

    convertor = RecordConvertorWithRulesDict(rule_dict=rules)
    result = convertor.convert({"item": {"name": "Shop"}, "address": {"city": "Amsterdam"}})
    # {"name": "Shop", "city": "Amsterdam"}


Using YAML Rules
----------------

For more complex rule sets, subclass ``RecordConvertor`` and point to a YAML file:

.. code-block:: python

    from record_convertor import RecordConvertor

    class MyConvertor(RecordConvertor):
        pass

    convertor = MyConvertor(rule_source="/path/to/rules.yaml")
    result = convertor.convert(input_record)

The YAML file uses the same structure as the dict rules:

.. code-block:: yaml

    name: item.name
    city: address.city
    website:
      $convert_website:
        fieldname: item.url
        actions:
          - action_type: remove_params_from_url
            action_value: item.url


Rule Types Overview
-------------------

Field Mapping
^^^^^^^^^^^^^

A string value maps an output key directly to an input field path:

.. code-block:: python

    {"output_key": "input.field.path"}


Field Conversions (``$convert``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Transform a field value in-place on the input record before it is mapped to output.
See :doc:`field-convertors` for the full reference.

.. code-block:: python

    {
        "$convert_price": {
            "fieldname": "item.price_str",
            "actions": [
                {"action_type": "to_str", "action_value": "item.price_str"}
            ]
        },
        "price": "item.price_str",
    }


Date Formatting (``$format_date``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Convert date fields between formats. See :doc:`date-convertors`.

.. code-block:: python

    {
        "$format_date_opened": {
            "date_field": "opened_date",
            "format": "DD-MM-YYYY",
        },
        "opened": "opened_date",
    }


Commands (``$``)
^^^^^^^^^^^^^^^^

Compute output values using command functions. See :doc:`commands`.

.. code-block:: python

    {
        "location": {"$point": {"lat": "latitude", "lon": "longitude"}},
        "full_name": {"$join": {"fields": ["first_name", "last_name"], "separator": " "}},
    }


Skip Rules (``$skip``)
^^^^^^^^^^^^^^^^^^^^^^^

Conditionally skip the entire record. See :doc:`conditions`.

.. code-block:: python

    {
        "$skip": {
            "fieldname": "status",
            "condition": {"equals": "inactive"},
        }
    }


Dataclass Processing (``$dataclass``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run a record through a Pydantic model or dataclass. See :doc:`dataclass-processor`.

.. code-block:: python

    {
        "$dataclass": {
            "data_class_name": "MyModel",
            "params": {"name": "item.name"},
            "methods": [],
        }
    }


Protocol-Based Customization
-----------------------------

The convertor uses protocols for dependency injection, allowing you to substitute
custom implementations:

.. code-block:: python

    from record_convertor import RecordConvertorWithRulesDict
    from record_convertor.field_convertors import BaseFieldConvertor

    class MyFieldConvertor(BaseFieldConvertor):
        def my_custom_action(self, action_value):
            # custom conversion logic
            self.set_field_value("transformed", self._field_name)

    convertor = RecordConvertorWithRulesDict(
        rule_dict=rules,
        field_convertor=MyFieldConvertor,
    )

Available protocol injection points:

- ``field_convertor`` — custom field conversion class (implements ``FieldConvertorProtocol``)
- ``date_formatter`` — custom date formatting class (implements ``DateFormatProtocol``)
- ``command_class`` — custom command processor class
- ``data_classes`` — list of dataclass/Pydantic model types to register
