from AlteryxPythonSDK import AlteryxEngine, FieldType, RecordInfo, RecordRef

from ayx_blackbird.anchors import InputAnchor
from ayx_blackbird.core import ConnectionEvents, ConnectionInterface, PluginEvents
from ayx_blackbird.mixins import ObservableMixin
from ayx_blackbird.utilities.constants import ConnectionStatus

import pytest


class MockPlugin(ObservableMixin):
    pass


class MockRecordContainer:
    def __init__(self):
        self.records = []

    def clear_records(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)


@pytest.fixture
def connection_interface() -> ConnectionInterface:
    connection_name = "#1"
    anchor = InputAnchor("Input", False)

    return ConnectionInterface(
        plugin=MockPlugin(), connection_name=connection_name, anchor=anchor
    )


@pytest.fixture
def record_collection():
    record_info = RecordInfo(AlteryxEngine())
    record_info.add_field("a", FieldType.float)
    record_info.add_field("b", FieldType.float)

    record1 = RecordRef(record_info)
    record1.data["a"] = 123
    record1.data["b"] = 666.666

    record2 = RecordRef(record_info)
    record2.data["a"] = 456
    record2.data["b"] = 999.999

    records = [record1, record2]

    return record_info, records


def test_connection_interface_ii_init(
    connection_interface: ConnectionInterface, record_collection
):
    record_info = record_collection[0]

    assert connection_interface.record_info is None

    events = []
    connection_interface.subscribe(
        ConnectionEvents.CONNECTION_INITIALIZED, lambda **kwargs: events.append(kwargs)
    )

    connection_interface.ii_init(record_info=record_info)
    assert connection_interface.record_info is record_info
    assert len(events) == 1


def test_connection_interface_record_handling(
    connection_interface: ConnectionInterface, record_collection
):
    record_info, records = record_collection

    container = MockRecordContainer()
    connection_interface.add_record_container(container)

    events = []
    connection_interface.subscribe(
        ConnectionEvents.RECORD_RECEIVED, lambda **kwargs: events.append(kwargs)
    )

    for record in records:
        connection_interface.ii_push_record(record)

    assert len(events) == len(records)
    assert len(container.records) == len(records)

    connection_interface.clear_records()
    assert len(container.records) == 0


def test_plugin_initialization_callback():
    plugin = MockPlugin()
    connection_interface = ConnectionInterface(
        plugin=plugin,
        connection_name="Connection",
        anchor=InputAnchor(name="Input", optional=False),
    )

    assert not connection_interface.plugin_failed

    plugin.notify_topic(PluginEvents.PLUGIN_FAILURE)
    assert connection_interface.plugin_failed


def test_connection_interface_ii_update_progress(
    connection_interface: ConnectionInterface
):
    events = []
    connection_interface.subscribe(
        ConnectionEvents.PROGRESS_UPDATE, lambda **kwargs: events.append(kwargs)
    )

    assert connection_interface.progress_percentage == 0

    connection_interface.ii_update_progress(60)
    assert len(events) == 1
    assert connection_interface.progress_percentage == 60

    connection_interface.ii_update_progress(70)
    assert len(events) == 2
    assert connection_interface.progress_percentage == 70

    connection_interface.ii_update_progress(-20)
    assert len(events) == 3
    assert connection_interface.progress_percentage == 0


def test_connection_interface_ii_close(connection_interface: ConnectionInterface):
    events = []
    connection_interface.subscribe(
        ConnectionEvents.CONNECTION_CLOSED, lambda **kwargs: events.append(kwargs)
    )

    assert connection_interface.status == ConnectionStatus.CREATED
    connection_interface.ii_close()
    assert connection_interface.status == ConnectionStatus.CLOSED
    assert len(events) == 1
