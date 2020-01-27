"""Utility definitions."""
from .constants import NULL_VALUE_PLACEHOLDER


def fill_df_nulls_with_blackbird_nulls(df):
    """Fill all dataframe null values with blackbird's representation."""
    df.fillna(NULL_VALUE_PLACEHOLDER, inplace=True)


__all__ = ["NULL_VALUE_PLACEHOLDER", "fill_df_nulls_with_blackbird_nulls"]
