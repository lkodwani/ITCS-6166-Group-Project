from common.utils import circular_range_check, remote_procedure_call
from config.consts import RING_SIZE
from network.nodes import Node


def initialize_finger_table(node_id: str) -> list:
    """
    Initializes the finger table of the node, only called when the node is the first node in the ring.
    """
    finger_table = []
    for i in range(RING_SIZE):
        # might need to be 2 ** i not 2 ** i - 1
        start_point = (node_id + (2 ** i - 1)) % (2 ** RING_SIZE)
        finger_table.append({'start_point': start_point})

    return finger_table


def create_finger_table(node: Node) -> None:
    """
    Creates the finger table for the given node.
    """

    if len(node.successors) > 0:

        node_info = remote_procedure_call(
            node.successors[0]['address'], 'find_successor',
            (node.finger_table[0]['start_point'],))

        node.successors.append(node_info)
        node.finger_table[0]['node_info'] = node_info

        node_info = remote_procedure_call(
            node.successors[0]['address'], 'get_node_info', ())
        node.predecessor = node_info['predecessor']

        remote_procedure_call(
            node_info['address'], 'reset_predecessor', (node.generate_node_info(),))

        for i in range(1, RING_SIZE):
            start = node.finger_table[i]['start_point']
            end = node.finger_table[i - 1]['start_point']
            if circular_range_check(start, node.id, end):
                node.finger_table[i]['node_info'] = node.finger_table[i - 1]['node_info']
            else:
                node.finger_table[i]['node_info'] = remote_procedure_call(
                    node.successors[0]['address'], 'find_successor', (start,))

        node.update_others(node.generate_node_info())

        keys = remote_procedure_call(
            node.successors[0]['address'], 'get_preceeding_keys', (node.id,))

        for key in keys:
            node.keys[key] = keys[key]

    else:
        for i in range(RING_SIZE):
            node.finger_table[i]['node_info'] = node.generate_node_info()
        node.reset_successors(node.generate_node_info())


def update_finger_table(node: Node, node_info: dict, finger_id: str) -> None:
    """
    Updates the finger table of the node.

    args:
        node_info: the node information (dict)
        finger_id: the id of the finger to be updated (str)
    """
    finger_id = int(finger_id)
    start = node_info['id']
    end = node.finger_table[finger_id]['node_info']['id']

    if node.id == node_info['id'] or circular_range_check(start, end, node.id):

        node.finger_table[finger_id]['node_info'] = node_info
        node.reset_successors(node_info) if finger_id == 0 else None
