import AlteryxPythonSDK as Sdk

from ayx_blackbird.core import BasePlugin, ConnectionInterface, PluginEvents
from ayx_blackbird.records import generate_records_from_df

import pytest

import xmltodict


class SimplePlugin(BasePlugin):
    """Concrete implementation of an AyxPlugin."""

    def __init__(
        self,
        tool_id: int,
        alteryx_engine: Sdk.AlteryxEngine,
        output_anchor_mgr: Sdk.OutputAnchorManager,
    ):
        """Construct a plugin."""
        super().__init__(tool_id, alteryx_engine, output_anchor_mgr)
        self.output_anchor = None

    @property
    def tool_name(self) -> str:
        """Get the tool name."""
        return "BlackbirdPassthrough"

    @property
    def record_batch_size(self):
        """Get the record batch size."""
        return 10000

    def initialize_plugin(self) -> None:
        """Initialize plugin."""
        self.engine.info(self.engine.xmsg("Plugin initialized."))
        self.output_anchor = self.get_output_anchor("Output")

    def initialize_connection(self, connection: ConnectionInterface) -> None:
        """Initialize a connection."""
        super().initialize_connection(connection)
        self.output_anchor.record_info = connection.record_info.clone()
        self.push_all_metadata()

    def on_incoming_records(self, connection: ConnectionInterface) -> None:
        """Process records in batches."""
        input_df = connection.record_containers[0].build_dataframe()
        self.output_anchor.push_records(
            generate_records_from_df(input_df, self.output_anchor.record_info)
        )

        connection.clear_records()

    def on_complete(self) -> None:
        """Finalize the plugin."""
        self.engine.info(self.engine.xmsg("Completed processing records."))


@pytest.fixture
def simple_plugin(tool_config_location_patch, passthrough_output_anchor_mgr):
    tool_config_location_patch("passthrough_tool_config.xml")
    return SimplePlugin(
        1, Sdk.AlteryxEngine(), output_anchor_mgr=passthrough_output_anchor_mgr
    )


@pytest.fixture
def erroring_simple_plugin(
    monkeypatch, tool_config_location_patch, passthrough_output_anchor_mgr
):
    def raise_err(*_, **__):
        raise ValueError("Hello world")

    monkeypatch.setattr(SimplePlugin, "initialize_plugin", raise_err)

    tool_config_location_patch("passthrough_tool_config.xml")
    return SimplePlugin(
        1, Sdk.AlteryxEngine(), output_anchor_mgr=passthrough_output_anchor_mgr
    )


def test_base_plugin_construction(simple_plugin):
    assert simple_plugin.tool_id == 1
    assert len(simple_plugin.input_anchors) == 0
    assert len(simple_plugin.output_anchors) == 0
    assert not simple_plugin.initialized


def test_base_plugin_pi_init(simple_plugin):
    events = []
    simple_plugin.subscribe(
        PluginEvents.PLUGIN_INITIALIZED, lambda **kwargs: events.append(kwargs)
    )

    config = {"Configuration": {"Hello": "World"}}
    config_str = xmltodict.unparse(config, full_document=False)
    simple_plugin.pi_init(config_str)

    assert len(events) == 1


def test_passthrough_pi_push_all_records_errors(simple_plugin):
    simple_plugin.pi_init("<Configuration/>")
    assert not simple_plugin.pi_push_all_records(1000)


def test_passthrough_pi_add_incoming_connection(simple_plugin):
    simple_plugin.pi_init("<Configuration/>")

    assert len(simple_plugin.input_anchors[0].connections) == 0

    simple_plugin.pi_add_incoming_connection(anchor_name="Input", connection_name="#1")
    assert len(simple_plugin.input_anchors[0].connections) == 1


def test_passthrough_pi_add_outgoing_connection(simple_plugin):
    simple_plugin.pi_init("<Configuration/>")

    assert simple_plugin.output_anchors[0].num_connections == 0

    simple_plugin.pi_add_outgoing_connection(anchor_name="Output")
    assert simple_plugin.output_anchors[0].num_connections == 1
