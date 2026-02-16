===============
Date Convertors
===============

Date convertors transform date fields from various input formats into the standard
``YYYY-MM-DD`` output format. They are triggered by rule keys starting with ``$format_date``.

Rule Format
-----------

.. code-block:: python

    {
        "$format_date_<name>": {
            "date_field": "path.to.date.field",
            "format": "<input_format>",
            "condition": {                     # optional
                "is_null": False,
            }
        }
    }

- ``date_field`` — the input field containing the date value (JMESPath dot notation)
- ``format`` — the input date format to parse from
- ``condition`` — optional conditions for when to apply the conversion (see :doc:`conditions`)


Supported Input Formats
-----------------------

All formats are converted to the output format ``YYYY-MM-DD``.

.. list-table::
   :header-rows: 1
   :widths: 20 30 30

   * - Format string
     - Input example
     - Output
   * - ``DD-MM-YYYY``
     - ``15-02-2024``
     - ``2024-02-15``
   * - ``DD.MM.YYYY``
     - ``15.02.2024``
     - ``2024-02-15``
   * - ``YYYY_MM_DD``
     - ``2024_02_15``
     - ``2024-02-15``
   * - ``YYYY_MM_DD:Time``
     - ``2024_02_15:14:30:00``
     - ``2024-02-15``
   * - ``UNIX_DT_STAMP``
     - ``1708000000``
     - ``2024-02-15``
   * - ``YYYY-MM-DD``
     - ``2024-02-15``
     - ``2024-02-15``


Examples
--------

Basic date conversion:

.. code-block:: python

    rules = {
        "$format_date_opened": {
            "date_field": "opened_date",
            "format": "DD-MM-YYYY",
        },
        "opened": "opened_date",
    }

    # Input:  {"opened_date": "15-02-2024"}
    # Output: {"opened": "2024-02-15"}

Unix timestamp conversion:

.. code-block:: python

    rules = {
        "$format_date_created": {
            "date_field": "created_at",
            "format": "UNIX_DT_STAMP",
        },
        "created": "created_at",
    }

Nested date field:

.. code-block:: python

    rules = {
        "$format_date_updated": {
            "date_field": "metadata.last_update",
            "format": "YYYY_MM_DD:Time",
        },
        "updated": "metadata.last_update",
    }

Conditional date conversion:

.. code-block:: python

    rules = {
        "$format_date_closed": {
            "date_field": "closed_date",
            "format": "DD-MM-YYYY",
            "condition": {
                "is_null": False,
            }
        },
        "closed": "closed_date",
    }
