import AlteryxPythonSDK as Sdk

from ayx_blackbird.anchors import OutputAnchor
from ayx_blackbird.records import generate_records_from_df

import pandas as pd

import pytest


@pytest.fixture
def output_anchor(output_anchor_mgr):
    return OutputAnchor(
        name="test_anchor1", optional=False, output_anchor_mgr=output_anchor_mgr
    )


@pytest.fixture
def output_record_info():
    record_info = Sdk.RecordInfo(Sdk.AlteryxEngine())
    record_info.add_field("Field1", Sdk.FieldType.float)
    record_info.add_field("Field2", Sdk.FieldType.v_wstring)
    return record_info


@pytest.fixture
def output_records(output_record_info):
    df = pd.DataFrame({"Field1": [1, 2, 3], "Field2": ["Hello", "from", "blackbird"]})
    return generate_records_from_df(df, output_record_info)


def test_output_anchor_construction(output_anchor_mgr):
    anchor = OutputAnchor(
        name="test_anchor1", optional=False, output_anchor_mgr=output_anchor_mgr
    )

    assert anchor.name == "test_anchor1"
    assert not anchor.optional
    assert anchor.record_info is None

    anchor = OutputAnchor(
        name="test_anchor2", optional=True, output_anchor_mgr=output_anchor_mgr
    )

    assert anchor.name == "test_anchor2"
    assert anchor.optional
    assert anchor.record_info is None

    with pytest.raises(RuntimeError):
        OutputAnchor(
            name="fake_anchor", optional=False, output_anchor_mgr=output_anchor_mgr
        )


def test_record_info_setter(output_anchor, output_record_info):
    output_anchor.record_info = output_record_info

    assert output_anchor.record_info is output_record_info

    output_anchor.push_metadata()
    with pytest.raises(RuntimeError):
        output_anchor.record_info = output_record_info


def test_output_anchor_push_metadata(
    output_anchor_map, output_anchor_mgr, output_record_info
):
    anchor_name = list(output_anchor_map.keys())[0]
    output_anchor = OutputAnchor(
        name=anchor_name, optional=False, output_anchor_mgr=output_anchor_mgr
    )

    with pytest.raises(ValueError):
        output_anchor.push_metadata()

    output_anchor.record_info = output_record_info
    output_anchor.push_metadata()

    assert output_anchor_map[anchor_name].record_info is output_record_info

    with pytest.raises(RuntimeError):
        output_anchor.push_metadata()


def test_output_anchor_update_progress(output_anchor_map, output_anchor_mgr):
    anchor_name = list(output_anchor_map.keys())[0]
    output_anchor = OutputAnchor(
        name=anchor_name, optional=False, output_anchor_mgr=output_anchor_mgr
    )

    progress = 96.0
    output_anchor.update_progress(progress)

    assert output_anchor_map[anchor_name].progress == progress


def test_output_anchor_close(output_anchor_map, output_anchor_mgr):
    anchor_name = list(output_anchor_map.keys())[0]
    output_anchor = OutputAnchor(
        name=anchor_name, optional=False, output_anchor_mgr=output_anchor_mgr
    )

    assert not output_anchor_map[anchor_name].is_closed

    output_anchor.close()

    assert output_anchor_map[anchor_name].is_closed


def test_output_push_records(
    output_anchor_map, output_anchor_mgr, output_record_info, output_records
):
    anchor_name = list(output_anchor_map.keys())[0]
    output_anchor = OutputAnchor(
        name=anchor_name, optional=False, output_anchor_mgr=output_anchor_mgr
    )

    output_anchor.record_info = output_record_info

    with pytest.raises(RuntimeError):
        output_anchor.push_records(output_records)

    output_anchor.push_metadata()
    output_anchor.push_records(output_records)
