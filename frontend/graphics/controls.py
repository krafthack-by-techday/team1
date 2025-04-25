import datetime

import streamlit as st

from frontend.config import Config


def controls():  # -> Config:
    # metering_point_id = st.sidebar.text_input(
    #     "Målepunkt ID", placeholder="Din Målepunkt ID", disabled=True
    # )

    # Dropdown for a predefined user
    select_user = st.sidebar.selectbox(
        "Hvem er du?",
        [
            "Jan Erik",
            "Christine",
        ],
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

    # Drowpdown for date interval
    today = datetime.date.today()
    # min_value = today - datetime.timedelta(days=30 * 13 * 1)

    start_date = datetime.date(2024, 1, 1)
    min_value = start_date
    end_date = datetime.date(2025, 1, 1)
    time_window = st.sidebar.date_input(
        "Velg dato",
        value=(start_date, end_date),
        min_value=min_value,
        max_value=today,
        format="YYYY-MM-DD",
    )

    return Config(
        # metering_point_id=metering_point_id,
        select_user=select_user,
        compare_based_on="Forecast" if "Prognose" in compare_based_on else "History",
        time_window=time_window,
        assumed_fixed_price=assumed_fixed_price,
    )
