from hashlib import sha256
from zerorpc import Client


def build_address(host: str, port: str) -> str:
    """
    Builds the address for the node.

    returns:
        address: the address of the node (str)
    """
    return f'{host}:{port}'


def build_tcp_address(address: str) -> str:
    """
    Builds the tcp call address for the node.

    returns:
        address: the address of the node (str)
    """
    return f'tcp://{address}'


def hash_string(string: str) -> str:
    """
    Hashes a string using sha256, then returns the hash.

    returns:
        hash: the hash of the string (str) -- length will be 64 characters
    """
    return sha256(string.encode()).hexdigest()


def circular_range_check(start: str, key: str, end: str) -> bool:
    """
    Checks if a key is in a circular range.

    args:
        start: the start of the range (str)
        key: the key to be checked (str)
        end: the end of the range (str)

    returns:
        is_in_range: whether or not the key is in the range (bool)
    """
    if key < end:
        return key <= start < end
    else:
        return key <= start or start < end


def remote_procedure_call(address, method, *args):
    """
    A wrapper for the remote procedure call.

    args:
        address: the address of the node to call (str)
        method: the method to be called (str)
        *args: the arguments to be passed to the method (tuple)
    """
    client = Client()
    tcp_address = build_tcp_address(address)
    print(f'Calling {method} on {tcp_address} with {args}...')
    client.connect(tcp_address)
    response = client(method, *args)
    client.close()
    return response
