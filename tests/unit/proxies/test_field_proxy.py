from AlteryxPythonSDK import AlteryxEngine, FieldType, RecordCreator, RecordInfo

from ayx_blackbird.proxies import FieldProxy
from ayx_blackbird.utilities.constants import NULL_VALUE_PLACEHOLDER


def test_field_proxy():
    record_info = RecordInfo(AlteryxEngine())
    record_info.add_field(
        field_name="float",
        field_type=FieldType.float,
        size=1,
        scale=1,
        source="test.txt",
        description="Test description",
    )

    field_proxy = FieldProxy(record_info.fields[0])

    record_creator = RecordCreator(record_info)
    assert field_proxy.name == "float"

    field_proxy.set(record_creator, "10.0")
    assert field_proxy.get(record_creator.finalize_record()) == 10.0

    field_proxy.set(record_creator, NULL_VALUE_PLACEHOLDER)
    assert field_proxy.get(record_creator.finalize_record()) is None

    field_proxy.set_null(record_creator)
    assert field_proxy.get(record_creator.finalize_record()) is None
