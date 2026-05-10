import streamlit as st
from utils.config import setup_page
from data.products import PRODUCTS, MARKETPLACES
import pandas as pd
import random
from datetime import datetime, timedelta

setup_page()

st.title("📊 Painel Administrativo")
st.caption("Analytics de cliques, receita e performance por marketplace")

# --- KPIs principais ---
st.markdown("### 📈 Resumo do mês")
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("Cliques totais", "12.847", delta="+18% vs mês ant.")
with k2:
    st.metric("Conversões", "384", delta="+12%")
with k3:
    st.metric("Receita estimada", "R$ 2.341,00", delta="+R$ 310")
with k4:
    st.metric("Taxa de conversão", "2,99%", delta="+0.3pp")

st.divider()

# --- Cliques por dia (últimos 30 dias) ---
st.markdown("### 📅 Cliques por dia")
dates = [datetime.today() - timedelta(days=i) for i in range(29, -1, -1)]
clicks = [random.randint(200, 800) for _ in dates]
conversions = [int(c * random.uniform(0.02, 0.05)) for c in clicks]
df_daily = pd.DataFrame({
    "Data": dates,
    "Cliques": clicks,
    "Conversões": conversions,
})
st.line_chart(df_daily.set_index("Data"))

# --- Performance por marketplace ---
st.markdown("### 🏪 Performance por marketplace")
mp_data = []
for key, val in MARKETPLACES.items():
    prods = [p for p in PRODUCTS if p["marketplace"] == key]
    cliques = random.randint(500, 4000)
    conv = random.randint(10, 120)
    receita = round(conv * random.uniform(5, 25), 2)
    mp_data.append({
        "Marketplace": val["label"],
        "Produtos": len(prods),
        "Cliques": cliques,
        "Conversões": conv,
        "Receita (R$)": receita,
        "Tx. Conversão": f"{conv/cliques*100:.2f}%",
    })
df_mp = pd.DataFrame(mp_data).sort_values("Receita (R$)", ascending=False)
st.dataframe(df_mp, use_container_width=True, hide_index=True)

st.bar_chart(df_mp.set_index("Marketplace")["Cliques"])

st.divider()

# --- Produtos mais clicados ---
st.markdown("### 🔥 Produtos mais clicados")
top_products = sorted(PRODUCTS, key=lambda p: p["reviews"], reverse=True)[:5]
for p in top_products:
    mp_label = MARKETPLACES.get(p["marketplace"], {}).get("label", "")
    c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 1])
    with c1:
        st.markdown(f"**{p['title'][:55]}...**")
    with c2:
        st.caption(mp_label)
    with c3:
        st.caption(f"R$ {p['price']:,.2f}")
    with c4:
        cliques = random.randint(100, 1200)
        st.caption(f"👆 {cliques:,}")
    with c5:
        receita = round(cliques * random.uniform(0.02, 0.05) * p["price"] * 0.05, 2)
        st.caption(f"💰 R$ {receita:,.2f}")

st.divider()

# --- Gerenciar produtos ---
st.markdown("### ➕ Adicionar produto manualmente")
with st.form("add_product"):
    col_a, col_b = st.columns(2)
    with col_a:
        title = st.text_input("Título do produto")
        price = st.number_input("Preço (R$)", min_value=1.0, value=100.0, step=10.0)
        original = st.number_input("Preço original (R$)", min_value=1.0, value=150.0, step=10.0)
    with col_b:
        image_url = st.text_input("URL da imagem")
        affiliate_url = st.text_input("Link de afiliado")
        marketplace = st.selectbox("Marketplace", list(MARKETPLACES.keys()),
                                    format_func=lambda x: MARKETPLACES[x]["label"])
    submitted = st.form_submit_button("Adicionar produto", type="primary")
    if submitted:
        if title and affiliate_url:
            st.success(f"✅ Produto '{title[:40]}...' adicionado com sucesso! (Em produção, seria salvo no banco de dados)")
        else:
            st.warning("Preencha pelo menos o título e o link de afiliado.")
