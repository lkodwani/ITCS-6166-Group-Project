from common.utils import *
from config.consts import RING_SIZE
from network.fingers import initialize_finger_table, create_finger_table, update_finger_table
from network.keys import clear_preceeding_keys, key_rpc_helper, key_transfer_helper


class Node:
    """
    A node in a chord ring.

    attr:
        address: the address of the node (str)
        id: the id of the node (str)
        predecessor: the predecessor of the node (node_info dict)
        successors: the successors of the node (list of node_info dicts)
        data: the data stored within the node (dict where key: datatype, value: data)
        finger_table: the finger table of the node (list of node_info dicts)
        keys: the keys stored within the node (dict where key: key, value: datatype)
    """

    def __init__(self, address: str) -> None:
        self.address = address
        self.id = self.generate_id()
        self.predecessor = {}
        self.successors = []
        self.data = {}
        self.finger_table = []
        self.keys = {}

    def generate_id(self) -> str:
        """
        Generates the unique id of the node.

        returns:
            id: the id of the node (str)
        """
        return hash_string(self.address)

    def generate_node_info(self) -> dict:
        """
        Generates the node information.

        returns:
            node_info: the node information (dict)
        """
        node_info = {
            'address': self.address,
            'id': self.id,
            'successors': self.successors,
            'predecessor': self.predecessor,
        }
        return node_info

    def join(self, successor_address: str = None) -> None:
        """
        Joins the node to the chord ring.
        """
        self.finger_table = initialize_finger_table(self.id)
        if successor_address is None:
            self.reset_successors(self.generate_node_info())
        else:
            self.reset_successors(remote_procedure_call(
                successor_address, 'find_successor', (self.id,)))

        create_finger_table(self)

    def quit(self) -> None:
        """
        Removes the node from the chord ring.
        """
        self.update_others(self.successors[0])
        remote_procedure_call(
            self.successors[0]['address'], 'reset_predecessor', (self.predecessor,))

        key_transfer_helper(self.keys, self.predecessor['address'], 'add')

    def find_predecessor(self, target_id: str) -> dict:
        """
        Finds the predecessor of the node.

        args:
            target_id: the id of the node to be searched for (str)
        returns:
            predecessor: the predecessor of the node (Node)
        """
        node_info = self.generate_node_info()
        node_id = node_info['id']
        successor_id = self.successors[0]['id']
        while not circular_range_check(target_id, node_id, successor_id):
            if node_id == self.id:
                # node_info = self.closest_preceding_node(target_id)
                i = RING_SIZE - 1
                while i >= 0:
                    node_info = self.finger_table[i]['node_id']
                    if circular_range_check(node_info['id'], self.id, target_id):
                        node_info = remote_procedure_call(
                            node_info['address'], 'get_node_info', ())
                    i -= 1

                if node_info['id'] == self.id:
                    node_info = self.successors[0]

            else:
                node_info = remote_procedure_call(
                    node_info['address'], 'closest_preceding_node', (target_id,))

            # reassign node_id and successor_id since the RPC may change them
            node_id, successor_id = node_info['id'], node_info['successors'][0]['id']
        return node_info

    def reset_predecessor(self, node_info: dict) -> None:
        """
        Resets a node's predecessor

        args:
            node_info: the node information (dict)
        """
        predecessor = {'address': node_info['address'], 'id': node_info['id']}
        self.predecessor = predecessor

    def find_successor(self, target_id: str) -> dict:
        """
        Finds the successor of the node.

        args:
            target_id: the id of the node to be searched for (str)
        returns:
            successor: the successor of the node (as a node_info dict)
        """
        predecessor = self.find_predecessor(target_id)

        if len(predecessor['successors']) == 0:
            return self.generate_node_info()
        else:
            return predecessor['successors'][0]

    def reset_successors(self, node_info: dict) -> None:
        """
        Resets a node's successors

        args:
            node_info: the node information (dict)
        """
        successor = {'address': node_info['address'], 'id': node_info['id']}
        self.successors = [successor]

    def update_others(self, node_info: dict) -> None:
        """
        Updates the other nodes in the ring.

        args:
            node_info: the node information (dict)
        """
        for i in range(RING_SIZE):
            predecessor = self.find_predecessor(
                (self.id - (2 ** i - 1)) % (2 ** RING_SIZE))
            if predecessor['id'] != self.id:
                remote_procedure_call(
                    predecessor['address'], 'update_finger_table', (node_info, str(i)))

    def key_rpc_interface(self, call_type: str, address: str, key: str, value: str = None):
        """
        Determines which key-related call to make and sends it via an RPC.

        args:
            call_type: the type of call to be made (str)
            address: the address of the node to be called (str)
            key: the key to be modified (str)
            value: the value to be modified (str) (optional)

        returns:
            response: the response from the RPC (tuple in the form of ()
        """

        successor_info = self.find_successor(hash_string(key))

        if int(successor_info['id']) == int(self.id):
            return key_rpc_helper(address, call_type, self.keys, key, value)
        else:
            return remote_procedure_call(successor_info['address'],
                                         'key_rpc_interface', (call_type, key, value))


def test():
    """
    Tests the node functionality.
    """

    ADDRESS = "0.0.0.0:4242"
    addr = build_tcp_address(ADDRESS)
    node = Node(addr)
