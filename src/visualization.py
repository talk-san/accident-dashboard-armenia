"""
Reusable Plotly chart functions for interactive dashboard.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def accidents_over_time(df: pd.DataFrame, freq: str = "W") -> go.Figure:
    """Line chart of accident counts over time."""
    series = (
        df
        .resample(freq, on="timestamp")
        .size()
        .reset_index(name="count")
    )
    fig = px.line(
        series,
        x="timestamp",
        y="count",
        title=f"Accidents Over Time ({freq})",
        labels={"timestamp": "Date", "count": "Accident Count"},
        markers=True,
    )
    fig.update_layout(xaxis_title="Date", yaxis_title="Accidents")
    return fig


def by_hour_histogram(df: pd.DataFrame) -> go.Figure:
    """Histogram of accidents by hour of day."""
    fig = px.histogram(
        df,
        x="hour",
        nbins=24,
        title="Accidents by Hour of Day",
        labels={"hour": "Hour (0–23)", "count": "Accident Count"},
    )
    fig.update_layout(xaxis=dict(dtick=1), bargap=0.01)
    return fig


def cost_distribution(df: pd.DataFrame) -> go.Figure:
    """Box plot of accident repair costs by car brand."""
    top_brands = df["car_brand"].value_counts().nlargest(10).index
    subset = df[df["car_brand"].isin(top_brands)]
    fig = px.box(
        subset,
        x="car_brand",
        y="cost_midpoint",
        points="all",
        title="Repair Cost Distribution by Top 10 Car Brands",
        labels={"car_brand": "Car Brand", "cost_midpoint": "Cost (AMD)"},
    )
    fig.update_layout(xaxis_tickangle=-45, yaxis_title="Cost (AMD)")
    return fig
