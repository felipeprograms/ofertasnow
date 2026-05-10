import streamlit as st
from data.products import PRODUCTS, CATEGORIES, MARKETPLACES


def get_products_smart(categoria="todos", search_query=""):
    """Usa API do ML se configurado, senão usa produtos mock."""
    try:
        import streamlit as st
        client_id = st.secrets.get("ML_CLIENT_ID", "")
        if client_id:
            from utils.mercadolivre import buscar_produtos_ml, buscar_por_termo_ml
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
    shipping = "✅ Frete grátis" if product["free_shipping"] else "🚚 Calcular frete"

    mp_emoji = {
        "mercadolivre": "🟡",
        "amazon":       "🟠",
        "shopee":       "🔴",
        "kabum":        "🟤",
        "pichau":       "🔵",
    }
    emoji = mp_emoji.get(product["marketplace"], "🛒")

    with st.container(border=True):
        try:
            st.image(product["image"], use_container_width=True)
        except Exception:
            st.markdown("🖼️")

        col_badge1, col_badge2 = st.columns(2)
        with col_badge1:
            st.markdown(f"🔥 **-{product['discount']}% OFF**")
        with col_badge2:
            st.markdown(f"{emoji} {mp_label}")

        st.markdown(f"**{product['title'][:70]}{'...' if len(product['title']) > 70 else ''}**")
        st.caption(product["tag"])
        st.markdown(f"### R$ {product['price']:,.2f}")
        st.caption(f"~~R$ {product['original_price']:,.2f}~~  •  💚 Economia R$ {economy:,.2f}")

        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.caption(f"{stars} ({product['reviews']:,})")
        with col_r2:
            st.caption(shipping)

        st.link_button(
            f"🛒 Comprar no {mp_label}",
            url=product["affiliate_url"],
            use_container_width=True,
        )


def filter_products(products):
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
    elif order == "Menor preço":
        products.sort(key=lambda p: p["price"])
    elif order == "Maior preço":
        products.sort(key=lambda p: p["price"], reverse=True)
    elif order == "Melhor avaliado":
        products.sort(key=lambda p: p["rating"], reverse=True)

    return products


def render_feed():
    if "selected_category" not in st.session_state:
        st.session_state["selected_category"] = "todos"

    selected = st.session_state["selected_category"]
    search_query = st.session_state.get("search_query", "")

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

    # Busca produtos (API real ou mock)
    with st.spinner("🔍 Buscando ofertas..."):
        products = get_products_smart(selected, search_query)
        products = filter_products(products)

    if not products:
        st.info("🔍 Nenhum produto encontrado. Tente outro filtro.")
        return

    # Indica fonte dos dados
    try:
        using_api = bool(st.secrets.get("ML_CLIENT_ID", ""))
    except Exception:
        using_api = False

    fonte = "🟢 Produtos reais do Mercado Livre" if using_api else "🟡 Produtos de demonstração"
    st.markdown(f"🔥 **{len(products)} ofertas encontradas** · *{fonte}*")
    st.markdown("")

    # Grid 3 colunas
    for i in range(0, len(products), 3):
        row = products[i:i+3]
        cols = st.columns(3, gap="medium")
        for j, product in enumerate(row):
            with cols[j]:
                render_product_card(product)
        st.markdown("")
