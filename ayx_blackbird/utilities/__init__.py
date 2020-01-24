from .constants import NULL_VALUE_PLACEHOLDER


def fill_df_nulls_with_blackbird_nulls(df):
    df.fillna(NULL_VALUE_PLACEHOLDER, inplace=True)
