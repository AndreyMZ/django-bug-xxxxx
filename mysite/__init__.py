import os
import threading

import django.db
import django.db.utils


class ConnectionHandler(django.db.utils.ConnectionHandler):
	def __init__(self, databases=None):
		self._databases = databases
		if os.environ.get('DJANGO_ALLOW_ASYNC_REUSE_DB_CONNECTIONS'):
			self._connections = threading.local()
		else:
			self._connections = django.db.utils.Local(thread_critical=True)

def django_db_connections_exist() -> bool:
	# noinspection PyProtectedMember
	connections = django.db.connections._connections
	databases = django.db.connections.databases
	return any(getattr(connections, alias, None) for alias in databases)

def monkey_patch_django_db_connections():
	assert not django_db_connections_exist()
	django.db.connections = ConnectionHandler()


# Uncomment if you want to do this.
# monkey_patch_django_db_connections()
