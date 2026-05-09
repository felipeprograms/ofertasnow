import streamlit as st
from data.products import PRODUCTS, CATEGORIES, MARKETPLACES

def render_product_card(product):
    mp = MARKETPLACES.get(product["marketplace"], {})
    badge_class = mp.get("badge_class", "badge-ml")
    mp_label = mp.get("label", product["marketplace"])
    economy = product["original_price"] - product["price"]
    stars = "★" * int(product["rating"]) + "☆" * (5 - int(product["rating"]))
    shipping = "✅ Frete grátis" if product["free_shipping"] else "🚚 Frete a calcular"

    st.markdown(f"""
    <div class="product-card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">
            <span class="discount-badge">-{product['discount']}% OFF</span>
            <span class="marketplace-badge {badge_class}">{mp_label}</span>
        </div>

        <div style="text-align:center; background:#111118; border-radius:10px; padding:12px; margin-bottom:8px;">
            <img src="{product['image']}" style="max-height:160px; max-width:100%; object-fit:contain; border-radius:6px;"
                 onerror="this.src='https://via.placeholder.com/200x160/1a1a24/666?text=Produto'" />
        </div>

        <div style="background:#111; border-radius:6px; padding:3px 8px; display:inline-block; margin-bottom:6px;">
            <span style="font-size:11px; color:#ff6b00; font-weight:600;">{product['tag']}</span>
        </div>

        <p class="product-title">{product['title']}</p>

        <div style="margin:8px 0;">
            <span class="price-main">R$ {product['price']:,.2f}</span><br>
            <span class="price-original">R$ {product['original_price']:,.2f}</span>
            <span class="price-economy"> • Economia de R$ {economy:,.2f}</span>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
            <span class="rating">{stars} <span style="color:#888; font-size:11px;">({product['reviews']:,})</span></span>
            <span style="font-size:11px; color:#666;">{shipping}</span>
        </div>

        <a href="{product['affiliate_url']}" target="_blank" class="buy-btn">
            🛒 Ver oferta no {mp_label} →
        </a>
    </div>
    """, unsafe_allow_html=True)


def filter_products():
    products = PRODUCTS.copy()

    # Filtro de busca
    q = st.session_state.get("search_query", "").lower().strip()
    if q:
        products = [p for p in products if q in p["title"].lower() or q in p["category"].lower()]

    # Filtro de categoria
    cat = st.session_state.get("selected_category", "todos")
    if cat != "todos":
        products = [p for p in products if p["category"] == cat]

    # Filtro de marketplace
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

    # Ordenação
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
    # Chips de categoria
    st.markdown('<div style="margin-bottom:16px;">', unsafe_allow_html=True)
    if "selected_category" not in st.session_state:
        st.session_state["selected_category"] = "todos"

    cols = st.columns(len(CATEGORIES))
    for i, cat in enumerate(CATEGORIES):
        with cols[i]:
            active = "🔸" if st.session_state["selected_category"] == cat["id"] else ""
            if st.button(f"{active}{cat['label']}", key=f"cat_{cat['id']}",
                         use_container_width=True):
                st.session_state["selected_category"] = cat["id"]
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    products = filter_products()

    if not products:
        st.markdown("""
        <div style="text-align:center; padding:60px 20px; color:#666;">
            <div style="font-size:40px; margin-bottom:12px;">🔍</div>
            <p style="font-size:16px;">Nenhum produto encontrado.</p>
            <p style="font-size:13px;">Tente buscar por outro termo ou limpar os filtros.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Contagem e título
    st.markdown(f"""
    <div class="section-title">
        🔥 {len(products)} ofertas encontradas
        <span style="font-size:13px; font-weight:400; color:#666; margin-left:8px;">
            Atualizado agora
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Grid de produtos — 3 colunas
    for i in range(0, len(products), 3):
        row = products[i:i+3]
        cols = st.columns(3)
        for j, product in enumerate(row):
            with cols[j]:
                render_product_card(product)
        st.markdown("<br>", unsafe_allow_html=True)
