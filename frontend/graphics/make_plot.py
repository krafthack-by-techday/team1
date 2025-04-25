from functools import lru_cache

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.NorgesPlotter import NorgesPlotter


# @st.cache_resource
def make_plot(
    data: pd.DataFrame = None,
) -> None:
    plotter = NorgesPlotter(data)
    plotter.add_line(
        x_col="index",
        y_col="Norgespris",
        title="Sammenligning av kostnader",
        name="Norgespris",
        x_title="Tid",
        y_title="Kostnad [NOK]",
        line_color="#469d13",
    )
    plotter.add_line(
        x_col="index",
        y_col="Spotpris",
        title="Sammenligning av kostnader",
        name="Spotpris m/ strømstøtte",
        x_title="Tid",
        y_title="Kostnad [NOK]",
        line_color="#d29d2f",
    )
    plotter.shade_between_lines()
    st.plotly_chart(
        plotter.show_plot(streamlit_mode=True), config=({"displayModeBar": False})
    )
