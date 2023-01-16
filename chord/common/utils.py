import hashlib
import random


def build_tcp_address(host: str, port: str):
    """
    Builds the tcp call address for the node.

    returns:
        address: the address of the node (str)
    """
    return f'tcp://{host}:{port}'
