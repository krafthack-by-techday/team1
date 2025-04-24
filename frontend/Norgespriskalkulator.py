import os

import streamlit as st
from dotenv import load_dotenv
from PIL import Image

try:
    from frontend.graphics.controls import controls
    from frontend.graphics.elements import colored_box
    from frontend.graphics.make_plot import make_plot
    from frontend.utils.utils import get_price_area
except ModuleNotFoundError:
    msg = "Could not import code, did you run pip install -e . ?"
    raise ModuleNotFoundError(msg)

load_dotenv("CONFIG.env")
logo = Image.open("assets/logo-green.png")
icon = Image.open("assets/ikon-gold.png")


st.set_page_config(page_title="Norgespriskalkulator", page_icon=icon, layout="wide")

with st.sidebar:
    st.image(logo, use_container_width=False, width=200)


st.write("""### Hei 👋 Her kan du sjekke om Norgesprisen lønner seg for deg 💰""")

norgespriscolor = os.environ["NORGESPRISCOLOR"]
spotpriscolor = os.environ["SPOTPRISCOLOR"]


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


@st.dialog("Informasjon om Norgespriskalkulator")
def vote(item):
    st.write(
        "Ikke lad din Tesla kl 16."
        "Hvis hele Norge lager Grandiossa 🍕 og lader Tesla 🏎️ til samme tid, så blir det strømutfall ⚡"
    )


if "vote" not in st.session_state:
    if st.sidebar.button("Informasjon om Norgespriskalkulator"):
        vote("Informasjon")
