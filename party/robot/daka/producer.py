from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from robot.msg_queue import put


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


def producer():
    # Create server
    with SimpleXMLRPCServer(('localhost', 12345),
                            requestHandler=RequestHandler) as server:
        server.register_introspection_functions()
        server.register_function(put)
        # Run the server's main loop
        server.serve_forever()
