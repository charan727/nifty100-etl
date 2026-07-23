import sys
from pathlib import Path

import streamlit as st

# Add project src folder to Python path
SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

st.set_page_config(
    page_title="Nifty 100 Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Nifty 100 Analytics")
st.write("Select a page from the sidebar.")