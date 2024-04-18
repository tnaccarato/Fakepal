from threading import Thread, Lock
import threading

from django.apps import AppConfig
from django.db.models.signals import post_migrate
from register import create_admin_account
from thrift_timestamp import server

# Global lock for Thrift server start
thrift_server_lock = Lock()


class RegisterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'register'

    def ready(self):
        # Check and start Thrift server in a new thread if not already running
        def start_server():
            with thrift_server_lock:
                if not hasattr(threading.current_thread(), 'thrift_server_started'):
                    server.start_thrift_server()
                    setattr(threading.current_thread(), 'thrift_server_started', True)

        thrift_server_thread = Thread(target=start_server)
        thrift_server_thread.daemon = True
        thrift_server_thread.start()

        # Connect the post_migrate signal
        post_migrate.connect(create_admin_account.create_admin_group_and_account, sender=self)
