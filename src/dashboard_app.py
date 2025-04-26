from __future__ import annotations

import streamlit as st
import pandas as pd

from data_processing import load_raw, clean_data, write_clean, load_processed
import visualization as vz


@st.cache_data(show_spinner=False)
def get_data() -> pd.DataFrame:
    try:
        return load_processed()
    except FileNotFoundError:
        df_clean = clean_data(load_raw())
        write_clean(df_clean)
        return df_clean


# ----------------------------------------------------------------------------
def main() -> None:
    st.set_page_config("Armenia Accident Dashboard", layout="wide")
    st.title("Armenia – Accident Risk & Cost Dashboard")

    df = get_data()

    # ----- sidebar filters ---------------------------------------------------
    st.sidebar.header("Filters")

    min_d, max_d = df["timestamp"].dt.date.min(), df["timestamp"].dt.date.max()
    date_from, date_to = st.sidebar.date_input(
        "Date range", value=(min_d, max_d), min_value=min_d, max_value=max_d
    )

    regions = sorted(df["region"].dropna().unique())
    region_sel = st.sidebar.multiselect("Region", regions, default=regions)

    list(range(24))
    hour_sel = st.sidebar.slider("Hour of day", 0, 23, (0, 23))

    # ----- apply filters -----------------------------------------------------
    mask = (
        (df["timestamp"].dt.date >= date_from)
        & (df["timestamp"].dt.date <= date_to)
        & (df["region"].isin(region_sel))
        & (df["hour"].between(hour_sel[0], hour_sel[1]))
    )
    dff = df.loc[mask]
    fig = vz.accidents_over_time(dff)
    st.plotly_chart(fig, use_container_width=True, key="accidents_overview")

    st.markdown(
        f"Showing **{len(dff):,}** accidents "
        f"from **{date_from}** to **{date_to}** "
        f"in selected regions."
    )

    # ----- layout ------------------------------------------------------------
    st.plotly_chart(vz.by_hour_histogram(dff), use_container_width=True, key="hour_hist")
    st.plotly_chart(vz.cost_distribution(dff), use_container_width=True, key="cost_dist")

    st.caption(
        "Data source: Armenian accident registry (2020 update). "
        "Costs mapped to band mid-points for indicative visualisation."
    )


if __name__ == "__main__":
    main()
