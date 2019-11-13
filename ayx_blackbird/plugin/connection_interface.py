from collections import defaultdict
from enum import Enum

from .observable_mixin import ObservableMixin
from .record_container import RecordContainer


class ConnectionStatus(Enum):
    CREATED = 0
    INITIALIZED = 1
    RECEIVING_RECORDS = 2
    CLOSED = 3


class ConnectionInterface(ObservableMixin):
    def __init__(self, plugin, connection_name):
        super().__init__()
        self.name = connection_name
        self.record_container = None
        self.record_info = None
        self.progress_percentage = 0.0
        self.status = ConnectionStatus.CREATED
        self.plugin_initialization_success = True

        plugin.subscribe("all_connections_initialized", self.plugin_initialization_callback)

        self._plugin = plugin

    def plugin_initialization_callback(self, value):
        self.plugin_initialization_success = bool(value)

    def ii_init(self, record_info):
        self.record_info = record_info
        self.record_container = RecordContainer(self.record_info)
        self.status = ConnectionStatus.INITIALIZED

        self.notify_topic("connection_initialized", self)

        return self.plugin_initialization_success

    def ii_push_record(self, record):
        self.status = ConnectionStatus.RECEIVING_RECORDS

        self.record_container.add_record(record)

        self.notify_topic("record_received", self)

        return True

    def ii_update_progress(self, d_percent):
        self.progress_percentage = max(d_percent, 0)
        self._plugin.update_progress()

    def ii_close(self):
        self.status = ConnectionStatus.CLOSED
        # self._plugin.connection_closed_callback()
        self.notify_topic("connection_closed", self)

