"""Functions for transforming data
"""

import datetime
import math

import pandas as pd
import src.exceptions as e
from pandas.api.types import is_datetime64_any_dtype as is_datetime


def copy_df(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of input dataframe"""
    return df.copy()


def round_minutes(df: pd.DataFrame, col: str = "time") -> pd.DataFrame:
    """Round datetime down to quarter hourly times."""
    if col not in df.columns:
        raise e.ColumnNotFoundException(col)

    if not is_datetime(df[col]):
        raise e.ColumnNotDatetimeException(col)

    df[col] = df[col].apply(
        lambda dt: datetime.datetime(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            15 * math.floor((float(dt.minute) + float(dt.second) / 60) / 15),
        ),
    )
    return df


def filter_dayofweek(df: pd.DataFrame, day: int = 4, col: str = "time") -> pd.DataFrame:
    """Filter dataframe for a specified day of the week"""
    if col not in df.columns:
        raise e.ColumnNotFoundException(col)

    if not is_datetime(df[col]):
        raise e.ColumnNotDatetimeException(col)

    df["dow"] = df[col].dt.dayofweek
    df = df.query(f"dow == {day}")
    return df.drop("dow", axis=1)


def filter_date(
    df: pd.DataFrame, after_date: str = None, before_date: str = None, col: str = "time"
) -> pd.DataFrame:
    """Filter dataframe for a specifed data range"""
    if col not in df.columns:
        raise e.ColumnNotFoundException(col)

    if not is_datetime(df[col]):
        raise e.ColumnNotDatetimeException(col)

    if after_date:
        df = df.query(f"{col} > '{after_date}'")
    if before_date:
        df = df.query(f"{col} < '{before_date}'")
    return df
