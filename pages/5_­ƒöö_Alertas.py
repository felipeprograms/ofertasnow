import streamlit as st
from utils.config import setup_page
from data.products import PRODUCTS, MARKETPLACES
import pandas as pd
from datetime import datetime

setup_page()

st.title("🔔 Alertas de Preço")
st.caption("Crie alertas e seja notificado quando o preço cair")

# Formulário de criação de alerta
st.markdown("### ➕ Novo alerta")

with st.form("alert_form"):
    col1, col2 = st.columns([2, 1])
    with col1:
        product_id = st.selectbox(
            "Selecione o produto",
            options=[p["id"] for p in PRODUCTS],
            format_func=lambda x: next(p["title"][:70] + "..." for p in PRODUCTS if p["id"] == x)
        )
    with col2:
        email = st.text_input("Seu e-mail", placeholder="voce@email.com")

    selected_product = next(p for p in PRODUCTS if p["id"] == product_id)
    current_price = selected_product["price"]

    col3, col4 = st.columns(2)
    with col3:
        target_price = st.number_input(
            f"Preço desejado (atual: R$ {current_price:,.2f})",
            min_value=1.0,
            value=round(current_price * 0.85, 2),
            step=10.0, format="%.2f"
        )
    with col4:
        notify_via = st.multiselect("Notificar via", ["E-mail", "Push", "Telegram"], default=["E-mail"])

    submitted = st.form_submit_button("🔔 Criar alerta", type="primary", use_container_width=True)
    if submitted:
        if email:
            diff = current_price - target_price
            pct = (diff / current_price) * 100
            st.success(f"✅ Alerta criado! Você será avisado quando o preço cair R$ {diff:,.2f} ({pct:.0f}%) para R$ {target_price:,.2f}")
        else:
            st.warning("Insira seu e-mail.")

st.divider()

# Alertas existentes (simulados)
st.markdown("### 📋 Seus alertas ativos")

alertas_simulados = [
    {"produto": PRODUCTS[0]["title"][:50] + "...", "atual": PRODUCTS[0]["price"],
     "alvo": PRODUCTS[0]["price"] * 0.85, "status": "🟡 Aguardando", "criado": "08/05/2025"},
    {"produto": PRODUCTS[1]["title"][:50] + "...", "atual": PRODUCTS[1]["price"],
     "alvo": PRODUCTS[1]["price"] * 0.80, "status": "🟢 Atingido!", "criado": "05/05/2025"},
    {"produto": PRODUCTS[3]["title"][:50] + "...", "atual": PRODUCTS[3]["price"],
     "alvo": PRODUCTS[3]["price"] * 0.90, "status": "🟡 Aguardando", "criado": "01/05/2025"},
]

df = pd.DataFrame(alertas_simulados)
df.columns = ["Produto", "Preço atual", "Preço alvo", "Status", "Criado em"]
df["Preço atual"] = df["Preço atual"].apply(lambda x: f"R$ {x:,.2f}")
df["Preço alvo"] = df["Preço alvo"].apply(lambda x: f"R$ {x:,.2f}")

st.dataframe(df, use_container_width=True, hide_index=True)

# Dica
st.info("💡 **Dica:** Ative notificações push no navegador para receber alertas instantâneos sem abrir o site!")
