import os
from pathlib import Path

from ayx_blackbird.config import ToolConfiguration

cur_dir = os.path.abspath(os.path.dirname(__file__))
assets_dir = os.path.abspath(os.path.join(cur_dir, "..", "..", "assets"))
example_tool_dir = os.path.abspath(os.path.join(assets_dir, "mock_tool_location"))
no_tools_dir = os.path.abspath(os.path.join(assets_dir, "mock_tool_location_no_tools"))


def test_tool_config_construction(monkeypatch, output_anchor_mgr):
    dummy_tool_config = {"Hello", "World"}
    monkeypatch.setattr(
        ToolConfiguration, "get_tool_config", lambda *args: dummy_tool_config
    )

    tool_name = "test_tool"
    tool_config = ToolConfiguration(
        tool_name=tool_name, output_anchor_mgr=output_anchor_mgr
    )
    assert tool_config.tool_name == tool_name
    assert tool_config.output_anchor_mgr is output_anchor_mgr
    assert tool_config.tool_config == dummy_tool_config


def test_get_tool_config(output_anchor_mgr, tool_config_location_patch):
    tool_config_location_patch("passthrough_tool_config.xml")

    config = ToolConfiguration(
        tool_name="test_tool", output_anchor_mgr=output_anchor_mgr
    ).get_tool_config()

    assert (
        config["AlteryxJavaScriptPlugin"]["Properties"]["MetaInfo"]["Name"]
        == "Blackbird Passthrough"
    )


def test_get_tool_config_file_path(monkeypatch, output_anchor_mgr):
    monkeypatch.setattr(ToolConfiguration, "get_tools_location", lambda *args: ".")
    monkeypatch.setattr(ToolConfiguration, "get_tool_config", lambda *args: {})

    tool_name = "test_tool"
    assert ToolConfiguration(
        tool_name=tool_name, output_anchor_mgr=output_anchor_mgr
    ).get_tool_config_filepath() == Path(
        os.path.join(".", tool_name, f"{tool_name}Config.xml")
    )


def test_get_tools_location_user_path(monkeypatch, output_anchor_mgr):
    monkeypatch.setattr(ToolConfiguration, "get_tool_config", lambda *args: {})
    tool_config = ToolConfiguration(
        tool_name="ExampleTool", output_anchor_mgr=output_anchor_mgr
    )

    monkeypatch.setenv("APPDATA", example_tool_dir)
    monkeypatch.setenv("ALLUSERSPROFILE", no_tools_dir)
    assert tool_config.get_tools_location() == Path(example_tool_dir) / "Alteryx/Tools"


def test_get_tools_location_admin_path(monkeypatch, output_anchor_mgr):
    monkeypatch.setattr(ToolConfiguration, "get_tool_config", lambda *args: {})
    tool_config = ToolConfiguration(
        tool_name="ExampleTool", output_anchor_mgr=output_anchor_mgr
    )

    monkeypatch.setenv("APPDATA", no_tools_dir)
    monkeypatch.setenv("ALLUSERSPROFILE", no_tools_dir)
    assert tool_config.get_tools_location() == Path(no_tools_dir) / "Alteryx/Tools"


def test_build_input_anchors_single_input(
    passthrough_output_anchor_mgr, tool_config_location_patch
):
    tool_config_location_patch("passthrough_tool_config.xml")

    tool_config = ToolConfiguration(
        tool_name="test_tool", output_anchor_mgr=passthrough_output_anchor_mgr
    )

    input_anchors = tool_config.build_input_anchors()
    assert len(input_anchors) == 1

    anchor = input_anchors[0]
    assert anchor.name == "Input"
    assert not anchor.optional


def test_build_output_anchors_single_output(
    passthrough_output_anchor_mgr, tool_config_location_patch
):
    tool_config_location_patch("passthrough_tool_config.xml")

    tool_config = ToolConfiguration(
        tool_name="test_tool", output_anchor_mgr=passthrough_output_anchor_mgr
    )

    output_anchors = tool_config.build_output_anchors()
    assert len(output_anchors) == 1

    anchor = output_anchors[0]
    assert anchor.name == "Output"


def test_build_input_anchors_double_input(
    two_in_two_out_output_anchor_mgr, tool_config_location_patch
):
    tool_config_location_patch("two_in_two_out_tool_config.xml")

    tool_config = ToolConfiguration(
        tool_name="test_tool", output_anchor_mgr=two_in_two_out_output_anchor_mgr
    )

    input_anchors = tool_config.build_input_anchors()
    assert len(input_anchors) == 2
    assert input_anchors[0].name == "Input1"
    assert not input_anchors[0].optional
    assert input_anchors[1].name == "Input2"
    assert not input_anchors[1].optional


def test_build_output_anchors_double_output(
    two_in_two_out_output_anchor_mgr, tool_config_location_patch
):
    tool_config_location_patch("two_in_two_out_tool_config.xml")

    tool_config = ToolConfiguration(
        tool_name="test_tool", output_anchor_mgr=two_in_two_out_output_anchor_mgr
    )

    output_anchors = tool_config.build_output_anchors()
    assert len(output_anchors) == 2
    assert output_anchors[0].name == "Output1"
    assert not output_anchors[0].optional
    assert output_anchors[1].name == "Output2"
    assert not output_anchors[1].optional


def test_build_input_anchors_no_input(
    no_in_no_out_output_anchor_mgr, tool_config_location_patch
):
    tool_config_location_patch("no_in_no_out_tool_config.xml")

    tool_config = ToolConfiguration(
        tool_name="test_tool", output_anchor_mgr=no_in_no_out_output_anchor_mgr
    )

    input_anchors = tool_config.build_input_anchors()
    assert len(input_anchors) == 0


def test_build_output_anchors_no_output(
    no_in_no_out_output_anchor_mgr, tool_config_location_patch
):
    tool_config_location_patch("no_in_no_out_tool_config.xml")

    tool_config = ToolConfiguration(
        tool_name="test_tool", output_anchor_mgr=no_in_no_out_output_anchor_mgr
    )

    output_anchors = tool_config.build_output_anchors()
    assert len(output_anchors) == 0
