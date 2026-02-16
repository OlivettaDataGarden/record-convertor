==========
Conditions
==========

Conditions control when a rule executes. They can be attached to field conversions
(``$convert``), date formatting (``$format_date``), and skip rules (``$skip``).

All conditions in a rule must evaluate to ``True`` for the rule to execute.

Condition Format
----------------

Conditions are specified as a dict where each key is a condition name and the value
is the argument for that condition:

.. code-block:: python

    {
        "$convert_example": {
            "fieldname": "status",
            "conditions": {
                "is_null": False,
                "equals": "active",
            },
            "actions": [...]
        }
    }

In the example above, both ``is_null: False`` (field is not null) **and** ``equals: "active"``
must be true for the actions to run.


Skip Rules
----------

The ``$skip`` rule uses conditions to skip the entire record:

.. code-block:: python

    {
        "$skip": {
            "fieldname": "status",
            "condition": {
                "equals": "deleted",
            }
        }
    }

When the condition evaluates to ``True``, the record is skipped and the convertor
returns the ``DEFAULT_VALUE`` (empty dict by default).


Condition Reference
-------------------

String Type Checks
^^^^^^^^^^^^^^^^^^

``is_a_string``
    Returns ``True`` if the field value is a string.

    .. code-block:: python

        {"conditions": {"is_a_string": True}}

``is_not_a_string``
    Returns ``True`` if the field value is not a string.

    .. code-block:: python

        {"conditions": {"is_not_a_string": True}}

Null Checks
^^^^^^^^^^^

``is_null``
    Checks whether the field value is ``None``. Pass ``True`` to match null values,
    ``False`` to match non-null values.

    .. code-block:: python

        {"conditions": {"is_null": False}}     # field must not be None
        {"conditions": {"is_null": True}}      # field must be None

``field_does_exist``
    Returns ``True`` if the field value is not ``None``.

    .. code-block:: python

        {"conditions": {"field_does_exist": True}}

``field_does_not_exist``
    Returns ``True`` if the field value is ``None``.

    .. code-block:: python

        {"conditions": {"field_does_not_exist": True}}

Equality Checks
^^^^^^^^^^^^^^^

``equals``
    Returns ``True`` if the field value equals the specified value.

    .. code-block:: python

        {"conditions": {"equals": "active"}}

``does_not_equal``
    Returns ``True`` if the field value does not equal the specified value.

    .. code-block:: python

        {"conditions": {"does_not_equal": "deleted"}}

List Membership
^^^^^^^^^^^^^^^

``in_list``
    Returns ``True`` if the field value is in the provided list.

    .. code-block:: python

        {"conditions": {"in_list": ["active", "pending"]}}

``not_in_list``
    Returns ``True`` if the field value is not in the provided list.

    .. code-block:: python

        {"conditions": {"not_in_list": ["deleted", "archived"]}}

String Content
^^^^^^^^^^^^^^

``contains``
    Returns ``True`` if the field value contains the specified substring.

    .. code-block:: python

        {"conditions": {"contains": "http"}}

``does_not_contain``
    Returns ``True`` if the field value does not contain the specified substring.

    .. code-block:: python

        {"conditions": {"does_not_contain": "spam"}}

``str_length``
    Returns ``True`` if the string length equals the specified value.

    .. code-block:: python

        {"conditions": {"str_length": 2}}

Date Checks
^^^^^^^^^^^

``date_not_today``
    Returns ``True`` if the field value (a ``YYYY-MM-DD`` date string) is not today's date.

    .. code-block:: python

        {"conditions": {"date_not_today": True}}


Combining Conditions
--------------------

Multiple conditions can be combined in a single dict. All conditions must pass:

.. code-block:: python

    {
        "$convert_example": {
            "fieldname": "email",
            "conditions": {
                "is_null": False,
                "contains": "@",
                "does_not_contain": "test",
            },
            "actions": [
                {"action_type": "to_lower_str", "action_value": "email"}
            ]
        }
    }
