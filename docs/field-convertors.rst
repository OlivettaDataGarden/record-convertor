================
Field Convertors
================

Field convertors transform values **in-place** on the input record before output mapping.
They are triggered by rule keys starting with ``$convert``.

Rule Format
-----------

.. code-block:: python

    {
        "$convert_<name>": {
            "fieldname": "path.to.field",
            "conditions": {                # optional
                "is_null": False,
            },
            "actions": [
                {
                    "action_type": "<action_name>",
                    "action_value": "<value_or_field_path>",
                    "target_field_name": "optional.target",  # optional
                }
            ]
        }
    }

- ``fieldname`` — the input field to operate on (JMESPath dot notation)
- ``conditions`` — optional dict of conditions; all must be true for the actions to execute (see :doc:`conditions`)
- ``actions`` — list of action dicts to apply sequentially
- ``action_type`` — name of the action method to call
- ``action_value`` — argument passed to the action method
- ``target_field_name`` — optional; if present, the result is written to this field instead of the source field


String Operations
-----------------

``to_str``
^^^^^^^^^^

Converts the field value to a string.

.. code-block:: python

    {"action_type": "to_str", "action_value": "fieldname"}

``to_lower_str``
^^^^^^^^^^^^^^^^

Converts the field value to a lowercase string.

.. code-block:: python

    {"action_type": "to_lower_str", "action_value": "fieldname"}

``to_upper_str``
^^^^^^^^^^^^^^^^

Converts the field value to an uppercase string.

.. code-block:: python

    {"action_type": "to_upper_str", "action_value": "fieldname"}

``add_prefix``
^^^^^^^^^^^^^^

Prepends a fixed string to the field value.

.. code-block:: python

    {"action_type": "add_prefix", "action_value": "https://"}

``add_postfix``
^^^^^^^^^^^^^^^

Appends a fixed string to the field value.

.. code-block:: python

    {"action_type": "add_postfix", "action_value": "/index.html"}

``string_begin``
^^^^^^^^^^^^^^^^

Returns the first N characters of a string value.

.. code-block:: python

    {"action_type": "string_begin", "action_value": 10}

``str_to_dict``
^^^^^^^^^^^^^^^

Parses a JSON string into a dict.

.. code-block:: python

    {"action_type": "str_to_dict", "action_value": "fieldname"}


URL Operations
--------------

``remove_params_from_url``
^^^^^^^^^^^^^^^^^^^^^^^^^^

Strips query parameters from a URL, returning only the base URL.

.. code-block:: python

    {"action_type": "remove_params_from_url", "action_value": "website_url"}


Math Operations
---------------

``multiply_by``
^^^^^^^^^^^^^^^

Multiplies the field value by a given number.

.. code-block:: python

    {"action_type": "multiply_by", "action_value": 100}

``divide_by``
^^^^^^^^^^^^^

Divides the field value by a given number.

.. code-block:: python

    {"action_type": "divide_by", "action_value": 1000}

``round``
^^^^^^^^^

Rounds the field value to the specified number of decimal places.

.. code-block:: python

    {"action_type": "round", "action_value": 2}


Date Operations
---------------

``days_ago_to_date``
^^^^^^^^^^^^^^^^^^^^

Converts a "number of days ago" value to a ``YYYY-MM-DD`` date string.

.. code-block:: python

    {"action_type": "days_ago_to_date", "action_value": "days_since_update"}

``date_of_today``
^^^^^^^^^^^^^^^^^

Sets the field to today's date as ``YYYY-MM-DD``.

.. code-block:: python

    {"action_type": "date_of_today", "action_value": "last_checked"}


Key and Field Operations
------------------------

``fixed_value``
^^^^^^^^^^^^^^^

Sets the field to a fixed (literal) value.

.. code-block:: python

    {"action_type": "fixed_value", "action_value": "default_status"}

``add_value_from_field``
^^^^^^^^^^^^^^^^^^^^^^^^

Copies a value from another field into the target field.

.. code-block:: python

    {"action_type": "add_value_from_field", "action_value": "source.field.path"}

``add_key_value_from_field``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Creates a dict from key-value field references.

.. code-block:: python

    {"action_type": "add_key_value_from_field", "action_value": {"key": "key_field", "value": "value_field"}}

``insert_key``
^^^^^^^^^^^^^^

Wraps the field value in a dict with the specified key.

.. code-block:: python

    {"action_type": "insert_key", "action_value": "wrapper_key"}

``change_key_name_to``
^^^^^^^^^^^^^^^^^^^^^^

Renames a field in the record.

.. code-block:: python

    {"action_type": "change_key_name_to", "action_value": "new_field_name"}

``join_fields``
^^^^^^^^^^^^^^^

Joins values from multiple fields into a single string.

.. code-block:: python

    {"action_type": "join_fields", "action_value": {"fields": ["first", "last"], "separator": " "}}

``remove``
^^^^^^^^^^

Removes a field from the record.

.. code-block:: python

    {"action_type": "remove", "action_value": "field_to_remove"}

``add_data_from_dict``
^^^^^^^^^^^^^^^^^^^^^^

Merges entries from another dict field into the current dict field.

.. code-block:: python

    {"action_type": "add_data_from_dict", "action_value": "source_dict_field"}


Data Structure Operations
-------------------------

``select_object_from_list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Selects an object from a list where a key matches a specific value.

.. code-block:: python

    {"action_type": "select_object_from_list", "action_value": {"key": "type", "value": "primary"}}

``list_to_dict``
^^^^^^^^^^^^^^^^

Converts a list of two-element lists (``[[a, b], [c, d]]``) into a dict (``{a: b, c: d}``).

.. code-block:: python

    {"action_type": "list_to_dict", "action_value": "key_value_pairs"}

``add_data_from_list_of_dict``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Converts a list of dicts with key/value pairs into a single flat dict.

.. code-block:: python

    {"action_type": "add_data_from_list_of_dict", "action_value": {"key": "name", "value": "data"}}

``convert_data_from_html_fragment_to_list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Extracts a list of text items from an HTML fragment.

.. code-block:: python

    {"action_type": "convert_data_from_html_fragment_to_list", "action_value": "html_field"}


Phone and Country Operations
-----------------------------

``get_country_code_from_phone_nr``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Extracts the country code from a phone number string using the ``phonenumbers`` library.

.. code-block:: python

    {"action_type": "get_country_code_from_phone_nr", "action_value": "phone"}

``alpha3_to_iso3116_cc``
^^^^^^^^^^^^^^^^^^^^^^^^

Converts an alpha-3 country code (e.g., ``NLD``) to an ISO 3166 two-letter code (e.g., ``NL``).

.. code-block:: python

    {"action_type": "alpha3_to_iso3116_cc", "action_value": "country_code"}


Full Example
------------

.. code-block:: python

    rules = {
        "$convert_cleanup": {
            "fieldname": "item.name",
            "conditions": {"is_null": False},
            "actions": [
                {"action_type": "to_lower_str", "action_value": "item.name"},
                {"action_type": "add_prefix", "action_value": "shop: "},
            ]
        },
        "$convert_price": {
            "fieldname": "item.price",
            "actions": [
                {"action_type": "multiply_by", "action_value": 100},
                {"action_type": "round", "action_value": 0},
            ]
        },
        "name": "item.name",
        "price_cents": "item.price",
    }
