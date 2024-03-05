from typing import Dict, List, Any


__all__ = ["list_in_lower_case", "keys_in_lower_case", "dict_without_non_values"]


def list_in_lower_case(input_record: List[Any]) -> List[Any]:
    """
    Return input dict or list with all keys in lower case including nested keys.

    Args:
        input_record (Union[Dict[str, Any], List[Any]]): The dict of which the keys need
        to be put in lower case or a list that needs to be processed item by item.

    Returns:
        Union[Dict[str, Any], List[Any]]: A new dict or list with all keys in lower case.
    """
    result: List[Any] = []
    for item in input_record:
        if isinstance(item, list):
            result.append(list_in_lower_case(item))
        elif isinstance(item, dict):
            result.append(keys_in_lower_case(item))
        else:
            result.append(item)

    return result


def keys_in_lower_case(input_record: dict[str, Any]) -> dict[str, Any]:
    """
    Return input dict or list with all keys in lower case including nested keys.

    Args:
        input_record (Union[Dict[str, Any], List[Any]]): The dict of which the keys need
        to be put in lower case or a list that needs to be processed item by item.

    Returns:
        Union[Dict[str, Any], List[Any]]: A new dict or list with all keys in lower case.
    """
    dict_result: Dict[str, Any] = {}
    for key, value in input_record.items():
        if isinstance(value, list):
            dict_result[key.lower()] = list_in_lower_case(value)
        elif isinstance(value, dict):
            dict_result[key.lower()] = keys_in_lower_case(value)
        else:
            dict_result[key.lower()] = value
    return dict_result


def dict_without_non_values(input_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of the input dict with all None values removed."""
    return {k: v for k, v in input_dict.items() if v is not None}
