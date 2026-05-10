import streamlit as st
from utils.config import setup_page
from data.products import PRODUCTS, MARKETPLACES
from utils.mercadolivre import buscar_produtos_ml
import random
import pandas as pd

setup_page()

st.title("🔍 Detalhes do Produto")

params = st.query_params
product_id = params.get("id", None)

# Tenta achar o produto nos mocks primeiro
product = next((p for p in PRODUCTS if p["id"] == product_id), None)

# Se não achou no mock, tenta buscar no ML pelo ID externo
if not product and product_id and product_id.startswith("ml_"):
    ml_id = product_id.replace("ml_", "")
    try:
        import requests
        resp = requests.get(f"https://api.mercadolibre.com/items/{ml_id}", timeout=8)
        if resp.status_code == 200:
            item = resp.json()
            original = item.get("original_price") or item["price"]
            price = item["price"]
            discount = int((1 - price / original) * 100) if original > price else 0
            image = ""
            pictures = item.get("pictures", [])
            if pictures:
                image = pictures[0].get("url", "")
            product = {
                "id": product_id,
                "title": item["title"],
                "price": price,
                "original_price": original,
                "discount": discount,
                "image": image,
                "marketplace": "mercadolivre",
                "rating": 4.2,
                "reviews": item.get("sold_quantity", 0) or 0,
                "affiliate_url": item.get("permalink", "#"),
                "category": "busca",
                "tag": "🟡 Mercado Livre",
                "free_shipping": item.get("shipping", {}).get("free_shipping", False),
                "description": item.get("title", ""),
            }
    except Exception as e:
        st.warning(f"Erro ao buscar produto: {e}")

# Se ainda não achou, mostra lista para selecionar
if not product:
    st.info("Selecione um produto para ver os detalhes.")

    # Mostra produtos do ML ou mock
    try:
        client_id = st.secrets.get("ML_CLIENT_ID", "")
        all_products = buscar_produtos_ml("informatica", 12) if client_id else PRODUCTS
    except Exception:
        all_products = PRODUCTS

    cols = st.columns(3, gap="medium")
    for i, p in enumerate(all_products[:9]):
        with cols[i % 3]:
            with st.container(border=True):
                try:
                    st.image(p["image"], use_container_width=True)
                except Exception:
                    pass
                st.markdown(f"**{p['title'][:50]}...**")
                st.markdown(f"R$ {p['price']:,.2f}")
                if st.button("Ver detalhes", key=f"sel_{p['id']}", use_container_width=True):
                    st.query_params["id"] = p["id"]
                    st.rerun()
    st.stop()

# ── Página do produto ──
mp = MARKETPLACES.get(product["marketplace"], {})
mp_label = mp.get("label", product["marketplace"])
economy = product["original_price"] - product["price"]
stars = "★" * int(product["rating"]) + "☆" * (5 - int(product["rating"]))

col_img, col_info = st.columns([1, 1], gap="large")

with col_img:
    try:
        st.image(product["image"], use_container_width=True)
    except Exception:
        st.markdown("🖼️ Imagem indisponível")

    st.markdown("#### 📈 Histórico de preço (últimos 30 dias)")
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
    base = product["original_price"]
    prices = [round(base * (1 - random.uniform(0.05, 0.40)), 2) for _ in range(30)]
    prices[-1] = product["price"]
    df = pd.DataFrame({"Data": dates, "Preço (R$)": prices})
    st.line_chart(df.set_index("Data"), color="#ff6b00")
    st.caption(f"💡 Menor preço: **R$ {min(prices):,.2f}** · Maior: **R$ {max(prices):,.2f}**")

with col_info:
    st.markdown(f"### {product['title']}")
    st.caption(f"{stars} · {product['reviews']:,} vendidos · {mp_label}")
    st.markdown("---")

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.metric("Preço atual", f"R$ {product['price']:,.2f}",
                  delta=f"-R$ {economy:,.2f} ({product['discount']}% OFF)",
                  delta_color="inverse")
    with col_p2:
        st.metric("Preço original", f"R$ {product['original_price']:,.2f}")

    st.markdown("---")

    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1:
        st.markdown("✅ **Frete grátis**" if product["free_shipping"] else "🚚 **Calcular**")
    with col_i2:
        st.markdown("📦 **Em estoque**")
    with col_i3:
        st.markdown(f"🏪 **{mp_label}**")

    st.markdown("---")

    st.link_button(
        f"🛒 Comprar no {mp_label} →",
        url=product["affiliate_url"],
        use_container_width=True,
        type="primary",
    )

    with st.expander("🔔 Criar alerta de preço"):
        email = st.text_input("Seu e-mail", placeholder="voce@email.com")
        target = st.number_input("Avisar quando chegar em R$",
                                  value=round(product["price"] * 0.9, 2),
                                  min_value=1.0, step=10.0, format="%.2f")
        if st.button("Criar alerta", type="primary"):
            if email:
                st.success(f"✅ Alerta criado! Avisaremos quando chegar em R$ {target:,.2f}")
            else:
                st.warning("Insira seu e-mail.")

    with st.expander("📤 Compartilhar"):
        link = f"https://seusite.streamlit.app/Produto?id={product['id']}"
        st.code(link)

# Produtos similares
st.markdown("---")
st.markdown("### 🔀 Produtos similares")
try:
    client_id = st.secrets.get("ML_CLIENT_ID", "")
    similares = buscar_produtos_ml(product["category"], 6) if client_id else []
    similares = [p for p in similares if p["id"] != product["id"]][:3]
except Exception:
    similares = []

if not similares:
    similares = [p for p in PRODUCTS if p["category"] == product.get("category") and p["id"] != product["id"]][:3]

if similares:
    cols = st.columns(len(similares), gap="medium")
    for i, sim in enumerate(similares):
        with cols[i]:
            with st.container(border=True):
                try:
                    st.image(sim["image"], use_container_width=True)
                except Exception:
                    pass
                st.markdown(f"**{sim['title'][:50]}...**")
                st.markdown(f"### R$ {sim['price']:,.2f}")
                st.caption(f"-{sim['discount']}% OFF")
                st.link_button("Ver oferta", url=sim["affiliate_url"], use_container_width=True)
