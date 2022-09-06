def create_dict_from_lists(list_of_keys, list_of_values):
    """Easy way to create a dictionary out of two different lists. One with the keys and one with values.

    Args:
        list_of_keys (_type_): Keys
        list_of_values (_type_): Values

    Returns:
        _type_: A dictionary with keys and values.
    """
    return {key:value for (key, value) in zip(list_of_keys, list_of_values)}
