from enum import Enum

from .record_container import RecordContainer


class ConnectionStatus(Enum):
    CREATED = 0
    INITIALIZED = 1
    RECEIVING_RECORDS = 2
    CLOSED = 3


class ConnectionInterface:
    def __init__(self, plugin, connection_name):
        self.name = connection_name
        self.record_container = None
        self.record_info = None
        self.progress_percentage = 0.0
        self.status = ConnectionStatus.CREATED

        self._plugin = plugin

    def ii_init(self, record_info):
        self.record_info = record_info
        self.record_container = RecordContainer(self.record_info)
        self.status = ConnectionStatus.INITIALIZED

        return self._plugin.connection_initialized_callback()

    def ii_push_record(self, record):
        if self._plugin.update_only_mode or not self._plugin.all_connections_initialized:
            return False

        self.status = ConnectionStatus.RECEIVING_RECORDS

        self.record_container.add_record(record)

        self._plugin.single_record_received_callback()

        return True

    def ii_update_progress(self, d_percent):
        if self._plugin.update_only_mode:
            return

        self.progress_percentage = max(d_percent, 0)
        self._plugin.update_progress()

    def ii_close(self):
        self.status = ConnectionStatus.CLOSED
        self._plugin.connection_closed_callback()

