import os
import sys
from thrift_timestamp.server import ThriftServerSingleton


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapps2024.settings')
    try:
        from django.core.management import execute_from_command_line
        from threading import Thread
        from thrift_timestamp import server
        thrift_server = ThriftServerSingleton()
        thrift_server_thread = Thread(target=thrift_server.start_server)
        thrift_server_thread.daemon = True
        thrift_server_thread.start()

        execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

if __name__ == '__main__':
    main()
