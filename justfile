init:
    #!/bin/bash
    rm -rf .venv
    python3.12 -m venv .venv --prompt gnisten
    .venv/bin/pip3 install --upgrade pip
    .venv/bin/pip3 install -r requirements.txt

start_gui:
    .venv/bin/streamlit run norgespriskalkulator.py