"""Connection class definitions."""
from enum import Enum

from .events import ConnectionEvents, PluginEvents
from .observable_mixin import ObservableMixin
from .record_container import RecordContainer


class ConnectionStatus(Enum):
    """Connection states."""

    CREATED = 0
    INITIALIZED = 1
    RECEIVING_RECORDS = 2
    CLOSED = 3


class ConnectionInterface(ObservableMixin):
    """Connection interface definition."""

    def __init__(self, plugin, connection_name):
        """Instantiate a connection interface."""
        super().__init__()
        self.name = connection_name
        self.record_container = None
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

    def get_dataframe(self):
        return self.record_container.parse_to_df()

    def plugin_initialization_callback(self, value: bool):
        """Callback for when the plugin initialization code runs."""
        self.plugin_initialization_success = value

    def ii_init(self, record_info):
        """Initialize the connection."""
        self.status = ConnectionStatus.INITIALIZED
        self.__record_info = record_info
        self.record_container = RecordContainer(self.record_info)

        self.notify_topic(ConnectionEvents.CONNECTION_INITIALIZED, self)

        return self.plugin_initialization_success

    def ii_push_record(self, record):
        """Receive a record."""
        self.status = ConnectionStatus.RECEIVING_RECORDS
        self.record_container.add_record(record)
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

    def __len__(self):
        return len(self.record_container)

    def __iter__(self):
        yield from self.record_container
