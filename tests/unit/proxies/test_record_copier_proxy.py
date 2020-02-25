from AlteryxPythonSDK import AlteryxEngine, FieldType, RecordInfo, RecordRef

from ayx_blackbird.proxies import RecordCopierProxy


def test_record_copier_proxy():
    engine = AlteryxEngine()

    input_record_info = RecordInfo(engine)
    output_record_info = RecordInfo(engine)

    field_props = [
        {"field_name": "a", "field_type": FieldType.int32},
        {"field_name": "b", "field_type": FieldType.v_wstring},
    ]

    for props in field_props:
        input_record_info.add_field(**props)
        output_record_info.add_field(**props)

    record_copier_proxy = RecordCopierProxy(
        input_record_info, output_record_info, {"a": "a", "b": "b"}
    )

    record = RecordRef(input_record_info)
    record.data["a"] = 123
    record.data["b"] = "Hello world"

    record_copier = record_copier_proxy.copy(record)

    assert record == record_copier.finalize_record()
    assert record is not record_copier.finalize_record()
