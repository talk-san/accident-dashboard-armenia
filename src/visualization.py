"""
Reusable Plotly chart functions.
"""

import pandas as pd
import plotly.express as px


# ---------------------------------------------------------------------------
def accidents_over_time(df: pd.DataFrame, freq: str = "W") -> px.line:
    series = (
        df
        .resample(freq, on="timestamp")
        .size()
        .reset_index(name="count")
    )

    return px.line(
        series,
        x="timestamp",
        y="count",
        title=f"Accidents over time ({freq})",
        markers=True,
    )


def by_hour_histogram(df: pd.DataFrame) -> px.histogram:
    """Histogram of accidents by hour of day."""
    return px.histogram(
        df,
        x="hour",
        nbins=24,
        title="Accidents by hour of day",
        labels={"hour": "Hour (0‒23)", "count": "Accident count"},
    )


def cost_distribution(df: pd.DataFrame) -> px.box:
    """Box-and-scatter of accident cost midpoint by car brand."""
    top_brands = (
        df["car_brand"]
        .value_counts()
        .head(10)
        .index
    )
    subset = df[df["car_brand"].isin(top_brands)]
    return px.box(
        subset,
        x="car_brand",
        y="cost_midpoint",
        points="all",
        title="Accident cost distribution – top 10 car brands",
        labels={"car_brand": "Brand", "cost_midpoint": "Cost (AMD)"},
    )
