import os

import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Dict, List

try:
    from frontend.graphics.controls import controls
    from frontend.graphics.elements import colored_box
    from frontend.graphics.make_plot import make_plot
    from frontend.utils.utils import get_price_area
    from backend.app import Backend
except ModuleNotFoundError:
    msg = "Could not import code, did you run pip install -e . ?"
    raise ModuleNotFoundError(msg)

load_dotenv("CONFIG.env")
logo = Image.open("assets/logo-green-nobackground.png")
icon = Image.open("assets/ikon-gold-nobackground.png")


st.set_page_config(page_title="Norgespriskalkulator", page_icon=icon, layout="wide")
app = Backend()

@st.cache_data
def henter_og_beregner_data(user: str, fastpris: int, price_area: str) -> Dict[str, pd.DataFrame]:
    """
    Aggregates specified value columns in a time-indexed DataFrame.

    :param data: DataFrame with a DatetimeIndex.
    :param value_columns: List of column names to aggregate.
    :return: Dictionary with aggregated DataFrames for each level.

    NB. The function name is shown in the app so i've given it a norwegian name
    """
    spot_cost = app.get_spotpris_cost_per_hour(
        start=datetime(2022, 6, 1, hour=0, tzinfo=ZoneInfo("UTC")),
        end=datetime(2025, 3, 1, hour=23, tzinfo=ZoneInfo("UTC")),
        meter_name=user,
        price_area=price_area
    )

    norgespris_cost = app.get_fastpris_cost_per_hour(
            fastpris=fastpris,
            start=datetime(2022, 6, 1, hour=0, tzinfo=ZoneInfo("UTC")),
            end=datetime(2025, 3, 1, hour=23, tzinfo=ZoneInfo("UTC")),
            meter_name=user,
        )

    data = pd.concat([spot_cost, norgespris_cost], axis=1)
    data.columns = ["Spotpris", "Norgespris"]
    data["Spotpris"] = data["Spotpris"].astype(float)
    data["Norgespris"] = data["Norgespris"].astype(float)

    # removing index because of interactive date-picker, can be readded later
    data.index = data.index.tz_convert(None)

    value_columns = ["Spotpris", "Norgespris"]

    if not isinstance(data.index, pd.DatetimeIndex):
        raise ValueError("Data index must be a DatetimeIndex.")

    return {
        "original": data,
        "hour": data[value_columns].resample("H").sum(),
        "day": data[value_columns].resample("D").sum(),
        "month": data[value_columns].resample("M").sum(),
        "year": data[value_columns].resample("Y").sum()
    }

with st.sidebar:
    st.image(logo, use_container_width=False, width=200)


st.write("### Hei 👋")
st.write("### Mister du også helt Gnisten av hva Norgespris er?")
st.write("Her kan du sjekke om Norgesprisen lønner seg for deg 💰""")

norgespriscolor = os.environ["NORGESPRISCOLOR"]
spotpriscolor = os.environ["SPOTPRISCOLOR"]

# Build the page

config = controls()

if (price_area := get_price_area(config.metering_point_id)) is not None:
    st.text(f"Din målepunkt er i prisområdet {price_area}")

user_mapping = {
    "Jan Erik": {
        "bio": "Jan Erik, 39 år, bor i enebolig i NO2",
        "timeseries": "Trydal_1",
        "price_area": "NO2"
    },
    "Christine": {
        "bio": "Christine, 29 år, bor i leilighet i NO1",
        "timeseries": "christine",
        "price_area": "NO1"
    },
}

st.write(f"Beregner for {user_mapping[config.select_user]["bio"]}")

hour_tab, day_tab, month_tab, year_tab = st.tabs(
    ["Time", "Dag", "Måned", "År"]
)

data = henter_og_beregner_data(
    user_mapping[config.select_user]["timeseries"],
    fastpris=config.assumed_fixed_price,
    price_area=user_mapping[config.select_user]["price_area"]
)

