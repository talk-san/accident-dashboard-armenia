from __future__ import annotations
import streamlit as st
import pandas as pd

from data_processing import load_raw, clean_data, write_clean, load_processed
from visualization import (
    accidents_over_time,
    by_hour_histogram,
    cost_distribution,
)

@st.cache_data(show_spinner=False)
def get_data() -> pd.DataFrame:
    try:
        return load_processed()
    except FileNotFoundError:
        df_clean = clean_data(load_raw())
        write_clean(df_clean)
        return df_clean

def main() -> None:
    st.set_page_config("Armenia Accident Dashboard", layout="wide")
    st.title("Armenia – Accident Risk & Cost Dashboard")

    st.markdown("""
        <style>
        div.stButton > button {
            width: 100%;
            font-size: 14px;
            padding: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    df = get_data()

    # ----- sidebar filters ---------------------------------------------------
    st.sidebar.header("Filters")

    min_d = df["timestamp"].dt.date.min()
    max_d = df["timestamp"].dt.date.max()
    date_from, date_to = st.sidebar.date_input(
        "Date range", value=(min_d, max_d), min_value=min_d, max_value=max_d
    )

    reg_col1, reg_col2 = st.sidebar.columns(2)

    # Region selector
    regions = sorted(df["region"].dropna().unique())
    if "region_sel" not in st.session_state:
        st.session_state.region_sel = regions.copy()
    if reg_col1.button("Select all regions"):
        st.session_state.region_sel = regions.copy()
    if reg_col2.button("Clear regions"):
        st.session_state.region_sel = []
    region_sel = st.sidebar.multiselect(
        "Region",
        regions,
        key="region_sel",
    )

    brand_col1, brand_col2 = st.sidebar.columns(2)

    # Car brand selector
    brands = df["car_brand"].value_counts().nlargest(20).index.tolist()
    if "brand_sel" not in st.session_state:
        st.session_state.brand_sel = brands.copy()
    if brand_col1.button("Select all brands"):
        st.session_state.brand_sel = brands.copy()
    if brand_col2.button("Clear brands"):
        st.session_state.brand_sel = []
    brand_sel = st.sidebar.multiselect(
        "Car Brand (top 20)",
        brands,
        key="brand_sel",
    )

    hour_sel = st.sidebar.slider("Hour of day", 0, 23, (0, 23))
    age_sel = st.sidebar.slider("Age", 16, 80, (16, 80))

    # Gender selector
    genders = sorted(df["gender"].unique())
    if "gender_sel" not in st.session_state:
        st.session_state.gender_sel = genders.copy()
    gender_sel = st.sidebar.multiselect(
        "Gender",
        genders,
        key="gender_sel",
    )

    # ----- validate filters --------------------------------------------------
    if not region_sel or not brand_sel:
        st.warning("Please select at least one **Region** and one **Car Brand** to see the charts.")
        return

    # ----- apply filters -----------------------------------------------------
    mask = (
            (df["timestamp"].dt.date >= date_from)
            & (df["timestamp"].dt.date <= date_to)
            & (df["region"].isin(region_sel))
            & (df["car_brand"].isin(brand_sel))
            & (df["gender"].isin(gender_sel))
            & (df["hour"].between(hour_sel[0], hour_sel[1]))
            & (df["age"].between(age_sel[0], age_sel[1]))
    )
    dff = df.loc[mask]

    st.markdown(
        f"Showing **{len(dff):,}** accidents "
        f"from **{date_from}** to **{date_to}**, "
        f"hours **{hour_sel[0]}–{hour_sel[1]}**, "
        f"ages **{age_sel[0]}–{age_sel[1]}**, "
        f"{len(region_sel)} region(s), "
        f"{len(brand_sel)} brand(s), "
        f"{len(gender_sel)} gender(s)."
    )

    # ----- main charts -----------------------------------------------
    st.plotly_chart(accidents_over_time(dff), use_container_width=True)
    st.plotly_chart(by_hour_histogram(dff),   use_container_width=True)
    st.plotly_chart(cost_distribution(dff),   use_container_width=True)

    st.caption(
        "Data source: Armenian accident registry (2020 update). "
        "Costs mapped to band mid-points."
    )

if __name__ == "__main__":
    main()
