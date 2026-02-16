===================
Dataclass Processor
===================

The dataclass processor runs input records through Python dataclasses or Pydantic
``BaseModel`` classes, optionally calling methods on the instance before extracting
the result as a dict.

Rule Format
-----------

.. code-block:: python

    {
        "$dataclass": {
            "data_class_name": "MyModel",
            "params": {
                "output_key": "input.field.path",
            },
            "methods": [
                {
                    "method_name": "validate",
                    "args": {}
                }
            ]
        }
    }

- ``data_class_name`` — name of the registered dataclass or Pydantic model
- ``params`` — a rules dict that maps dataclass field names to input record paths (this is itself a record conversion)
- ``methods`` — optional list of methods to call on the created instance before extracting the dict


Registering Dataclasses
-----------------------

Dataclasses must be registered with the convertor before use. Pass them via the
``data_classes`` parameter:

.. code-block:: python

    from dataclasses import dataclass
    from record_convertor import RecordConvertorWithRulesDict

    @dataclass
    class Location:
        city: str
        country: str

    rules = {
        "$dataclass": {
            "data_class_name": "Location",
            "params": {
                "city": "address.city",
                "country": "address.country_code",
            },
            "methods": [],
        }
    }

    convertor = RecordConvertorWithRulesDict(
        rule_dict=rules,
        data_classes=[Location],
    )

    result = convertor.convert({"address": {"city": "Amsterdam", "country_code": "NL"}})
    # {"city": "Amsterdam", "country": "NL"}


Using Pydantic Models
---------------------

Pydantic ``BaseModel`` classes work the same way as dataclasses:

.. code-block:: python

    from pydantic import BaseModel
    from record_convertor import RecordConvertorWithRulesDict

    class Product(BaseModel):
        name: str
        price: float

        def apply_tax(self, rate: float = 0.21):
            self.price = round(self.price * (1 + rate), 2)

    rules = {
        "$dataclass": {
            "data_class_name": "Product",
            "params": {
                "name": "item.name",
                "price": "item.base_price",
            },
            "methods": [
                {"method_name": "apply_tax", "args": {"rate": 0.21}}
            ],
        }
    }

    convertor = RecordConvertorWithRulesDict(
        rule_dict=rules,
        data_classes=[Product],
    )


Running Methods
---------------

The ``methods`` list specifies methods to invoke on the dataclass instance after
creation. Methods are called in order, and their arguments are resolved from the
input record:

.. code-block:: python

    "methods": [
        {
            "method_name": "enrich",
            "args": {
                "source": "metadata.source",
            }
        }
    ]

The instance is updated by each method call. After all methods have run, the
instance is converted to a dict (using ``dataclasses.asdict()`` or Pydantic's
``model_dump()``), which becomes the output.
