from AlteryxPythonSDK import AlteryxEngine, FieldType, RecordInfo, RecordRef

from ayx_blackbird.records import ParsedRecordContainer

import pandas as pd


def test_simple_parsed_record_container():
    record_info = RecordInfo(AlteryxEngine())
    record_info.add_field(field_name="a", field_type=FieldType.byte)
    record_info.add_field(field_name="b", field_type=FieldType.fixeddecimal)

    container = ParsedRecordContainer(record_info)

    record1 = RecordRef(record_info)
    record1.data["a"] = 123
    record1.data["b"] = 666.666

    record2 = RecordRef(record_info)
    record2.data["a"] = 456
    record2.data["b"] = 999.999

    records = [record1, record2]

    for record in records:
        container.add_record(record)

    df = container.build_dataframe()
    assert df.equals(pd.DataFrame({"a": [123, 456], "b": [666.666, 999.999]}))


def test_field_subset_parsed_record_container():
    record_info = RecordInfo(AlteryxEngine())
    record_info.add_field(field_name="a", field_type=FieldType.byte)
    record_info.add_field(field_name="b", field_type=FieldType.fixeddecimal)

    container = ParsedRecordContainer(record_info, field_names_to_parse=["a"])

    record1 = RecordRef(record_info)
    record1.data["a"] = 123
    record1.data["b"] = 666.666

    record2 = RecordRef(record_info)
    record2.data["a"] = 456
    record2.data["b"] = 999.999

    records = [record1, record2]

    for record in records:
        container.add_record(record)

    df = container.build_dataframe()
    assert df.equals(pd.DataFrame({"a": [123, 456]}))
