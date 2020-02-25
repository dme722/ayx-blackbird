"""Connection callback strategy definitions."""
from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

from .connection_interface import ConnectionInterface

if TYPE_CHECKING:
    from .base_plugin import BasePlugin


class ConnectionCallbackStrategy(ABC):
    """ABC for callback strategy."""

    __slots__ = ["plugin"]

    def __init__(self, plugin: "BasePlugin") -> None:
        """Construct a callback strategy."""
        self.plugin = plugin

    def update_progress_callback(self, **_: Any) -> None:
        """Update input progress percentage."""
        import numpy as np

        percent = float(
            np.mean(
                [
                    connection.progress_percentage
                    for anchor in self.plugin.input_anchors
                    for connection in anchor.connections
                ]
            )
        )

        self.plugin.engine.output_tool_progress(percent)

        for anchor in self.plugin.output_anchors:
            anchor.update_progress(percent)

    @abstractmethod
    def connection_initialized_callback(
        self, connection: ConnectionInterface, **_: Any
    ) -> None:
        """Run callback for connection initialization."""
        pass

    @abstractmethod
    def record_received_callback(
        self, connection: ConnectionInterface, **_: Any
    ) -> None:
        """Run callback for when a record is received."""
        pass

    @abstractmethod
    def connection_closed_callback(self, **_: Any) -> None:
        """Run callback for connection closing."""
        pass


class WorkflowRunConnectionCallbackStrategy(ConnectionCallbackStrategy):
    """Callback strategy for workflow runs."""

    def connection_initialized_callback(
        self, connection: ConnectionInterface, **_: Any
    ) -> None:
        """Run callback for connection initialization."""
        try:
            if not self.plugin.all_required_connections_connected:
                self.plugin.raise_missing_inputs()

            if not self.plugin.initialized:
                self.plugin.initialize_plugin()
                self.plugin.initialized = True

            if not self.plugin.failure_occurred:
                self.plugin.initialize_connection(connection)
        except Exception as e:
            self.plugin.handle_plugin_error(e)

    def record_received_callback(
        self, connection: ConnectionInterface, **_: Any
    ) -> None:
        """Process single records by batch size."""
        batch_size = self.plugin.record_batch_size
        if batch_size is None:
            return

        if (
            len(connection.record_containers[0].records) >= batch_size
            and not self.plugin.failure_occurred
        ):
            try:
                self.plugin.on_incoming_records(connection)
            except Exception as e:
                self.plugin.handle_plugin_error(e)

    def connection_closed_callback(self, **_: Any) -> None:
        """Process any remaining records and finalize."""
        if self.plugin.all_connections_closed:
            if not self.plugin.failure_occurred:
                try:
                    for anchor in self.plugin.input_anchors:
                        for connection in anchor.connections:
                            self.plugin.on_incoming_records(connection)
                    self.plugin.on_complete()
                    self.plugin.close_output_anchors()
                except Exception as e:
                    self.plugin.handle_plugin_error(e)


class UpdateOnlyConnectionCallbackStrategy(ConnectionCallbackStrategy):
    """Callback strategy for update only runs."""

    def connection_initialized_callback(
        self, connection: ConnectionInterface, **_: Any
    ) -> None:
        """Run callback for connection initialization."""
        try:
            if not self.plugin.all_required_connections_connected:
                self.plugin.raise_missing_inputs()

            if not self.plugin.initialized:
                self.plugin.initialize_plugin()
                self.plugin.initialized = True

            if not self.plugin.failure_occurred:
                self.plugin.initialize_connection(connection)
        except Exception as e:
            self.plugin.handle_plugin_error(e)

    def record_received_callback(
        self, connection: ConnectionInterface, **_: Any
    ) -> None:
        """Raise error since this should never be called in update only mode."""
        raise RuntimeError("Record received in update only mode.")

    def connection_closed_callback(self, **_: Any) -> None:
        """Close all anchors."""
        if self.plugin.all_connections_closed:
            if not self.plugin.failure_occurred:
                try:
                    self.plugin.close_output_anchors()
                except Exception as e:
                    self.plugin.handle_plugin_error(e)
