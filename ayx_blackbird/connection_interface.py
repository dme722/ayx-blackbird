from enum import Enum

from .record_container import RecordContainer

class ConnectionStatus(Enum):
    CREATED = 0
    INITIALIZED = 1
    RECEIVING_RECORDS = 2
    CLOSED = 3

class ConnectionInterface:
    def __init__(self, plugin, input_anchor, connection_name):
        self._plugin = plugin
        self._input_anchor = input_anchor
        self.name = connection_name

        self._record_info = None
        self._record_container = None
        self.progress_percentage = 0.0
        self.status = ConnectionStatus.CREATED

    def parse_records(self, format):
        return self._record_container.parse_records(format)

    def clear_records(self):
        self.clear_records()

    @property
    def record_list(self):
        if self.status == ConnectionStatus.CREATED:
            raise RuntimeError("Connection Interface must be initialized before record list can be accessed.")

        return self._record_container.record_list

    def ii_init(self, record_info):
        self._record_info = record_info
        self._record_container = RecordContainer(self._record_info)
        self.status = ConnectionStatus.INITIALIZED

        return self._plugin.connection_initialized_callback()

    def ii_push_record(self, record):
        if self._plugin.update_only_mode or not self._plugin.all_connections_initialized:
            return False

        self.status = ConnectionStatus.RECEIVING_RECORDS

        self._record_container.add_record(record)

        self._plugin.single_record_received_callback()

        return True

    def ii_update_progress(self, d_percent):
        if self._plugin.update_only_mode:
            return

        self.progress_percentage = d_percent
        self._plugin.update_progress()

    def ii_close(self):
        self.status = ConnectionStatus.CLOSED
        self._plugin.connection_closed_callback()

