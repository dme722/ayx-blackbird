from ..proxies import FieldProxy, RecordProxy
from ..utilities import fill_df_nulls_with_blackbird_nulls


def generate_records_from_df(df, record_info):
    fill_df_nulls_with_blackbird_nulls(df)
    columns = list(df)
    values = df.values.tolist()
    fields = {field.name: FieldProxy(field) for field in record_info}

    record_creator = record_info.construct_record_creator()

    for row in values:
        record_creator.reset()
        record_proxy = RecordProxy(record_creator=record_creator)
        for col_idx, column in enumerate(columns):
            fields[column].set(record_proxy, row[col_idx])

        yield record_proxy
