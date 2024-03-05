from record_convertor.package_settings import keys_in_lower_case, dict_without_non_values

def test_keys_returned_in_lower_case():
    """
    Test that all keys in a dictionary are converted to lower case.
    """
    test_dict = {"KEY": "VALUE"}
    assert keys_in_lower_case(test_dict) == {"key": "VALUE"}

def test_nested_keys_returned_in_lower_case():
    """
    Test that all keys in a nested dictionary are converted to lower case.
    """
    test_dict = {"KEY": {"NESTED_KEY": "VALUE"}}
    assert keys_in_lower_case(test_dict) == {"key": {"nested_key": "VALUE"}}

def test_list_nested_keys_returned_in_lower_case():
    """
    Test that keys in dictionaries nested within a list are converted to lower case.
    This includes testing dictionaries directly within the list and nested within other dictionaries.
    """
    test_list = [
        {"KEY1": {"NESTED_KEY1": "VALUE"}},
        {"KEY2": "VALUE"},
        "other list entry"
    ]
    assert keys_in_lower_case(test_list) == [
        {"key1": {"nested_key1": "VALUE"}},
        {"key2": "VALUE"},
        "other list entry"
    ]

def test_none_values_removed_from_dict():
    """
    Test that keys with None as value are removed from the dictionary.
    """
    test_dict = {"key1": "VALUE", "key2": None}
    assert dict_without_non_values(test_dict) == {"key1": "VALUE"}
