def merge_dicts(dict_a, dict_b, add_keys=True):
    """https://gist.github.com/CMeza99/5eae3af0776bef32f945f34428669437"""

    dict_a = dict_a if dict_a else {}
    dict_b = dict_b if dict_b else {}
    result = dict_a.copy()

    if add_keys is False:
        dict_b = { key: dict_b[key] for key in set(result).intersection(set(dict_b)) }

    result.update({
        key: merge_dicts(result[key], dict_b[key], add_keys=add_keys)
        if isinstance(result.get(key), dict) and isinstance(dict_b[key], dict)
        else dict_b[key]
        for key in dict_b.keys()
    })

    return result