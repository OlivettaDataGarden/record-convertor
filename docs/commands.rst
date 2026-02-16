=================
Command Processor
=================

Commands create **output field values** from the input record. They are used as the value
side of an output mapping rule and are identified by a ``$`` prefix.

.. code-block:: python

    rules = {
        "output_field": {"$command_name": {<arguments>}},
    }


Command Reference
-----------------

``$fixed_value``
^^^^^^^^^^^^^^^^

Returns a literal fixed value.

.. code-block:: python

    {"output_field": {"$fixed_value": "some_literal_value"}}

``$split_field``
^^^^^^^^^^^^^^^^

Splits a field by a separator and returns the entry at the given index.

.. code-block:: python

    {"first_name": {"$split_field": {"field": "full_name", "separator": " ", "entry": 0}}}

``$int_from_string``
^^^^^^^^^^^^^^^^^^^^

Extracts a numerical value from a string by removing specified substrings.

.. code-block:: python

    {"count": {"$int_from_string": {"field": "count_str", "remove": ["items", " "]}}}

``$join``
^^^^^^^^^

Joins field values and/or fixed values with an optional separator.

.. code-block:: python

    {"address": {"$join": {"fields": ["street", "city"], "separator": ", "}}}

Fields can include fixed values using ``$fixed:`` prefix:

.. code-block:: python

    {"label": {"$join": {"fields": ["$fixed:Name:", "first_name"], "separator": " "}}}

``$point``
^^^^^^^^^^

Creates a GeoJSON Point geometry from latitude and longitude fields.

.. code-block:: python

    {"location": {"$point": {"lat": "latitude", "lon": "longitude"}}}

Returns:

.. code-block:: python

    {"type": "Point", "coordinates": [<lon>, <lat>]}

``$full_record``
^^^^^^^^^^^^^^^^

Returns the complete input record as the output value.

.. code-block:: python

    {"raw_data": {"$full_record": {}}}

``$join_key_value``
^^^^^^^^^^^^^^^^^^^

Creates a key-value pair from two fields.

.. code-block:: python

    {"metadata": {"$join_key_value": {"key": "meta_key", "value": "meta_value"}}}

``$key_value``
^^^^^^^^^^^^^^

Creates a dict with a fixed key and a value from a field.

.. code-block:: python

    {"info": {"$key_value": {"key": "status", "value": "record_status"}}}

``$from_list``
^^^^^^^^^^^^^^

Transforms a list of dicts using a sub-rules dict. Each item in the source list
is converted using the provided rules.

.. code-block:: python

    {"items": {"$from_list": {"field": "raw_items", "rules": {"name": "item_name", "qty": "quantity"}}}}

``$first_item_from_list``
^^^^^^^^^^^^^^^^^^^^^^^^^

Same as ``$from_list`` but returns only the first converted item instead of a list.

.. code-block:: python

    {"first_item": {"$first_item_from_list": {"field": "raw_items", "rules": {"name": "item_name"}}}}

``$to_list``
^^^^^^^^^^^^

Creates a list from specified field values. Skips ``None`` values.

.. code-block:: python

    {"tags": {"$to_list": {"fields": ["tag1", "tag2", "tag3"]}}}

``$to_list_dynamic``
^^^^^^^^^^^^^^^^^^^^

Creates a list from multiple rule sets, allowing more complex list construction.

.. code-block:: python

    {"contacts": {"$to_list_dynamic": [{"name": "primary_name"}, {"name": "secondary_name"}]}}

``$to_int``
^^^^^^^^^^^

Removes specified strings from a field value (used to clean numeric strings).

.. code-block:: python

    {"year": {"$to_int": {"field": "year_str", "remove": ["year", " "]}}}

``$set_to_none_value``
^^^^^^^^^^^^^^^^^^^^^^

Always returns ``None``. Useful for explicitly setting a field to null.

.. code-block:: python

    {"deprecated_field": {"$set_to_none_value": {}}}

``$allow_none_value``
^^^^^^^^^^^^^^^^^^^^^

Returns the field value, or ``None`` if the field is not found. By default, missing
fields result in an empty dict; this command allows ``None`` instead.

.. code-block:: python

    {"optional_field": {"$allow_none_value": "maybe_missing_field"}}

``$current_year``
^^^^^^^^^^^^^^^^^

Returns the current year as a string.

.. code-block:: python

    {"year": {"$current_year": {}}}


Full Example
------------

.. code-block:: python

    rules = {
        "name": "item.name",
        "location": {"$point": {"lat": "geo.lat", "lon": "geo.lon"}},
        "full_address": {"$join": {"fields": ["street", "city", "country"], "separator": ", "}},
        "source": {"$fixed_value": "api_v2"},
        "year": {"$current_year": {}},
    }
