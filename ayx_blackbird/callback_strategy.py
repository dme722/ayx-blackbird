from abc import ABC, abstractmethod

from .connection_interface import ConnectionInterface


class CallbackStrategy(ABC):
    def __init__(self, plugin):
        self.plugin = plugin

    def update_progress_callback(self, _: ConnectionInterface) -> None:
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

    def connection_initialized_callback(self, _: ConnectionInterface) -> bool:
        if self.plugin.all_connections_initialized:
            return self.plugin.initialize_plugin()

        return True

    @abstractmethod
    def single_record_received_callback(self, connection: ConnectionInterface) -> None:
        pass

    @abstractmethod
    def connection_closed_callback(self, _: ConnectionInterface) -> None:
        pass


class WorkflowRunCallbackStrategy(CallbackStrategy):
    def single_record_received_callback(self, connection: ConnectionInterface) -> None:
        if self.plugin.record_batch_size is None:
            return

        if len(connection.record_container) >= self.plugin.record_batch_size:
            self.plugin.process_records()

    def connection_closed_callback(self, _: ConnectionInterface) -> None:
        if self.plugin.all_connections_closed:
            self.plugin.process_records()
            self.plugin.on_complete()
            self.plugin.close_output_anchors()


class UpdateOnlyCallbackStrategy(CallbackStrategy):
    def single_record_received_callback(self, connection: ConnectionInterface) -> None:
        pass

    def connection_closed_callback(self, _: ConnectionInterface) -> None:
        if self.plugin.all_connections_closed:
            self.plugin.close_output_anchors()
