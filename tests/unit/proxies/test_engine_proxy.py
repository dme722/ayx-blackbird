from AlteryxPythonSDK import AlteryxEngine, RecordInfo

from ayx_blackbird.config import WorkflowConfiguration
from ayx_blackbird.proxies import EngineProxy

import pytest

import xmltodict


@pytest.fixture
def engine_proxy():
    return EngineProxy(AlteryxEngine(), 1)


def test_xmsg(engine_proxy):
    string = "Hello world"
    assert engine_proxy.xmsg(string) == string


def test_error(engine_proxy):
    error = "Error occurred"
    engine_proxy.error(error)

    errors = engine_proxy.engine.tool_execution_info[1].errors
    assert len(errors) == 1
    assert errors[0] == error


def test_warning(engine_proxy):
    warning = "Warning occurred"
    engine_proxy.warning(warning)

    warnings = engine_proxy.engine.tool_execution_info[1].warnings
    assert len(warnings) == 1
    assert warnings[0] == warning


def test_info(engine_proxy):
    info = "Info occurred"
    engine_proxy.info(info)

    infos = engine_proxy.engine.tool_execution_info[1].infos
    assert len(infos) == 1
    assert infos[0] == info


def test_update_only(engine_proxy):
    engine_proxy.engine.init_vars["UpdateOnly"] = "False"
    assert not engine_proxy.update_only_mode

    engine_proxy.engine.init_vars["UpdateOnly"] = "True"
    assert engine_proxy.update_only_mode


def test_update_config_xml(engine_proxy):
    config_str = xmltodict.unparse({"Configuration": {"Value": "123"}})
    config = WorkflowConfiguration(config_str)

    engine_proxy.update_config_xml(config)
    assert engine_proxy.engine.tool_execution_info[1].output_workflow_xml is None

    config["Value"] = "456"
    engine_proxy.update_config_xml(config)
    assert engine_proxy.engine.tool_execution_info[1].output_workflow_xml is not None


def test_output_tool_progress(engine_proxy):
    progress = 0.66
    engine_proxy.output_tool_progress(progress)
    assert engine_proxy.engine.tool_execution_info[1].progress == progress


def test_create_record_info(engine_proxy):
    assert isinstance(engine_proxy.create_record_info(), RecordInfo)


def test_create_temp_file(engine_proxy):
    assert engine_proxy.create_temp_file().endswith(".tmp")
