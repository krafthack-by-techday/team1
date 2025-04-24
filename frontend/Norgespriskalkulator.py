import os
from typing import Literal

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel

st.set_page_config(page_title="Norgespriskalkulator", page_icon="🧮")

st.write("""### Hei 👋 Her kan du sjekke om Norgesprisen lønner seg for deg 💰
         """)

load_dotenv("CONFIG.env")
norgespriscolor = os.environ["NORGESPRISCOLOR"]
spotpriscolor = os.environ["SPOTPRISCOLOR"]


class Config(BaseModel):
    metering_point_id: str
    compare_based_on: Literal["History", "Forecast"]
    assumed_fixed_price: float
    # time_window: Literal["Year", "Month", "Day"]

    @property
    def input_is_set(self) -> bool:
        return self.compare_based_on != ""


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


def make_plot():
    # --- Hard-coded sample data in a DataFrame ---
    df = pd.DataFrame(
        {
            "foo": [1, 2, 3, 4, 5],
            "Series 1": [10, 20, 30, 40, 50],
            "Series 2": [15, 25, 35, 45, 55],
        }
    )

    # --- Create a Plotly Express line chart ---
    fig = px.line(
        df,
        x="foo",
        y=["Series 1", "Series 2"],
        markers=True,
    )

    # --- Render in Streamlit ---
    st.plotly_chart(fig, use_container_width=True)


def get_price_area(metering_point_id: str) -> str | None:
    if metering_point_id != "":  # The default return value of the text widget -
        # until the user has entered their ID, we do not know the price area
        return "NO42"
    return None


# Build the page


config = controls()


if (price_area := get_price_area(config.metering_point_id)) is not None:
    st.text(f"Din målepunkt er i prisområdet {price_area}")

make_plot()


cost_with_spotprice = 1
cost_with_norgesprice = 1


if config.input_is_set is True:
    # create two columns
    col1, col2 = st.columns(2)

    # helper to generate a colored box with black, bold text
    def colored_box(content: str, bg_color: str):
        return f"""
        <div style="
            background-color: {bg_color};
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
            color: #000;            /* black text */
            font-weight: bold;      /* bold text */
        ">
        {content}
        </div>
        """

    with col1:
        st.markdown(
            colored_box(
                f"Strømregning med Norgespris: {int(cost_with_norgesprice)} NOK",
                bg_color=norgespriscolor,
            ),
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            colored_box(
                f"Strømregning med spotpris: {int(cost_with_spotprice)} NOK",
                bg_color=spotpriscolor,
            ),
            unsafe_allow_html=True,
        )
