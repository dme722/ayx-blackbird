"""Connection class definitions."""
from .events import ConnectionEvents, PluginEvents
from ..mixins import ObservableMixin
from ..utilities.constants import ConnectionStatus


class ConnectionInterface(ObservableMixin):
    """Connection interface definition."""
    __slots__ = ["name", "record_accumulator", "__record_info", "progress_percentage", "status", "plugin_initialization_success"]

    def __init__(self, plugin, connection_name, record_accumulator):
        """Instantiate a connection interface."""
        super().__init__()
        self.name = connection_name
        self.record_accumulator = record_accumulator
        self.__record_info = None
        self.progress_percentage = 0.0
        self.status = ConnectionStatus.CREATED
        self.plugin_initialization_success = True

        plugin.subscribe(
            PluginEvents.PLUGIN_INITIALIZED, self.plugin_initialization_callback
        )

    @property
    def record_info(self):
        """Getter for record info."""
        return self.__record_info

    def plugin_initialization_callback(self, value: bool):
        """Callback for when the plugin initialization code runs."""
        self.plugin_initialization_success = value

    def ii_init(self, record_info):
        """Initialize the connection."""
        self.status = ConnectionStatus.INITIALIZED
        self.__record_info = record_info
        self.record_accumulator.set_record_info_in(self.record_info)

        self.notify_topic(ConnectionEvents.CONNECTION_INITIALIZED, self)

        return self.plugin_initialization_success

    def ii_push_record(self, record):
        """Receive a record."""
        self.status = ConnectionStatus.RECEIVING_RECORDS
        self.record_accumulator.add_raw_record(record)
        self.notify_topic(ConnectionEvents.RECORD_RECEIVED, self)

        return True

    def ii_update_progress(self, d_percent: float):
        """Update progress of incoming data."""
        self.progress_percentage = max(d_percent, 0)
        self.notify_topic(ConnectionEvents.PROGRESS_UPDATE, self)

    def ii_close(self):
        """Close the connection."""
        self.status = ConnectionStatus.CLOSED
        self.notify_topic(ConnectionEvents.CONNECTION_CLOSED, self)
