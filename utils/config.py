import streamlit as st

def setup_page():
    st.set_page_config(
        page_title="OfertasNow — Melhores Ofertas do Brasil",
        page_icon="🔥",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Fundo dark */
    .stApp { background-color: #0f0f13; color: #f0f0f0; }

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 1400px !important;
    }

    /* Hero header */
    .hero-header {
        background: linear-gradient(135deg, #1a0a00 0%, #0f0f13 50%, #000a1a 100%);
        border: 1px solid #2a2a3a;
        border-radius: 20px;
        padding: 32px 40px;
        margin-bottom: 24px;
    }
    .hero-title {
        font-size: 36px;
        font-weight: 800;
        background: linear-gradient(90deg, #ff6b00, #ffaa00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    .hero-subtitle { color: #888; font-size: 15px; margin-top: 6px; }

    /* Botões de categoria — override Streamlit */
    .stButton > button {
        background: #1a1a24 !important;
        color: #bbb !important;
        border: 1px solid #2a2a3a !important;
        border-radius: 20px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        padding: 6px 4px !important;
        transition: all 0.15s !important;
    }
    .stButton > button:hover {
        background: #252535 !important;
        color: #fff !important;
        border-color: #ff6b00 !important;
    }
    /* Botão primário (categoria ativa) */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid*="primary"] {
        background: #ff6b00 !important;
        color: #fff !important;
        border-color: #ff6b00 !important;
    }

    /* Inputs de busca e selects */
    .stTextInput input {
        background: #1a1a24 !important;
        border: 1px solid #2a2a3a !important;
        color: #fff !important;
        border-radius: 10px !important;
    }
    .stTextInput input:focus {
        border-color: #ff6b00 !important;
        box-shadow: 0 0 0 1px #ff6b00 !important;
    }
    .stSelectbox > div > div {
        background: #1a1a24 !important;
        border: 1px solid #2a2a3a !important;
        color: #fff !important;
        border-radius: 10px !important;
    }

    /* Form inputs na sidebar */
    .stNumberInput input, .stTextInput input {
        background: #1a1a24 !important;
        color: #fff !important;
    }
    .stForm { background: transparent !important; border: none !important; }

    /* Botão submit do formulário */
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #ff6b00, #ff3c00) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
    }

    /* Esconde elementos padrão */
    #MainMenu, footer { visibility: hidden; }
    .stDeployButton { display: none; }

    /* Links globais */
    a { color: #ff6b00 !important; }

    /* Scrollbar dark */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0f0f13; }
    ::-webkit-scrollbar-thumb { background: #2a2a3a; border-radius: 3px; }
    </style>
    """, unsafe_allow_html=True)
