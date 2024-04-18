from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift_timestamp.gen_py.timestamp_service import TimestampService


class ThriftTimestampClient:
    """Thrift client to fetch the current timestamp from the Thrift server."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Implement the Singleton design pattern for the Thrift client."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host='localhost', port=9090):
        """Initialize the Thrift client with the host and port of the Thrift server."""
        self.host = host
        self.port = port

    def get_current_timestamp(self):
        """Fetch the current timestamp from the Thrift server."""
        try:
            # Create a Thrift client to connect to the server
            transport = TSocket.TSocket(self.host, self.port)
            transport = TTransport.TBufferedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            client = TimestampService.Client(protocol)
            # Open the connection to the server
            transport.open()
            # Fetch the current timestamp from the server
            timestamp = client.getCurrentTimestamp()
            # Close the connection to the server
            transport.close()
            return timestamp

        # Handle any exceptions that occur during the process
        except Exception as e:
            print("An error occurred while fetching the timestamp:", e)
            return None
