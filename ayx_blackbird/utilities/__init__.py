"""Utility definitions."""
from typing import TYPE_CHECKING

from .constants import NULL_VALUE_PLACEHOLDER

if TYPE_CHECKING:
    import pandas as pd


def fill_df_nulls_with_blackbird_nulls(df: "pd.DataFrame") -> None:
    """Fill all dataframe null values with blackbird's representation."""
    df.fillna(NULL_VALUE_PLACEHOLDER, inplace=True)


__all__ = ["NULL_VALUE_PLACEHOLDER", "fill_df_nulls_with_blackbird_nulls"]
