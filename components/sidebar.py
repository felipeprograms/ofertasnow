import streamlit as st
from data.products import PRODUCTS, MARKETPLACES

def render_sidebar():

    # Top 3 maiores descontos
    top = sorted(PRODUCTS, key=lambda p: p["discount"], reverse=True)[:4]
    mp_labels = {k: v["label"] for k, v in MARKETPLACES.items()}

    st.markdown('<div class="sidebar-widget">', unsafe_allow_html=True)
    st.markdown('<h4>🏆 Top descontos</h4>', unsafe_allow_html=True)
    for p in top:
        economy = p["original_price"] - p["price"]
        st.markdown(f"""
        <a href="{p['affiliate_url']}" target="_blank"
           style="display:block; text-decoration:none; margin-bottom:12px;
                  padding:10px; background:#111118; border-radius:10px;
                  border:1px solid #2a2a3a; transition:border-color 0.2s;">
            <div style="display:flex; gap:10px; align-items:center;">
                <img src="{p['image']}" style="width:48px; height:48px; object-fit:contain;
                     border-radius:6px; background:#0f0f13;"
                     onerror="this.src='https://via.placeholder.com/48x48/1a1a24/666?text=?'" />
                <div style="flex:1; min-width:0;">
                    <div style="font-size:12px; color:#ccc; line-height:1.3;
                         white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                        {p['title'][:45]}...
                    </div>
                    <div style="font-size:14px; font-weight:700; color:#fff; margin-top:3px;">
                        R$ {p['price']:,.2f}
                        <span style="font-size:11px; color:#00c853; font-weight:600;
                              background:#001a0a; padding:1px 5px; border-radius:4px; margin-left:4px;">
                            -{p['discount']}%
                        </span>
                    </div>
                </div>
            </div>
        </a>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Alerta de preço
    st.markdown('<div class="sidebar-widget">', unsafe_allow_html=True)
    st.markdown('<h4>🔔 Alerta de preço</h4>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:12px; color:#888; margin-bottom:10px;">Avise-me quando o preço baixar</p>', unsafe_allow_html=True)

    with st.form("price_alert_form", clear_on_submit=True):
        email = st.text_input("Seu e-mail", placeholder="voce@email.com",
                              label_visibility="collapsed")
        product_name = st.text_input("Produto", placeholder="Nome do produto",
                                     label_visibility="collapsed")
        target_price = st.number_input("Preço desejado (R$)", min_value=1.0,
                                       value=500.0, step=50.0,
                                       label_visibility="collapsed",
                                       format="%.2f")
        submitted = st.form_submit_button("🔔 Criar alerta", use_container_width=True)
        if submitted and email:
            st.success(f"✅ Alerta criado! Você será avisado quando {product_name or 'o produto'} atingir R$ {target_price:,.2f}")

    st.markdown('</div>', unsafe_allow_html=True)

    # Marketplaces rápidos
    st.markdown('<div class="sidebar-widget">', unsafe_allow_html=True)
    st.markdown('<h4>🛍️ Marketplaces</h4>', unsafe_allow_html=True)
    marketplace_links = [
        ("🟡", "Mercado Livre", "mercadolivre", "https://www.mercadolivre.com.br"),
        ("🟠", "Amazon Brasil", "amazon", "https://www.amazon.com.br"),
        ("🔴", "Shopee", "shopee", "https://shopee.com.br"),
        ("🟤", "KaBuM!", "kabum", "https://www.kabum.com.br"),
        ("🔵", "Pichau", "pichau", "https://www.pichau.com.br"),
    ]
    for emoji, label, mkt_id, url in marketplace_links:
        count = len([p for p in PRODUCTS if p["marketplace"] == mkt_id])
        st.markdown(f"""
        <a href="{url}" target="_blank"
           style="display:flex; justify-content:space-between; align-items:center;
                  padding:8px 0; border-bottom:1px solid #1a1a24; text-decoration:none;">
            <span style="font-size:13px; color:#ccc;">{emoji} {label}</span>
            <span style="font-size:11px; color:#ff6b00; font-weight:600;">{count} ofertas</span>
        </a>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Instagram CTA
    st.markdown("""
    <div style="background:linear-gradient(135deg,#833ab4,#fd1d1d,#fcb045);
                border-radius:14px; padding:16px; text-align:center; margin-top:4px;">
        <div style="font-size:22px; margin-bottom:4px;">📲</div>
        <div style="font-weight:700; color:#fff; font-size:14px; margin-bottom:4px;">
            Siga no Instagram
        </div>
        <div style="color:rgba(255,255,255,0.85); font-size:12px; margin-bottom:10px;">
            130k seguidores • Ofertas exclusivas todo dia
        </div>
        <a href="https://instagram.com/seuusuario" target="_blank"
           style="background:white; color:#833ab4; font-weight:700; font-size:13px;
                  padding:8px 20px; border-radius:8px; text-decoration:none; display:inline-block;">
            @seuusuario →
        </a>
    </div>
    """, unsafe_allow_html=True)
