from .connection_interface import ConnectionStatus


class AnchorUtilsMixin:
    def push_all_records(self) -> None:
        for anchor in self.output_anchors:
            anchor.push_records()

    def push_all_metadata(self) -> None:
        if not self._metadata_pushed:
            for anchor in self.output_anchors:
                anchor.push_metadata()

    def close_output_anchors(self) -> None:
        for anchor in self.output_anchors:
            anchor.close()

    def clear_all_input_records(self) -> None:
        for anchor in self.input_anchors:
            for connection in anchor.connections:
                connection.record_container.clear_records()

    @property
    def all_connections_initialized(self) -> bool:
        return all(
            [
                connection.status != ConnectionStatus.CREATED
                for anchor in self.input_anchors
                for connection in anchor.connections
            ]
        )

    @property
    def all_connections_closed(self) -> bool:
        return all(
            [
                connection.status == ConnectionStatus.CLOSED
                for anchor in self.input_anchors
                for connection in anchor.connections
            ]
        )
