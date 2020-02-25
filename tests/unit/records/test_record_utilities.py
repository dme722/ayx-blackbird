from AlteryxPythonSDK import AlteryxEngine, FieldType, RecordInfo

from ayx_blackbird.records import generate_records_from_df

import pandas as pd


def test_generate_records_from_df():
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["Hello", "from", "blackbird"]})

    record_info = RecordInfo(AlteryxEngine())
    record_info.add_field(field_name="a", field_type=FieldType.byte)
    record_info.add_field(field_name="b", field_type=FieldType.v_string)

    record_generator = generate_records_from_df(df, record_info)

    num_rows, _ = df.shape

    for row, record in enumerate(record_generator):
        for column in list(df):
            assert record.finalize_record().data[column] == df[column][row]
