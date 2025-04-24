import pandas as pd
import plotly.express as px
import streamlit as st


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
