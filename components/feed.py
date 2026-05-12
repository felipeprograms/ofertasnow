import os
import streamlit as st
from data.products import PRODUCTS, CATEGORIES, MARKETPLACES
from utils.mercadolivre import buscar_produtos_ml, buscar_por_termo_ml


def get_products_smart(categoria="todos", search_query=""):
    try:
        client_id = os.environ.get("ML_CLIENT_ID", "")
        if not client_id:
            try:
                client_id = st.secrets.get("ML_CLIENT_ID", "")
            except Exception:
                pass
        if client_id:
            if search_query:
                produtos = buscar_por_termo_ml(search_query, limite=12)
            else:
                cat = categoria if categoria != "todos" else "informatica"
                produtos = buscar_produtos_ml(cat, limite=12)
            if produtos:
                return produtos
    except Exception:
        pass
    return PRODUCTS


def render_product_card(product):
    mp = MARKETPLACES.get(product["marketplace"], {})
    mp_label = mp.get("label", product["marketplace"])
    economy = product["original_price"] - product["price"]
    stars = "★" * int(product["rating"]) + "☆" * (5 - int(product["rating"]))
    shipping = "Frete gratis" if product["free_shipping"] else "Calcular frete"

    mp_cores = {
        "mercadolivre": "background:#ffe600; color:#222;",
        "amazon":       "background:#ff9900; color:#111;",
        "shopee":       "background:#ee4d2d; color:#fff;",
        "kabum":        "background:#ff6600; color:#fff;",
        "pichau":       "background:#0066cc; color:#fff;",
    }
    mp_cor = mp_cores.get(product["marketplace"], "background:#444; color:#fff;")

    url = product.get("affiliate_url", "https://www.mercadolivre.com.br")
    if not url.startswith("http"):
        url = "https://www.mercadolivre.com.br"

    image_url = product.get("image", "")

    with st.container(border=True):
        # Imagem
        if image_url and image_url.startswith("https"):
            st.markdown(
                f'<div style="text-align:center; background:#111; border-radius:8px; '
                f'padding:8px; margin-bottom:8px; height:180px; display:flex; '
                f'align-items:center; justify-content:center; overflow:hidden;">'
                f'<img src="{image_url}" style="max-height:170px; max-width:100%; '
                f'object-fit:contain;" loading="lazy"/></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div style="height:180px; background:#111; border-radius:8px; '
                'display:flex; align-items:center; justify-content:center; '
                'color:#666; margin-bottom:8px; font-size:13px;">Sem imagem</div>',
                unsafe_allow_html=True
            )

        # Badges
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**-{product['discount']}% OFF**")
        with col2:
            st.markdown(
                f'<span style="{mp_cor} padding:3px 10px; border-radius:6px; '
                f'font-size:12px; font-weight:bold;">{mp_label}</span>',
                unsafe_allow_html=True
            )

        # Titulo
        title = product["title"]
        st.markdown(f"**{title[:70]}{'...' if len(title) > 70 else ''}**")

        # Preco
        st.markdown(f"### R$ {product['price']:,.2f}")
        st.caption(f"De: R$ {product['original_price']:,.2f}  |  Economia: R$ {economy:,.2f}")

        # Rating e frete
        c1, c2 = st.columns(2)
        with c1:
            st.caption(f"{stars} ({product['reviews']:,})")
        with c2:
            st.caption(shipping)

        # Botao — texto simples ASCII para evitar problema de encoding
        btn_text = f"Comprar no {mp_label}"
        st.markdown(
            f'<a href="{url}" target="_blank" rel="noopener noreferrer" '
            f'style="display:block; text-align:center; background:#ff6b00; '
            f'color:white !important; padding:11px 0; border-radius:8px; '
            f'font-weight:700; text-decoration:none; font-size:14px; '
            f'margin-top:8px; font-family:sans-serif;">{btn_text}</a>',
            unsafe_allow_html=True
        )


def filter_products(products):
    q = st.session_state.get("search_query", "").lower().strip()
    if q:
        products = [p for p in products if
                    q in p["title"].lower() or q in p["category"].lower()]

    cat = st.session_state.get("selected_category", "todos")
    if cat != "todos":
        products = [p for p in products if p["category"] == cat]

    mkt = st.session_state.get("marketplace_filter", "Todos os marketplaces")
    mkt_map = {
        "Mercado Livre": "mercadolivre",
        "Amazon": "amazon",
        "Shopee": "shopee",
        "KaBuM!": "kabum",
        "Pichau": "pichau",
    }
    if mkt in mkt_map:
        products = [p for p in products if p["marketplace"] == mkt_map[mkt]]

    order = st.session_state.get("order_filter", "Maior desconto")
    if order == "Maior desconto":
        products.sort(key=lambda p: p["discount"], reverse=True)
    elif order == "Menor preco":
        products.sort(key=lambda p: p["price"])
    elif order == "Maior preco":
        products.sort(key=lambda p: p["price"], reverse=True)
    elif order == "Melhor avaliado":
        products.sort(key=lambda p: p["rating"], reverse=True)

    return products


def render_feed():
    if "selected_category" not in st.session_state:
        st.session_state["selected_category"] = "todos"

    selected = st.session_state["selected_category"]
    search_query = st.session_state.get("search_query", "")

    cols_cat = st.columns(len(CATEGORIES))
    for i, cat in enumerate(CATEGORIES):
        with cols_cat[i]:
            btn_type = "primary" if selected == cat["id"] else "secondary"
            if st.button(cat["label"], key=f"catbtn_{cat['id']}",
                         use_container_width=True, type=btn_type):
                st.session_state["selected_category"] = cat["id"]
                st.rerun()

    st.divider()

    with st.spinner("Buscando ofertas..."):
        products = get_products_smart(selected, search_query)
        products = filter_products(products)

    if not products:
        st.info("Nenhum produto encontrado.")
        return

    st.markdown(f"**{len(products)} ofertas encontradas**")
    st.markdown("")

    for i in range(0, len(products), 3):
        row = products[i:i+3]
        cols = st.columns(3, gap="medium")
        for j, product in enumerate(row):
            with cols[j]:
                render_product_card(product)
        st.markdown("")
