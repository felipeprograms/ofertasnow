import streamlit as st
from data.products import PRODUCTS, CATEGORIES, MARKETPLACES


def get_products_smart(categoria="todos", search_query=""):
    try:
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
    shipping = "Frete gratis" if product["free_shipping"] else "Calcular frete"

    mp_emoji = {
        "mercadolivre": "ML",
        "amazon":       "AMZ",
        "shopee":       "SHP",
        "kabum":        "KBM",
        "pichau":       "PCH",
    }
    sigla = mp_emoji.get(product["marketplace"], "🛒")

    url = product.get("affiliate_url", "#")
    if not url.startswith("http"):
        url = "https://www.mercadolivre.com.br"

    with st.container(border=True):
        # Imagem via requests para evitar bloqueio
        image_url = product.get("image", "")
        if image_url and image_url.startswith("http"):
            try:
                import requests
                from PIL import Image
                from io import BytesIO
                resp = requests.get(image_url, timeout=5,
                                    headers={"User-Agent": "Mozilla/5.0"})
                if resp.status_code == 200:
                    img = Image.open(BytesIO(resp.content))
                    st.image(img, use_container_width=True)
                else:
                    st.markdown("_(sem imagem)_")
            except Exception:
                st.markdown("_(sem imagem)_")
        else:
            st.markdown("_(sem imagem)_")

        col_badge1, col_badge2 = st.columns(2)
        with col_badge1:
            st.markdown(f"**-{product['discount']}% OFF**")
        with col_badge2:
            st.markdown(f"**{sigla}** {mp_label}")

        title = product['title']
        st.markdown(f"**{title[:70]}{'...' if len(title) > 70 else ''}**")
        st.caption(product.get("tag", ""))
        st.markdown(f"### R$ {product['price']:,.2f}")

        preco_orig = f"R$ {product['original_price']:,.2f}"
        economia = f"R$ {economy:,.2f}"
        st.caption(f"De: {preco_orig} | Economia: {economia}")

        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.caption(f"{stars} ({product['reviews']:,})")
        with col_r2:
            st.caption(shipping)

        # Botao HTML simples sem emoji para evitar problema de encoding
        st.markdown(
            f'<a href="{url}" target="_blank" rel="noopener noreferrer" '
            f'style="display:block; text-align:center; background:#ff6b00; '
            f'color:white !important; padding:10px; border-radius:8px; '
            f'font-weight:bold; text-decoration:none; font-size:14px; '
            f'margin-top:8px;">Comprar no {mp_label}</a>',
            unsafe_allow_html=True
        )


def filter_products(products):
    q = st.session_state.get("search_query", "").lower().strip()
    if q:
        products = [p for p in products if q in p["title"].lower()
                    or q in p["category"].lower()]

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
        st.info("Nenhum produto encontrado. Tente outro filtro.")
        return

    try:
        using_api = bool(st.secrets.get("ML_CLIENT_ID", ""))
    except Exception:
        using_api = False

    fonte = "Produtos reais do Mercado Livre" if using_api else "Produtos de demonstracao"
    st.markdown(f"**{len(products)} ofertas encontradas** | *{fonte}*")
    st.markdown("")

    for i in range(0, len(products), 3):
        row = products[i:i+3]
        cols = st.columns(3, gap="medium")
        for j, product in enumerate(row):
            with cols[j]:
                render_product_card(product)
        st.markdown("")
