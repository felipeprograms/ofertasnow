import streamlit as st

def render_header():
    st.markdown("""
    <div class="hero-header">
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px;">
            <div>
                <h1 class="hero-title">⚡ OfertasNow</h1>
                <p class="hero-subtitle">Melhores preços de Mercado Livre, Amazon, Shopee, KaBuM! e Pichau</p>
            </div>
            <div style="display:flex; gap:12px; align-items:center;">
                <div style="background:#1a1a24; border:1px solid #ff6b00; border-radius:8px; padding:6px 14px; color:#ff6b00; font-size:13px; font-weight:600;">
                    🔔 Alertas de Preço
                </div>
                <div style="background:linear-gradient(135deg,#ff6b00,#ff3c00); border-radius:8px; padding:6px 14px; color:#fff; font-size:13px; font-weight:600;">
                    📲 130k no Instagram
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Barra de busca
    col1, col2, col3 = st.columns([4, 1, 1])
    with col1:
        search = st.text_input("", placeholder="🔍  Buscar produto, marca ou categoria...",
                               label_visibility="collapsed", key="search_bar")
    with col2:
        marketplace_filter = st.selectbox("", ["Todos os marketplaces", "Mercado Livre",
                                               "Amazon", "Shopee", "KaBuM!", "Pichau"],
                                          label_visibility="collapsed", key="mkt_filter")
    with col3:
        order_filter = st.selectbox("", ["Maior desconto", "Menor preço",
                                         "Maior preço", "Melhor avaliado"],
                                    label_visibility="collapsed", key="order_filter")

    st.session_state["search_query"] = search
    st.session_state["marketplace_filter"] = marketplace_filter
    st.session_state["order_filter"] = order_filter
