"""Connection class definitions."""
from typing import Any, List, Optional, TYPE_CHECKING

from AlteryxPythonSDK import RecordInfo, RecordRef

from .events import ConnectionEvents, PluginEvents
from ..mixins import ObservableMixin
from ..records import BaseRecordContainer
from ..utilities.constants import ConnectionStatus

if TYPE_CHECKING:
    from .base_plugin import BasePlugin
    from ..anchors import InputAnchor


class ConnectionInterface(ObservableMixin):
    """Connection interface definition."""

    __slots__ = [
        "name",
        "record_containers",
        "__record_info",
        "progress_percentage",
        "status",
        "plugin_failed",
        "anchor",
    ]

    def __init__(
        self, plugin: "BasePlugin", connection_name: str, anchor: "InputAnchor"
    ) -> None:
        """Instantiate a connection interface."""
        super().__init__()
        self.name = connection_name
        self.__record_info: Optional[RecordInfo] = None
        self.progress_percentage = 0.0
        self.status = ConnectionStatus.CREATED
        self.plugin_failed = False
        self.record_containers: List[BaseRecordContainer] = []
        self.anchor = anchor

        plugin.subscribe(
            PluginEvents.PLUGIN_INITIALIZED, self.plugin_initialization_callback
        )
        plugin.subscribe(PluginEvents.PLUGIN_FAILURE, self.plugin_failure_callback)

    @property
    def record_info(self) -> Optional[RecordInfo]:
        """Getter for record info."""
        return self.__record_info

    def add_record_container(self, container: BaseRecordContainer) -> None:
        """Add a new record container."""
        self.record_containers.append(container)

    def clear_records(self) -> None:
        """Clear all records for this connections containers."""
        for container in self.record_containers:
            container.clear_records()

    def plugin_initialization_callback(self, value: bool, **_: Any) -> None:
        """Set success of plugin initialization."""
        self.plugin_failed = not value

    def plugin_failure_callback(self, **_: Any) -> None:
        """Set failed status from plugin."""
        self.plugin_failed = True

    def ii_init(self, record_info: RecordInfo) -> bool:
        """Initialize the connection."""
        self.status = ConnectionStatus.INITIALIZED
        self.__record_info = record_info
        self.notify_topic(ConnectionEvents.CONNECTION_INITIALIZED, connection=self)

        return not self.plugin_failed

    def ii_push_record(self, record: RecordRef) -> bool:
        """Receive a record."""
        self.status = ConnectionStatus.RECEIVING_RECORDS

        for container in self.record_containers:
            container.add_record(record)

        self.notify_topic(ConnectionEvents.RECORD_RECEIVED, connection=self)

        return not self.plugin_failed

    def ii_update_progress(self, d_percent: float) -> None:
        """Update progress of incoming data."""
        self.progress_percentage = max(d_percent, 0)
        self.notify_topic(
            ConnectionEvents.PROGRESS_UPDATE, connection=self, percent=d_percent
        )

    def ii_close(self) -> None:
        """Close the connection."""
        self.status = ConnectionStatus.CLOSED
        self.notify_topic(ConnectionEvents.CONNECTION_CLOSED, connection=self)
