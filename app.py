import streamlit as st
from utils.config import setup_page
from components.header import render_header
from components.feed import render_feed
from components.sidebar import render_sidebar

setup_page()

# Metatag de verificação Lomadee
st.markdown('<meta name="lomadee" content="2324685" />', unsafe_allow_html=True)

render_header()

col_main, col_side = st.columns([3, 1])

with col_main:
    render_feed()

with col_side:
    render_sidebar()
