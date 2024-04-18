from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift_timestamp.gen_py.timestamp_service import TimestampService
import socket
from datetime import datetime


class ThriftServerSingleton:
    """Singleton class to manage the Thrift server."""
    _instance = None # The instance of the Thrift server

    def __new__(cls, *args, **kwargs):
        """Implement the Singleton design pattern for the Thrift server."""
        if not cls._instance:
            print("Creating the Thrift server instance")
            cls._instance = super().__new__(cls) # Create the instance
            cls._instance._server = None # The Thrift server object
            cls._instance._server_running = False # Flag to indicate if the server is running
        return cls._instance # Return the instance

    def _port_is_available(self, port):
        """Check if the specified port is available on the local host."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) != 0

    def start_server(self):
        """Start the Thrift server."""
        # Check if the server is already running
        if self._instance._server_running:
            print("Thrift server is already running.")
            return # Exit the function

        # Check if the port is available
        if not self._instance._port_is_available(9090):
            print("Port 9090 is already in use. Please stop the existing server.")
            return

        # Create the Thrift server
        handler = TimestampHandler()
        processor = TimestampService.Processor(handler)
        transport = TSocket.TServerSocket(port=9090)
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()

        # Start the server loop
        self._instance._server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
        print("Starting the Thrift server...")
        self._instance._server_running = True
        while self._instance._server_running:
            self._instance._server.serve()

    def stop_server(self):
        """Stop the Thrift server."""
        if not self._instance._server_running:
            print("Thrift server is not running.")
            return

        print("Stopping the Thrift server...")
        self._instance._server.stop()
        self._instance._server_running = False


class TimestampHandler:
    def getCurrentTimestamp(self):
        """Return the current timestamp in the format 'YYYY-MM-DD HH:MM:SS'"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")