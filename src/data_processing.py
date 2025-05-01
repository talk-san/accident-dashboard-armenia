"""
Load, clean and enrich Armenia-accident data.

"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

script_dir = Path(__file__).parent.absolute()
project_root = script_dir.parent

RAW_PATH = project_root / "data/raw/car_accidents.xlsx"
PROCESSED_PATH = project_root / "data/processed/accidents_clean.parquet"

# ---- helpers ----------------------------------------------------------------
_COST_RE = re.compile(r"(\d[\d,]*)-(\d[\d,]*)")


def _cost_midpoint(cost_str: str) -> float | None:
    """
    Convert a cost band like "300,001-400,000" to its midpoint (350000).

    Returns None if parsing fails.
    """
    if not isinstance(cost_str, str):
        return None
    m = _COST_RE.search(cost_str.replace("\u202f", ""))  # remove thin-spaces
    if not m:
        return None
    low, high = (int(v.replace(",", "")) for v in m.groups())
    return float(low + high) / 2


def _combine_date_and_time(date_ser: pd.Series, time_ser: pd.Series) -> pd.Series:
    """
    `date_hour` is stored as 1900-01-01 + time.  Remove the bogus base date and
    add the true accident date to obtain a full timestamp.
    """
    delta = time_ser - pd.Timestamp("1900-01-01")
    return date_ser + delta


# ---- public API -------------------------------------------------------------


def load_raw(path: str | Path = RAW_PATH) -> pd.DataFrame:
    """Read the Excel file exactly as provided."""
    return pd.read_excel(path)


def clean_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Return a tidy DataFrame suitable for analysis and plotting."""
    df = df_raw.copy()

    # --- timestamp -----------------------------------------------------------
    df["timestamp"] = _combine_date_and_time(df["date_accident"], df["date_hour"])

    # --- temporal columns ----------------------------------------------------
    df["hour"] = df["timestamp"].dt.hour
    df["weekday"] = df["timestamp"].dt.day_name()
    df["day"] = df["timestamp"].dt.day
    df["month"] = df["timestamp"].dt.month
    df["year"] = df["timestamp"].dt.year

    # --- filter years -------------------------------------------------------
    df = df[df["year"].isin([2018, 2019, 2020])]

    # --- locations -----------------------------------------------------------
    df["region"] = df["region"].str.strip().str.title()

    # --- car years -----------------------------------------------------------
    df = df[(df.car_year >= 1960) & (df.car_year <= pd.Timestamp.now().year)]

    # --- costs ---------------------------------------------------------------
    df["cost_range"] = df["cost"]
    df["cost_midpoint"] = df["cost_range"].apply(_cost_midpoint)

    # --- normalize genders ----------------------------------------------------
    df["gender"] = (
        df["gender"]
        .str.strip()
        .str.lower()
        .map({"male": "M", "female": "F"})
    )
    df = df[df["gender"].isin(["M", "F"])]

    # --- rename & reorder ----------------------------------------------------
    desired = [
        "timestamp",
        "hour",
        "weekday",
        "day",
        "month",
        "year",
        "region",
        "gender",
        "type",
        "age",
        "car_brand",
        "car_year",
        "cost_range",
        "cost_midpoint",
    ]
    df = df[desired]

    return df


def write_clean(df: pd.DataFrame, out: str | Path = PROCESSED_PATH) -> None:
    """Write cleaned DataFrame to parquet."""
    try:
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(out, index=False)
        if out.exists():
            print(f"Successfully wrote {out.name}")
        else:
            raise FileNotFoundError(f"Failed to write {out}")
    except Exception as e:
        print(f"Error writing to {out}: {str(e)}")
        raise


def load_processed(path: str | Path = PROCESSED_PATH) -> pd.DataFrame:
    """Load the pre-cleaned parquet."""
    return pd.read_parquet(path)
