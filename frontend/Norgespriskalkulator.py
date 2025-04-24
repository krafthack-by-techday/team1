from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Norgespriskalkulator", page_icon="🧮")

st.write("""### Hei 👋 Her kan du sjekke om Norgesprisen lønner seg for deg 💰
         """)


start = datetime.now()


def make_plot(time_window, compare_based_on):
    # --- Hard-coded sample data in a DataFrame ---
    df = pd.DataFrame(
        {
            time_window: [1, 2, 3, 4, 5],
            "Series 1": [10, 20, 30, 40, 50],
            "Series 2": [15, 25, 35, 45, 55],
        }
    )

    # --- Create a Plotly Express line chart ---
    fig = px.line(
        df,
        x=time_window,
        y=["Series 1", "Series 2"],
        markers=True,
        labels={
            time_window: time_window,
            "value": compare_based_on,
            "variable": "Series",
        },
    )
    fig.update_layout(
        title=f"{compare_based_on} over {time_window}",
        xaxis_title=time_window,
        yaxis_title=compare_based_on,
    )

    # --- Render in Streamlit ---
    st.plotly_chart(fig, use_container_width=True)


# Målepunkt ID
metering_point_id = st.text_input("Målepunkt ID", placeholder="Enter Målepunkt ID")


# Dropdown menu for user selection
compare_against_dropdown_values = ["History", "Forecast (⚡💀)"]
compare_based_on = st.selectbox(
    "Compare against prices from:", compare_against_dropdown_values
)


# Dropdown menu for user selection
time_window_dropdown_values = ["Year", "Month", "Day"]
time_window = st.selectbox("Time window:", time_window_dropdown_values)

make_plot(time_window, compare_based_on)
