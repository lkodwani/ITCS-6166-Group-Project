from nodes import CurrentNode
from threading import Thread
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer as RPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from yaml import safe_load


class ChordClient(ServerProxy):
    def __init__(self, host, port):
        ServerProxy.__init__(self, f'http://{host}:{port}')


class Handler(SimpleXMLRPCRequestHandler):
    """
    Class to handle requests to the XML-RPC server.

    attr:
        rpc_paths: the paths that the server will listen to (tuple of strings)
    """

    def __init__(self, rpc_paths: tuple = ('/rpc',)):
        self.rpc_paths = rpc_paths


class ChordServer(RPCServer):
    """
    Class to create an XML-RPC server, using properties from the CurrentNode class.

    attr:
        node: the current node for the server (CurrentNode)
    """

    def __init__(self, node: CurrentNode, config_file_path: str = 'config/default.yaml'):
        Thread.__init__(self)
        self.node = node
        self.tcp_server = self.load_tcp_configs(config_file_path)

    def load_tcp_configs(self, config_file_path: str):
        """
        Loads the TCP configurations from a YAML file.

        args:
            config_file_path: the path to the YAML file (str)
        """
        with open(config_file_path, 'r') as config_file:
            configs = safe_load(config_file)
            # more configs can be easily added here
            # consider making this more dynamic
            allow_none = configs['allow_none']

        return RPCServer((self.node.host, int(self.node.port)),
                         requestHandler=Handler, allow_none=allow_none)

    def start(self):
        """
        Registers the CurrentNode class with the XML-RPC server and starts the server.
        """
        self.tcp_server.register_instance(self.node)
        self.tcp_server.serve_forever()

    def stop(self):
        """
        Stops the XML-RPC server.
        """
        self.tcp_server.shutdown()
        self.tcp_server.server_close()
