"""Record utilities."""
from ..proxies import FieldProxy
from ..utilities import fill_df_nulls_with_blackbird_nulls


def generate_records_from_df(df, record_info):
    """Generate record creators from a dataframe."""
    fill_df_nulls_with_blackbird_nulls(df)
    columns = list(df)
    field_map = {field.name: FieldProxy(field) for field in record_info}
    fields = [field_map[column_name] for column_name in columns]

    record_creator = record_info.construct_record_creator()

    col_range = range(len(fields))
    for row in df.itertuples():
        record_creator.reset()
        for col_idx in col_range:
            fields[col_idx].set(record_creator, row[col_idx + 1])

        yield record_creator
