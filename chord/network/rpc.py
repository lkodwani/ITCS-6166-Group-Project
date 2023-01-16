from common.utils import build_tcp_address
from nodes import CurrentNode, Node
from threading import Thread
from yaml import safe_load
from zerorpc import Client


def remote_procedure_call(address, method, *args):
    """
    A wrapper for the remote procedure call.

    args:
        method: the method to be called (str)
        *args: the arguments to be passed to the method (tuple)
    """
    client = Client()
    client.connect(build_tcp_address())
    response = client(method, *args)
    client.close()
    return response


class ChordClient:
    """
    An RPC-friendly client for the chord ring.

    attr:
        host: the ip address of the node (str)
        port: the port of the node (str)
        name: the name of the node (str)
    """

    def __init__(self, host: str, port: str, name: str):
        self.host = host
        self.port = port
        self.name = name

    def build_tcp_address(self):
        """
        Builds the tcp call address for the node.

        returns:
            address: the address of the node (str)
        """
        return f'tcp://{self.host}:{self.port}'

    def get_node_info_by_key(self, key: str):
        """
        Gets the node info for the node that owns the key.

        args:
            key: the key to be searched for (str)
        """
        return self._remote_procedure_call('get_node_by_key', [key])

    def add_new_key(self, key: str, value: str):
        """
        Adds a new key to the ring.

        args:
            key: the key to be added (str)
            value: the value to be added (str)
        """
        return self._remote_procedure_call('add_new_key', [key, value])
