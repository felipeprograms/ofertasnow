import streamlit as st
from data.products import PRODUCTS, CATEGORIES, MARKETPLACES


def render_product_card(product):
    mp = MARKETPLACES.get(product["marketplace"], {})
    mp_label = mp.get("label", product["marketplace"])
    economy = product["original_price"] - product["price"]
    stars = "★" * int(product["rating"]) + "☆" * (5 - int(product["rating"]))
    shipping = "✅ Frete grátis" if product["free_shipping"] else "🚚 Calcular frete"

    mp_colors = {
        "mercadolivre": "background:#ffe600; color:#222;",
        "amazon":       "background:#ff9900; color:#111;",
        "shopee":       "background:#ee4d2d; color:#fff;",
        "kabum":        "background:#ff6600; color:#fff;",
        "pichau":       "background:#0066cc; color:#fff;",
    }
    mp_badge_style = mp_colors.get(product["marketplace"], "background:#444; color:#fff;")
    title_short = product['title'][:80] + ('...' if len(product['title']) > 80 else '')

    st.markdown(f"""
    <div style="background:#1a1a24; border:1px solid #2a2a3a; border-radius:16px;
                padding:16px; box-sizing:border-box; margin-bottom:4px;">

        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <span style="background:linear-gradient(135deg,#ff3c00,#ff6b00); color:#fff;
                         font-size:12px; font-weight:700; padding:4px 10px; border-radius:20px;">
                -{product['discount']}% OFF
            </span>
            <span style="font-size:11px; font-weight:700; padding:4px 10px; border-radius:8px; {mp_badge_style}">
                {mp_label}
            </span>
        </div>

        <div style="text-align:center; background:#111118; border-radius:10px;
                    padding:14px; margin-bottom:10px; height:140px;
                    display:flex; align-items:center; justify-content:center;">
            <img src="{product['image']}"
                 style="max-height:120px; max-width:100%; object-fit:contain;"
                 onerror="this.style.display='none'" />
        </div>

        <div style="background:#111; border-radius:6px; padding:3px 8px;
                    display:inline-block; margin-bottom:8px;">
            <span style="font-size:11px; color:#ff6b00; font-weight:600;">{product['tag']}</span>
        </div>

        <p style="font-size:13px; font-weight:500; color:#e0e0e0; margin:0 0 10px;
                  line-height:1.4; min-height:36px;">{title_short}</p>

        <div style="margin-bottom:10px;">
            <div style="font-size:22px; font-weight:800; color:#ffffff;">
                R$ {product['price']:,.2f}
            </div>
            <div style="margin-top:3px;">
                <span style="font-size:12px; color:#777; text-decoration:line-through;">
                    R$ {product['original_price']:,.2f}
                </span>
                <span style="font-size:12px; color:#00c853; font-weight:600; margin-left:6px;">
                    Economia R$ {economy:,.2f}
                </span>
            </div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <span style="color:#ffc107; font-size:12px;">
                {stars} <span style="color:#666; font-size:11px;">({product['reviews']:,})</span>
            </span>
            <span style="font-size:11px; color:#666;">{shipping}</span>
        </div>

        <a href="{product['affiliate_url']}" target="_blank"
           style="display:block; width:100%; background:linear-gradient(135deg,#ff6b00,#ff3c00);
                  color:#fff !important; text-align:center; padding:11px 0; border-radius:10px;
                  font-weight:700; font-size:13px; text-decoration:none; box-sizing:border-box;">
            Comprar no {mp_label} &rarr;
        </a>
    </div>
    """, unsafe_allow_html=True)


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

    # Botões de categoria — usando st.button com CSS override via config
    cols_cat = st.columns(len(CATEGORIES))
    for i, cat in enumerate(CATEGORIES):
        with cols_cat[i]:
            is_active = selected == cat["id"]
            btn_type = "primary" if is_active else "secondary"
            if st.button(cat["label"], key=f"catbtn_{cat['id']}",
                         use_container_width=True, type=btn_type):
                st.session_state["selected_category"] = cat["id"]
                st.rerun()

    st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)

    products = filter_products()

    if not products:
        st.markdown("""
        <div style="text-align:center; padding:60px 20px;">
            <div style="font-size:40px; margin-bottom:12px;">🔍</div>
            <p style="font-size:16px; color:#888;">Nenhum produto encontrado.</p>
            <p style="font-size:13px; color:#555;">Tente outro termo ou limpe os filtros.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(f"""
    <div style="font-size:18px; font-weight:700; color:#fff; margin:4px 0 16px;
                display:flex; align-items:center; gap:8px;">
        🔥 {len(products)} ofertas encontradas
        <span style="font-size:13px; font-weight:400; color:#555;">Atualizado agora</span>
    </div>
    """, unsafe_allow_html=True)

    for i in range(0, len(products), 3):
        row = products[i:i+3]
        cols = st.columns(3, gap="medium")
        for j, product in enumerate(row):
            with cols[j]:
                render_product_card(product)
        st.markdown("<div style='margin-bottom:4px;'></div>", unsafe_allow_html=True)
