def post_fork(server, worker):
    from thrift_timestamp.server import ThriftServerSingleton
    server = ThriftServerSingleton()
    server.start_server()

certfile = '/home/ubuntu//webapps2024/webapps.crt'
keyfile = '/home/ubuntu/webapps2024/webapps.pem'
bind = '0.0.0.0:443'
