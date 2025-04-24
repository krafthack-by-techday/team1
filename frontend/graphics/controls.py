import streamlit as st

from frontend.config import Config


def controls():  # -> Config:
    # Målepunkt ID
    st.sidebar.title("🔧 Konfigurasjon")

    metering_point_id = st.sidebar.text_input(
        "Målepunkt ID", placeholder="Din Målepunkt ID"
    )

    # Dropdown menu for user selection
    compare_against_dropdown_values = ["Historikk", "Prognose (⚡💀)"]
    compare_based_on = st.sidebar.selectbox(
        "Beregn basert på", compare_against_dropdown_values
    )

    assumed_fixed_price = st.sidebar.number_input(
        "Antatt Norgespris (Øre/kWh)",
        min_value=0,
        value=40,
        max_value=10_000,
    )

    # # Dropdown menu for user selection
    # time_window_dropdown_values = ["Year", "Month", "Day"]
    # time_window = st.sidebar.selectbox("Time window:", time_window_dropdown_values)

    return Config(
        metering_point_id=metering_point_id,
        compare_based_on="Forecast" if "Prognose" in compare_based_on else "History",
        # time_window=time_window,
        assumed_fixed_price=assumed_fixed_price,
    )
