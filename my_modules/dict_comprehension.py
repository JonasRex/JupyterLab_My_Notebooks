def create_dict_from_lists(list_of_keys, list_of_values):
    return {key:value for (key, value) in zip(list_of_keys, list_of_values)}
