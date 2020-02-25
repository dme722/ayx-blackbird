from AlteryxPythonSDK import AlteryxEngine, FieldType, RecordInfo, RecordRef

from ayx_blackbird.records import RawRecordContainer

import pandas as pd

import pytest


def test_raw_record_container_construction():
    record_info = RecordInfo(AlteryxEngine())
    record_info.add_field(field_name="a", field_type=FieldType.byte)
    record_info.add_field(field_name="b", field_type=FieldType.fixeddecimal)

    with pytest.raises(ValueError):
        RawRecordContainer(record_info, record_info)


def test_simple_raw_record_container():
    record_info = RecordInfo(AlteryxEngine())
    record_info.add_field(field_name="a", field_type=FieldType.byte)
    record_info.add_field(field_name="b", field_type=FieldType.fixeddecimal)

    container = RawRecordContainer(record_info)

    record1 = RecordRef(record_info)
    record1.data["a"] = 123
    record1.data["b"] = 666.666

    record2 = RecordRef(record_info)
    record2.data["a"] = 456
    record2.data["b"] = 999.999

    records = [record1, record2]

    for record in records:
        container.add_record(record)

    for input_record, saved_record in zip(records, container.records):
        assert input_record.data == saved_record.finalize_record().data

    df = pd.DataFrame({"b": [1000, 2000]})
    container.update_with_dataframe(df)

    assert container.records[0].finalize_record().data == {"a": 123, "b": 1000}
    assert container.records[1].finalize_record().data == {"a": 456, "b": 2000}

    df = pd.DataFrame({"b": [1000, 2000, 3000]})
    with pytest.raises(ValueError):
        container.update_with_dataframe(df)

    df = pd.DataFrame({"d": [1000, 2000]})
    with pytest.raises(RuntimeError):
        container.update_with_dataframe(df)

    container.clear_records()
    assert len(container.records) == 0


def test_mapped_raw_record_container():
    input_record_info = RecordInfo(AlteryxEngine())
    input_record_info.add_field(field_name="a", field_type=FieldType.byte)
    input_record_info.add_field(field_name="b", field_type=FieldType.fixeddecimal)

    storage_record_info = RecordInfo(AlteryxEngine())
    storage_record_info.add_field(field_name="c", field_type=FieldType.fixeddecimal)
    storage_record_info.add_field(field_name="d", field_type=FieldType.byte)

    field_map = {"a": "d", "b": "c"}

    container = RawRecordContainer(input_record_info, storage_record_info, field_map)

    record1 = RecordRef(input_record_info)
    record1.data["a"] = 123
    record1.data["b"] = 666.666

    record2 = RecordRef(input_record_info)
    record2.data["a"] = 456
    record2.data["b"] = 999.999

    records = [record1, record2]

    for record in records:
        container.add_record(record)

    for input_record, saved_record in zip(records, container.records):
        assert input_record.data["a"] == saved_record.finalize_record().data["d"]
        assert input_record.data["b"] == saved_record.finalize_record().data["c"]
