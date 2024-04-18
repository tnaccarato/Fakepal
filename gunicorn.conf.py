def post_fork(server, worker):
    from thrift_timestamp.server import ThriftServerSingleton
    server = ThriftServerSingleton()
    server.start_server()
