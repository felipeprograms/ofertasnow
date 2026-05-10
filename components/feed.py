import streamlit as st
from data.products import PRODUCTS, CATEGORIES, MARKETPLACES


def render_product_card(product):
    mp = MARKETPLACES.get(product["marketplace"], {})
    mp_label = mp.get("label", product["marketplace"])
    economy = product["original_price"] - product["price"]
    stars = "★" * int(product["rating"]) + "☆" * (5 - int(product["rating"]))

    # Emoji por marketplace
    mp_emoji = {
        "mercadolivre": "🟡",
        "amazon":       "🟠",
        "shopee":       "🔴",
        "kabum":        "🟤",
        "pichau":       "🔵",
    }
    emoji = mp_emoji.get(product["marketplace"], "🛒")

    with st.container(border=True):
        # Imagem
        try:
            st.image(product["image"], use_container_width=True)
        except Exception:
            st.markdown("🖼️ *Imagem indisponível*")

        # Badges
        col_badge1, col_badge2 = st.columns(2)
        with col_badge1:
            st.markdown(f"🔥 **-{product['discount']}% OFF**")
        with col_badge2:
            st.markdown(f"{emoji} {mp_label}")

        # Título
        st.markdown(f"**{product['title'][:70]}{'...' if len(product['title']) > 70 else ''}**")

        # Tag
        st.caption(product["tag"])

        # Preço
        st.markdown(f"### R$ {product['price']:,.2f}")
        st.caption(f"~~R$ {product['original_price']:,.2f}~~  •  💚 Economia R$ {economy:,.2f}")

        # Rating e frete
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.caption(f"{stars} ({product['reviews']:,})")
        with col_r2:
            st.caption("✅ Frete grátis" if product["free_shipping"] else "🚚 Calcular")

        # Botão de compra
        st.link_button(
            f"🛒 Comprar no {mp_label}",
            url=product["affiliate_url"],
            use_container_width=True,
        )


def filter_products():
    products = PRODUCTS.copy()

    q = st.session_state.get("search_query", "").lower().strip()
    if q:
        products = [p for p in products if q in p["title"].lower() or q in p["category"].lower()]

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

    # Botões de categoria
    cols_cat = st.columns(len(CATEGORIES))
    for i, cat in enumerate(CATEGORIES):
        with cols_cat[i]:
            btn_type = "primary" if selected == cat["id"] else "secondary"
            if st.button(cat["label"], key=f"catbtn_{cat['id']}",
                         use_container_width=True, type=btn_type):
                st.session_state["selected_category"] = cat["id"]
                st.rerun()

    st.divider()

    products = filter_products()

    if not products:
        st.info("🔍 Nenhum produto encontrado. Tente outro filtro.")
        return

    st.markdown(f"🔥 **{len(products)} ofertas encontradas** · *Atualizado agora*")
    st.markdown("")

    # Grid 3 colunas
    for i in range(0, len(products), 3):
        row = products[i:i+3]
        cols = st.columns(3, gap="medium")
        for j, product in enumerate(row):
            with cols[j]:
                render_product_card(product)
        st.markdown("")
