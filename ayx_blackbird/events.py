from enum import Enum


class ConnectionEvents(Enum):
    CONNECTION_INITIALIZED = "connection_initialized"
    RECORD_RECEIVED = "record_received"
    PROGRESS_UPDATE = "progress_update"
    CONNECTION_CLOSED = "connection_closed"


class PluginEvents:
    PLUGIN_INITIALIZED = "plugin_initialized"
