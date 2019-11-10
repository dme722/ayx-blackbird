from enum import Enum

from ayx_blackbird.connection.connection_metadata import ConnectionMetadata
from ayx_blackbird.records import RecordContainer

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
        self._metadata = None
        self.progress_percentage = 0.0
        self.status = ConnectionStatus.CREATED

    def ii_init(self, record_info):
        self._record_info = record_info
        self._record_container = RecordContainer(self._record_info)
        self._metadata = ConnectionMetadata.build_from_record_info(self._record_info)
        self.status = ConnectionStatus.INITIALIZED

        return self._plugin.notify_connection_initialized()
        

    def ii_push_record(self, record):
        if self._plugin.update_only_mode or not self._plugin.all_connections_initialized:
            return False

        self.status = ConnectionStatus.RECEIVING_RECORDS

        self._record_container.add_record(record)

        self._plugin.notify_single_record_received()

        return True

    def ii_update_progress(self, d_percent):
        if self._plugin.update_only_mode:
            return

        self.progress_percentage = d_percent
        self._plugin.update_progress()

    def ii_close(self):
        self.status = ConnectionStatus.CLOSED
        self._plugin.notify_connection_closed()

