from common.utils import hash_string, remote_procedure_call


def clear_preceeding_keys(keys: dict, node_id: str) -> dict:
    """
    Gets the keys that are preceeding the key.

    args:
        key: the key to be searched for (str)
        keys: the keys to be searched (dict)
    returns:
        cleared_keys: the keys that are preceeding the key (dict)
    """
    cleared_keys = {}
    for k in keys:
        if hash_string(k) < int(node_id):
            cleared_keys.update({k: keys.pop(k)})
    return cleared_keys


def key_transfer_helper(keys: dict, address: str, call_type: str) -> dict:
    """
    Transfers the keys to the successor.

    args:
        keys: the keys to be transferred (dict)
        address: the address of the successor (str)
        call_type: the type of call to be made (str)
    """
    for key in keys:
        remote_procedure_call(address, 'key_rpc_interface',
                              (call_type, key, keys[key]))


def key_rpc_helper(address: str, call_type: str, keys: dict, key: str, value: str):
    if call_type == 'get':
        if key in keys:
            response, flag = keys[key], True
    elif call_type == 'add':
        keys[key] = value
        response, flag = address, True
    elif call_type == 'remove':
        if key in keys:
            keys.pop(key)
            response, flag = address, True
        else:
            response, flag = None, False
    else:
        response, flag = None, False  # Create a specific error for this
    return (response, flag)