with hour_tab:
    hour_plot = make_plot(data=data["hour"].loc[config.time_window[0]: config.time_window[1]])
    with st.expander("Se som tabell"):
        st.dataframe(data["hour"].loc[config.time_window[0]: config.time_window[1]])
with day_tab:
    day_plot = make_plot(data=data["day"].loc[config.time_window[0]: config.time_window[1]])
    with st.expander("Se som tabell"):
        st.dataframe(data["day"].loc[config.time_window[0]: config.time_window[1]])
with month_tab:
    month_plot = make_plot(data=data["month"].loc[config.time_window[0]: config.time_window[1]])
    with st.expander("Se som tabell"):
        st.dataframe(data["month"].loc[config.time_window[0]: config.time_window[1]])
with year_tab:
    year_plot = make_plot(data=data["year"].loc[config.time_window[0]: config.time_window[1]])
    with st.expander("Se som tabell"):
        st.dataframe(data["year"].loc[config.time_window[0]: config.time_window[1]])


cost_with_spotprice = data["original"].loc[config.time_window[0]: config.time_window[1]]["Spotpris"].sum()
cost_with_norgesprice = data["original"].loc[config.time_window[0]: config.time_window[1]]["Norgespris"].sum()


if config.input_is_set is True:
    # create two columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            colored_box(
                f"Strømregning med Norgespris: {cost_with_norgesprice:,.0f} NOK".replace(",", " "),
                bg_color="#C2EDA9",
            ),
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            colored_box(
                f"Strømregning med SPOT: {cost_with_spotprice:,.0f} NOK".replace(",", " "),
                bg_color="#FEEDC9",
            ),
            unsafe_allow_html=True,
        )


@st.dialog(title= "Informasjon om Norgespriskalkulator", width="large")
def vote(item):
    st.write(
        """
        ## Gnisten – Din guide til Norgespris
        Gnisten er en tjeneste som hjelper deg med å forstå hvordan norgespris påvirker din økonomi. Med Gnisten kan du enkelt sammenligne strømforbruksmønstre og tidsbestemt forbruk og se om Norgespris er det beste alternativet for deg.
        
        ## Hva er Norgespris?
        Norgespris er en statlig støtteordning som tilbyr en fast strømpris på 40 øre per kilowattime (ekskl. mva) for husholdninger og fritidsboliger. Dette gir forutsigbare og stabile strømpriser, uavhengig av markedets svingninger.
        
        ## Hvordan fungerer Gnisten?
        Med Gnisten kan du utforske forskjellige scenarier og se hvordan Norgespris sammenligner seg med andre strømavtaler. Tjenesten gir deg muligheten til å:
        - Sammenligne strømpriser: Se hvordan Norgespris står seg mot dagens spotpriser og stromstøtte.
        - Beregne kostnader: Få en oversikt over dine potensielle strømkostnader basert på ditt forbruksmønster i din bolig eller hytte. Data hentes fra ElHu i din bolig eller hytte. Data hentes fra ElHub.
        - Simulere ulike forbruksscenarier: Utforsk hvordan endringer i ditt strømforbruk påvirker kostnadene med Norgespris og andre avtaler.
        
        ## Hvorfor bruke Gnisten?
        Gnisten gir deg verktøyene du trenger for å ta informerte beslutninger om norgesprisen. Ved å bruke tjenesten kan du:
        - Spare penger: Teste scenarier for ditt behov.
        - Få trygghet: Forstå hvordan ulike avtaler påvirker din økonomi.
        - Støtte din beslutting: Norgespris ja eller nei.

        ## Hva koster det å burke gnisten?
        Gnisten er gratis å bruke for alle husholdninger og fritidsboliger i Norge. Det er ingen skjulte kostnader eller avgifter.
        """
    )


if "vote" not in st.session_state:
    if st.sidebar.button("Informasjon om Norgespriskalkulator"):
        vote("Informasjon")
