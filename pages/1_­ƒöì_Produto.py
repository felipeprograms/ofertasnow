import streamlit as st
from utils.config import setup_page
from data.products import PRODUCTS, MARKETPLACES
import random

setup_page()

st.title("🔍 Página do Produto")

# Pega produto pelo ID via query param ou mostra lista
params = st.query_params
product_id = params.get("id", None)

product = None
if product_id:
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)

if not product:
    st.info("Selecione um produto abaixo para ver os detalhes.")
    for p in PRODUCTS:
        if st.button(f"{p['title'][:60]}...", key=f"sel_{p['id']}"):
            st.query_params["id"] = p["id"]
            st.rerun()
    st.stop()

mp = MARKETPLACES.get(product["marketplace"], {})
mp_label = mp.get("label", product["marketplace"])
economy = product["original_price"] - product["price"]
stars = "★" * int(product["rating"]) + "☆" * (5 - int(product["rating"]))

# Layout principal
col_img, col_info = st.columns([1, 1], gap="large")

with col_img:
    st.image(product["image"], use_container_width=True)

    # Histórico de preço simulado
    st.markdown("#### 📈 Histórico de preço (últimos 30 dias)")
    import pandas as pd
    import numpy as np
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
    base = product["original_price"]
    prices = [round(base * (1 - random.uniform(0.05, 0.40)), 2) for _ in range(30)]
    prices[-1] = product["price"]  # Preço atual no último dia
    df = pd.DataFrame({"Data": dates, "Preço (R$)": prices})
    st.line_chart(df.set_index("Data"), color="#ff6b00")

    st.caption(f"💡 Menor preço registrado: **R$ {min(prices):,.2f}**  •  Maior: **R$ {max(prices):,.2f}**")

with col_info:
    st.markdown(f"### {product['title']}")
    st.caption(f"{stars} · {product['reviews']:,} avaliações · {mp_label}")

    st.markdown("---")

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.metric("Preço atual", f"R$ {product['price']:,.2f}",
                  delta=f"-R$ {economy:,.2f} ({product['discount']}% OFF)",
                  delta_color="inverse")
    with col_p2:
        st.metric("Preço original", f"R$ {product['original_price']:,.2f}")

    st.markdown("---")

    # Info rápida
    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1:
        st.markdown("✅ **Frete grátis**" if product["free_shipping"] else "🚚 **Calcular frete**")
    with col_i2:
        st.markdown(f"📦 **Em estoque**")
    with col_i3:
        st.markdown(f"🏪 **{mp_label}**")

    st.markdown("---")

    # Botão principal
    st.link_button(
        f"🛒 Comprar agora no {mp_label} →",
        url=product["affiliate_url"],
        use_container_width=True,
        type="primary",
    )

    # Alerta de preço
    with st.expander("🔔 Criar alerta de preço"):
        email = st.text_input("Seu e-mail", placeholder="voce@email.com")
        target = st.number_input("Avisar quando chegar em R$",
                                  value=round(product["price"] * 0.9, 2),
                                  min_value=1.0, step=10.0, format="%.2f")
        if st.button("Criar alerta", type="primary"):
            if email:
                st.success(f"✅ Alerta criado! Você receberá um e-mail quando o preço chegar em R$ {target:,.2f}")
            else:
                st.warning("Insira seu e-mail para criar o alerta.")

    # Compartilhar
    with st.expander("📤 Compartilhar produto"):
        link = f"https://seusite.streamlit.app/Produto?id={product['id']}"
        st.code(link)
        st.caption("Copie o link acima e compartilhe no Instagram, WhatsApp ou Telegram!")

# Produtos similares
st.markdown("---")
st.markdown("### 🔀 Produtos similares")
similares = [p for p in PRODUCTS if p["category"] == product["category"] and p["id"] != product["id"]][:3]
if similares:
    cols = st.columns(len(similares), gap="medium")
    for i, sim in enumerate(similares):
        with cols[i]:
            with st.container(border=True):
                st.image(sim["image"], use_container_width=True)
                st.markdown(f"**{sim['title'][:50]}...**")
                st.markdown(f"### R$ {sim['price']:,.2f}")
                st.caption(f"-{sim['discount']}% OFF")
                st.link_button("Ver oferta", url=sim["affiliate_url"], use_container_width=True)
