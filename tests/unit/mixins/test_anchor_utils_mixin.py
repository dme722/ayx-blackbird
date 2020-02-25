from ayx_blackbird.mixins import AnchorUtilsMixin
from ayx_blackbird.utilities.constants import ConnectionStatus
from ayx_blackbird.utilities.exceptions import AnchorNotFoundException

import pytest


class MockAnchor:
    def __init__(self, name, optional=False):
        self.name = name
        self.optional = optional
        self.metadata_pushed = False
        self.closed = False
        self.connections = []

    def push_metadata(self):
        self.metadata_pushed = True

    def close(self):
        self.closed = True


class MockConnection:
    def __init__(self):
        self.status = ConnectionStatus.CREATED


@pytest.fixture
def anchor_utils_mixin():
    inst = AnchorUtilsMixin()
    inst.input_anchors = [MockAnchor("Input1", True), MockAnchor("Input2", False)]
    inst.output_anchors = [MockAnchor("Output1"), MockAnchor("Output2")]

    return inst


def test_anchor_utils_mixin_push_all_metadata(anchor_utils_mixin):
    anchor_utils_mixin.push_all_metadata()
    for anchor in anchor_utils_mixin.output_anchors:
        assert anchor.metadata_pushed


def test_anchor_utils_mixin_close_output_anchors(anchor_utils_mixin):
    anchor_utils_mixin.close_output_anchors()
    for anchor in anchor_utils_mixin.output_anchors:
        assert anchor.closed


def test_anchor_utils_mixin_get_input_anchor(anchor_utils_mixin):
    anchor = anchor_utils_mixin.get_input_anchor("Input1")
    assert anchor is anchor_utils_mixin.input_anchors[0]

    with pytest.raises(AnchorNotFoundException):
        anchor_utils_mixin.get_input_anchor("afdsdfasadf")


def test_anchor_utils_mixin_get_output_anchor(anchor_utils_mixin):
    anchor = anchor_utils_mixin.get_output_anchor("Output1")
    assert anchor is anchor_utils_mixin.output_anchors[0]

    with pytest.raises(AnchorNotFoundException):
        anchor_utils_mixin.get_output_anchor("afdsdfasadf")


def test_anchor_utils_mixin_all_required_connections_connected(anchor_utils_mixin):
    assert not anchor_utils_mixin.all_required_connections_connected

    anchor_utils_mixin.input_anchors[1].connections.append(MockConnection())
    assert anchor_utils_mixin.all_required_connections_connected


def test_anchor_utils_mixin_all_connections_initialized(anchor_utils_mixin):
    assert anchor_utils_mixin.all_connections_initialized

    connection = MockConnection()
    anchor_utils_mixin.input_anchors[0].connections.append(connection)
    assert not anchor_utils_mixin.all_connections_initialized

    connection.status = ConnectionStatus.INITIALIZED
    assert anchor_utils_mixin.all_connections_initialized


def test_anchor_utils_mixin_all_connections_closed(anchor_utils_mixin):
    assert anchor_utils_mixin.all_connections_closed

    connection = MockConnection()
    anchor_utils_mixin.input_anchors[0].connections.append(connection)
    assert not anchor_utils_mixin.all_connections_closed

    connection.status = ConnectionStatus.INITIALIZED
    assert not anchor_utils_mixin.all_connections_closed

    connection.status = ConnectionStatus.CLOSED
    assert anchor_utils_mixin.all_connections_closed
