import streamlit as st
import datetime

from frontend.config import Config


def controls():  # -> Config:
    # Målepunkt ID
    st.sidebar.title("🔧 Konfigurasjon")

    metering_point_id = st.sidebar.text_input(
        "Målepunkt ID", placeholder="Din Målepunkt ID", disabled=True
    )

    # Dropdown for a predefined user
    select_user = st.sidebar.selectbox(
        "Hvem er du?",
        [
            "Jan Erik",
            "Christine",
        ]
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
    last_3_years = today - datetime.timedelta(days=30*12*3)
    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2023, 12, 31)
    time_window = st.sidebar.date_input(
        "Velg dato",
        value=(start_date, end_date),
        min_value=last_3_years,
        max_value=today,
        format="YYYY-MM-DD"
    )

    return Config(
        metering_point_id=metering_point_id,
        select_user=select_user,
        compare_based_on="Forecast" if "Prognose" in compare_based_on else "History",
        time_window=time_window,
        assumed_fixed_price=assumed_fixed_price,
    )
