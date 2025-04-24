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
        """
        ## Gnisten – Din guide til Norgespris
        Gnisten er en tjeneste som hjelper deg med å forstå hvordan norgespris påvirker din økonomi. Med Gnisten kan du enkelt sammenligne strømforbruksmønstre og tidsbestemt forbruk og se om Norgespris er det beste alternativet for deg.
        
        ## Hva er Norgespris?
        Norgespris er en statlig støtteordning som tilbyr en fast strømpris på 40 øre per kilowattime (ekskl. mva) for husholdninger og fritidsboliger. Dette gir forutsigbare og stabile strømpriser, uavhengig av markedets svingninger.
        
        ## Hvordan fungerer Gnisten?
        Med Gnisten kan du utforske forskjellige scenarier og se hvordan Norgespris sammenligner seg med andre strømavtaler. Tjenesten gir deg muligheten til å:
        - Sammenligne strømpriser: Se hvordan Norgespris står seg mot dagens spotpriser og stromstøtte.
        - Beregne kostnader: Få en oversikt over dine potensielle strømkostnader basert på ditt forbruksmønster.
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
