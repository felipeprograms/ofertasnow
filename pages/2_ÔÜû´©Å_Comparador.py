import streamlit as st
from utils.config import setup_page
from data.products import PRODUCTS, MARKETPLACES

setup_page()

st.title("⚖️ Comparador de Produtos")
st.caption("Compare até 3 produtos lado a lado e escolha a melhor oferta")

# Seleção de produtos
all_titles = {p["id"]: p["title"][:60] + "..." for p in PRODUCTS}

col1, col2, col3 = st.columns(3)
with col1:
    id1 = st.selectbox("Produto 1", options=list(all_titles.keys()),
                        format_func=lambda x: all_titles[x], index=0)
with col2:
    id2 = st.selectbox("Produto 2", options=list(all_titles.keys()),
                        format_func=lambda x: all_titles[x], index=1)
with col3:
    id3 = st.selectbox("Produto 3 (opcional)", options=["Nenhum"] + list(all_titles.keys()),
                        format_func=lambda x: "— Nenhum —" if x == "Nenhum" else all_titles[x])

selected_ids = [id1, id2] + ([id3] if id3 != "Nenhum" else [])
selected = [p for p in PRODUCTS if p["id"] in selected_ids]

# Ordena pela seleção do usuário
selected = sorted(selected, key=lambda p: selected_ids.index(p["id"]))

st.divider()

if len(selected) < 2:
    st.info("Selecione ao menos 2 produtos para comparar.")
    st.stop()

# --- Cabeçalhos com imagem e título ---
cols = st.columns(len(selected), gap="large")
for i, p in enumerate(selected):
    with cols[i]:
        mp_label = MARKETPLACES.get(p["marketplace"], {}).get("label", p["marketplace"])
        st.image(p["image"], use_container_width=True)
        st.markdown(f"**{p['title'][:65]}...**")
        st.caption(f"🏪 {mp_label}")

st.divider()

# --- Tabela de comparação ---
st.markdown("### 📊 Comparativo")

campos = [
    ("💰 Preço atual",       lambda p: f"R$ {p['price']:,.2f}"),
    ("🏷️ Preço original",   lambda p: f"R$ {p['original_price']:,.2f}"),
    ("🔥 Desconto",          lambda p: f"{p['discount']}% OFF"),
    ("💚 Economia",          lambda p: f"R$ {p['original_price'] - p['price']:,.2f}"),
    ("⭐ Avaliação",         lambda p: f"{'★' * int(p['rating'])} ({p['rating']})"),
    ("💬 Reviews",           lambda p: f"{p['reviews']:,}"),
    ("🚚 Frete",             lambda p: "Grátis ✅" if p["free_shipping"] else "A calcular"),
    ("🏪 Marketplace",       lambda p: MARKETPLACES.get(p["marketplace"], {}).get("label", "")),
]

# Destaca o melhor em cada campo numérico
def highlight_best(values, mode="min"):
    try:
        nums = [float(v.replace("R$","").replace(".","").replace(",",".").replace("%","").split()[0]) for v in values]
        best_idx = nums.index(min(nums) if mode == "min" else max(nums))
        return best_idx
    except Exception:
        return -1

for label, fn in campos:
    row_cols = st.columns([1] + [1] * len(selected))
    with row_cols[0]:
        st.markdown(f"**{label}**")

    values = [fn(p) for p in selected]
    mode = "min" if "Preço" in label or "Frete" in label else "max"
    best = highlight_best(values, mode) if "Avaliação" in label or "Preço atual" in label or "Desconto" in label else -1

    for i, (p, val) in enumerate(zip(selected, values)):
        with row_cols[i + 1]:
            if i == best:
                st.markdown(f"✅ **{val}**")
            else:
                st.markdown(val)

st.divider()

# --- Botões de compra ---
st.markdown("### 🛒 Ir para a loja")
btn_cols = st.columns(len(selected), gap="medium")
for i, p in enumerate(selected):
    mp_label = MARKETPLACES.get(p["marketplace"], {}).get("label", p["marketplace"])
    with btn_cols[i]:
        st.link_button(
            f"Comprar por R$ {p['price']:,.2f} →",
            url=p["affiliate_url"],
            use_container_width=True,
            type="primary",
        )
        st.caption(f"no {mp_label}")

# Recomendação automática
melhor = min(selected, key=lambda p: p["price"])
mp_melhor = MARKETPLACES.get(melhor["marketplace"], {}).get("label", "")
st.success(f"💡 **Melhor oferta:** {melhor['title'][:50]}... por **R$ {melhor['price']:,.2f}** no {mp_melhor} (-{melhor['discount']}% OFF)")
