import streamlit as st
from utils.config import setup_page
from data.products import PRODUCTS, MARKETPLACES

setup_page()

# Página de Bio Link — design limpo para link na bio do Instagram
st.markdown("""
<div style="max-width:480px; margin:0 auto; text-align:center; padding-top:20px;">
""", unsafe_allow_html=True)

# Avatar e nome
col_av, col_info = st.columns([1, 3])
with col_av:
    st.markdown("# 🔥")
with col_info:
    st.markdown("### OfertasNow")
    st.caption("Melhores ofertas do Brasil • 130k seguidores")

st.divider()

# Oferta do dia em destaque
top = sorted(PRODUCTS, key=lambda p: p["discount"], reverse=True)[0]
mp_label = MARKETPLACES.get(top["marketplace"], {}).get("label", "")

st.markdown("#### 🏆 Oferta do dia")
with st.container(border=True):
    c1, c2 = st.columns([1, 2])
    with c1:
        st.image(top["image"], use_container_width=True)
    with c2:
        st.markdown(f"**{top['title'][:55]}...**")
        st.markdown(f"### R$ {top['price']:,.2f}")
        st.caption(f"~~R$ {top['original_price']:,.2f}~~ · -{top['discount']}% OFF")
        st.link_button(f"🛒 Ver no {mp_label}", url=top["affiliate_url"],
                       use_container_width=True, type="primary")

st.markdown("---")

# Links rápidos por categoria
st.markdown("#### 🗂️ Navegar por categoria")

categorias_links = [
    ("💻 Informática", "informatica"),
    ("📱 Celulares",   "celulares"),
    ("🎮 Games",       "games"),
    ("📺 TV e Áudio",  "tv"),
    ("🏠 Casa",        "casa"),
]

for label, cat in categorias_links:
    count = len([p for p in PRODUCTS if p["category"] == cat])
    c1, c2 = st.columns([4, 1])
    with c1:
        st.link_button(f"{label} ({count} ofertas)",
                       url=f"/?cat={cat}",
                       use_container_width=True)

st.markdown("---")

# Alertas e redes
st.markdown("#### 🔔 Receba alertas de oferta")
email = st.text_input("", placeholder="Seu e-mail", label_visibility="collapsed")
if st.button("Quero receber alertas", use_container_width=True, type="primary"):
    if email:
        st.success(f"✅ {email} cadastrado! Você receberá as melhores ofertas.")
    else:
        st.warning("Insira seu e-mail.")

st.markdown("---")

# Redes sociais
st.markdown("#### 📲 Me siga nas redes")
r1, r2, r3 = st.columns(3)
with r1:
    st.link_button("📸 Instagram", url="https://instagram.com/seuusuario", use_container_width=True)
with r2:
    st.link_button("📱 TikTok", url="https://tiktok.com/@seuusuario", use_container_width=True)
with r3:
    st.link_button("✈️ Telegram", url="https://t.me/seucanal", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)
