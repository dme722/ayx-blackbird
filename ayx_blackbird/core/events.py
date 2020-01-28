"""Observable event definitions."""
from enum import Enum


class ConnectionEvents(Enum):
    """Events for connection objects."""

    CONNECTION_INITIALIZED = "connection_initialized"
    RECORD_RECEIVED = "record_received"
    PROGRESS_UPDATE = "progress_update"
    CONNECTION_CLOSED = "connection_closed"


class PluginEvents:
    """Events for plugin objects."""

    PLUGIN_INITIALIZED = "plugin_initialized"
    PI_INIT = "pi_init"
    INCOMING_CONNECTION_ADDED = "pi_add_incoming_connection"
    OUTGOING_CONNECTION_ADDED = "pi_add_outgoing_connection"
    PI_CLOSE = "pi_close"
    PI_PUSH_ALL_RECORDS = "pi_push_all_records"
    PLUGIN_FAILURE = "plugin_failure"
