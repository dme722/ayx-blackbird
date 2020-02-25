import AlteryxPythonSDK as Sdk

import pytest


@pytest.fixture
def output_anchor_map():
    return {"test_anchor1": Sdk.OutputAnchor(), "test_anchor2": Sdk.OutputAnchor()}


@pytest.fixture
def output_anchor_mgr(output_anchor_map):
    return Sdk.OutputAnchorManager(output_anchor_map)


@pytest.fixture
def passthrough_output_anchor_map():
    return {"Output": Sdk.OutputAnchor()}


@pytest.fixture
def passthrough_output_anchor_mgr(passthrough_output_anchor_map):
    return Sdk.OutputAnchorManager(passthrough_output_anchor_map)


@pytest.fixture
def two_in_two_out_output_anchor_map():
    return {"Output1": Sdk.OutputAnchor(), "Output2": Sdk.OutputAnchor()}


@pytest.fixture
def two_in_two_out_output_anchor_mgr(two_in_two_out_output_anchor_map):
    return Sdk.OutputAnchorManager(two_in_two_out_output_anchor_map)


@pytest.fixture
def no_in_no_out_output_anchor_mgr():
    return Sdk.OutputAnchorManager({})
