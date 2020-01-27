"""Connection callback strategy definitions."""
from abc import ABC, abstractmethod

from .connection_interface import ConnectionInterface


class ConnectionCallbackStrategy(ABC):
    """ABC for callback strategy."""

    __slots__ = ["plugin"]

    def __init__(self, plugin):
        """Construct a callback strategy."""
        self.plugin = plugin

    def update_progress_callback(self, _: ConnectionInterface) -> None:
        """Update input progress percentage."""
        import numpy as np

        percent = np.mean(
            [
                connection.progress_percentage
                for anchor in self.plugin.input_anchors
                for connection in anchor.connections
            ]
        )

        self.plugin.engine.output_tool_progress(self.plugin.tool_id, percent)

        for anchor in self.plugin.output_anchors:
            anchor.update_progress(percent)

    @abstractmethod
    def connection_initialized_callback(self, connection: ConnectionInterface) -> None:
        """Run callback for connection initialization."""
        pass

    @abstractmethod
    def record_received_callback(self, connection: ConnectionInterface) -> None:
        """Run callback for when a record is received."""
        pass

    @abstractmethod
    def connection_closed_callback(self, _: ConnectionInterface) -> None:
        """Run callback for connection closing."""
        pass


class WorkflowRunConnectionCallbackStrategy(ConnectionCallbackStrategy):
    """Callback strategy for workflow runs."""

    def __init__(self, plugin):
        """Construct a callback."""
        super().__init__(plugin)
        self._num_records_since_processed = 0

    def connection_initialized_callback(self, _: ConnectionInterface) -> None:
        """Run callback for connection initialization."""
        if self.plugin.all_connections_initialized:
            self.plugin.set_record_containers()
            self.plugin.initialize_plugin()

    def record_received_callback(self, connection: ConnectionInterface) -> None:
        """Process single records by batch size."""
        self._num_records_since_processed += 1

        if self.plugin.record_batch_size is None:
            return

        if self._num_records_since_processed >= self.plugin.record_batch_size:
            self.plugin.process_records()
            self._num_records_since_processed = 0

    def connection_closed_callback(self, _: ConnectionInterface) -> None:
        """Process any remaining records and finalize."""
        if self.plugin.all_connections_closed:
            self.plugin.process_records()
            self.plugin.on_complete()
            self.plugin.close_output_anchors()


class UpdateOnlyConnectionCallbackStrategy(ConnectionCallbackStrategy):
    """Callback strategy for update only runs."""

    def connection_initialized_callback(self, _: ConnectionInterface) -> None:
        """Run callback for connection initialization."""
        if self.plugin.all_connections_initialized:
            self.plugin.initialize_plugin()

    def record_received_callback(self, connection: ConnectionInterface) -> None:
        """Raise error since this should never be called in update only mode."""
        raise RuntimeError("Record received in update only mode.")

    def connection_closed_callback(self, _: ConnectionInterface) -> None:
        """Close all anchors."""
        if self.plugin.all_connections_closed:
            self.plugin.close_output_anchors()
