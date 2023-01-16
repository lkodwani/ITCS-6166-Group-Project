from hashlib import sha256
from rpc import ChordClient, ChordServer
from yaml import safe_load


class Node:
    """
    A base class for a node in a chord ring.

    attr:
        address: the address of the node (str)
        name: the name of the node (str)
        id: the id of the node (str)
    """

    def __init__(self, host: str, port: str, name: str):
        self.host = host
        self.port = port
        self.name = name
        self.id = self.generate_id()

    def generate_id(self):
        """
        Generates a unique id for the node using the host and port.

        returns:
            id: the id of the node (str) -- length will be 64 characters
        """
        id = sha256((self.host + self.port).encode()).hexdigest()
        return id


class CurrentNode(Node):
    """
    A class for the current user's node in the chord ring.

    attr:
        host: the ip address of the node (str) - Inherited from Node
        port: the port of the node (str) - Inherited from Node
        name: the name of the node (str) - Inherited from Node
        id: the id of the node (str) - Inherited from Node
        predecessor: the id of the predecessor node (str)
        finger_table: the finger table of the node (a dictionary of node ids as strings)
        server: the server object for the current node (Server)
        data: the data stored in the node (dict)
    """

    def __init__(self, host: str, port: str, name: str):
        super().__init__(host, port, name)
        self.predecessor = None
        self.finger_table = {}
        self.server = ChordServer(self)
        self.data = {}

    def get_successor(self):
        """
        Gets the successor node of the current node.

        returns:
            successor: the successor node (str)
        """
        return self.finger_table[0]

    def join(self, node: Node):
        """
        Joins the current node to an existing chord ring.

        args:
            node: the node to join (Node)
        """
        pass

    def update_finger_table(self, node_id, i):
        """
        Updates the finger table of the current node.

        args:
            node_id: the id of the node to update the finger table with (str)
            i: the index of the finger table to update (int)

        modifies:
            self.finger_table: the finger table of the current node (list of node ids as strings)
        """
        self.finger_table[i] = node_id

    def find_successor(self, key):
        """
        Finds the successor node of a given key by querying the current node's finger table.

        args:
            key: the key to find the successor node for (str)

        returns:
            successor: the successor node id (str)
        """
        for i in range(len(self.finger_table) - 1, -1, -1):
            if self.finger_table[i] >= key:
                return self.finger_table[i]
        return self.id
