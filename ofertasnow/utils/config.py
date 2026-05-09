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

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fundo escuro estilo tech */
    .stApp {
        background-color: #0f0f13;
        color: #f0f0f0;
    }

    /* Remove padding padrão do Streamlit */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 1400px !important;
    }

    /* Card de produto */
    .product-card {
        background: #1a1a24;
        border: 1px solid #2a2a3a;
        border-radius: 16px;
        padding: 16px;
        transition: all 0.2s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }

    .product-card:hover {
        border-color: #ff6b00;
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(255, 107, 0, 0.15);
    }

    /* Badge de desconto */
    .discount-badge {
        background: linear-gradient(135deg, #ff3c00, #ff6b00);
        color: white;
        font-size: 12px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 8px;
    }

    /* Badge de marketplace */
    .marketplace-badge {
        font-size: 11px;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-block;
    }

    .badge-ml   { background: #ffe600; color: #333; }
    .badge-amz  { background: #ff9900; color: #111; }
    .badge-shopee { background: #ee4d2d; color: #fff; }
    .badge-kabum { background: #f60; color: #fff; }
    .badge-pichau { background: #0066cc; color: #fff; }

    /* Preço */
    .price-main {
        font-size: 24px;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.1;
    }

    .price-original {
        font-size: 13px;
        color: #666;
        text-decoration: line-through;
    }

    .price-economy {
        font-size: 12px;
        color: #00c853;
        font-weight: 600;
    }

    /* Botão de compra */
    .buy-btn {
        display: block;
        width: 100%;
        background: linear-gradient(135deg, #ff6b00, #ff3c00);
        color: white !important;
        text-align: center;
        padding: 12px 0;
        border-radius: 10px;
        font-weight: 700;
        font-size: 14px;
        text-decoration: none !important;
        margin-top: 12px;
        transition: opacity 0.2s;
    }

    .buy-btn:hover {
        opacity: 0.9;
        text-decoration: none !important;
    }

    /* Título produto */
    .product-title {
        font-size: 14px;
        font-weight: 500;
        color: #e0e0e0;
        margin: 10px 0 8px;
        line-height: 1.4;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    /* Rating */
    .rating {
        font-size: 12px;
        color: #ffc107;
    }

    /* Header gradiente */
    .hero-header {
        background: linear-gradient(135deg, #1a0a00 0%, #0f0f13 50%, #000a1a 100%);
        border: 1px solid #2a2a3a;
        border-radius: 20px;
        padding: 32px 40px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }

    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -20%;
        width: 60%;
        height: 200%;
        background: radial-gradient(ellipse, rgba(255,107,0,0.08) 0%, transparent 70%);
        pointer-events: none;
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

    .hero-subtitle {
        color: #888;
        font-size: 15px;
        margin-top: 6px;
    }

    /* Filtros / tabs */
    .filter-chip {
        background: #1a1a24;
        border: 1px solid #2a2a3a;
        color: #bbb;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 13px;
        cursor: pointer;
        display: inline-block;
        margin: 4px;
    }

    .filter-chip.active {
        background: #ff6b00;
        border-color: #ff6b00;
        color: white;
    }

    /* Seção */
    .section-title {
        font-size: 18px;
        font-weight: 700;
        color: #fff;
        margin: 24px 0 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Sidebar widget */
    .sidebar-widget {
        background: #1a1a24;
        border: 1px solid #2a2a3a;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 16px;
    }

    .sidebar-widget h4 {
        color: #ff6b00;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
    }

    /* Esconde elementos padrão do Streamlit */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }

    /* Links do Streamlit */
    a { color: #ff6b00 !important; }

    /* Inputs */
    .stTextInput input {
        background: #1a1a24 !important;
        border: 1px solid #2a2a3a !important;
        color: #fff !important;
        border-radius: 10px !important;
    }

    .stSelectbox select {
        background: #1a1a24 !important;
        color: #fff !important;
    }

    div[data-testid="stHorizontalBlock"] { gap: 12px; }

    </style>
    """, unsafe_allow_html=True)
