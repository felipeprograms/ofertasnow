import streamlit as st
import requests

# ─────────────────────────────────────────────
# CONFIGURAÇÃO — substitua pelo seu App ID e Token
# Cadastre-se em: https://developers.mercadolivre.com.br
# Crie o app e copie o App ID. O Access Token pode ser
# gerado em: https://developers.mercadolivre.com.br/en_us/authentication-and-authorization
# ─────────────────────────────────────────────
ML_ACCESS_TOKEN = st.secrets.get("ML_ACCESS_TOKEN", "")  # Coloque no Streamlit Secrets
ML_AFFILIATE_ID = st.secrets.get("ML_AFFILIATE_ID", "")  # Seu ID de afiliado ML

BASE_URL = "https://api.mercadolibre.com"

CATEGORY_MAP = {
    "informatica": "MLB1648",   # Computadores e Acessórios
    "celulares":   "MLB1051",   # Celulares e Smartphones
    "tv":          "MLB1000",   # TV, Áudio e Vídeo
    "games":       "MLB1144",   # Video Games
    "casa":        "MLB1574",   # Eletrodomésticos
    "audio":       "MLB1000",   # Áudio
    "eletronicos": "MLB1000",   # Eletrônicos
}


def buscar_produtos_ml(categoria="informatica", limite=12, ordenar="price_asc"):
    """
    Busca produtos reais do Mercado Livre via API oficial.
    Retorna lista no mesmo formato do data/products.py para compatibilidade.
    """
    if not ML_ACCESS_TOKEN:
        return []  # Sem token, retorna vazio (usa mock)

    category_id = CATEGORY_MAP.get(categoria, "MLB1648")

    try:
        url = f"{BASE_URL}/sites/MLB/search"
        params = {
            "category": category_id,
            "limit": limite,
            "sort": ordenar,
            "condition": "new",
        }
        headers = {"Authorization": f"Bearer {ML_ACCESS_TOKEN}"}
        resp = requests.get(url, params=params, headers=headers, timeout=8)
        resp.raise_for_status()
        data = resp.json()

        products = []
        for item in data.get("results", []):
            original = item.get("original_price") or item["price"]
            price = item["price"]
            discount = int((1 - price / original) * 100) if original > price else 0

            # Monta link de afiliado
            affiliate_url = (
                f"https://www.mercadolivre.com.br/offsite?id={item['id']}"
                f"&matt_tool={ML_AFFILIATE_ID}&utm_source=ofertasnow&utm_medium=affiliate"
                if ML_AFFILIATE_ID
                else item.get("permalink", "#")
            )

            products.append({
                "id": f"ml_{item['id']}",
                "title": item["title"],
                "price": price,
                "original_price": original,
                "discount": discount,
                "image": item.get("thumbnail", "").replace("-I.jpg", "-O.jpg"),
                "marketplace": "mercadolivre",
                "rating": item.get("reviews", {}).get("rating_average", 4.0) or 4.0,
                "reviews": item.get("reviews", {}).get("total", 0) or 0,
                "affiliate_url": affiliate_url,
                "category": categoria,
                "tag": "🟡 Mercado Livre",
                "free_shipping": item.get("shipping", {}).get("free_shipping", False),
            })

        return products

    except Exception as e:
        st.warning(f"⚠️ Erro ao buscar no Mercado Livre: {e}")
        return []


def buscar_por_termo_ml(termo: str, limite=12):
    """Busca por termo livre (ex: 'notebook lenovo')."""
    if not ML_ACCESS_TOKEN:
        return []

    try:
        url = f"{BASE_URL}/sites/MLB/search"
        params = {
            "q": termo,
            "limit": limite,
            "condition": "new",
            "sort": "relevance",
        }
        headers = {"Authorization": f"Bearer {ML_ACCESS_TOKEN}"}
        resp = requests.get(url, params=params, headers=headers, timeout=8)
        resp.raise_for_keys()
        data = resp.json()

        products = []
        for item in data.get("results", []):
            original = item.get("original_price") or item["price"]
            price = item["price"]
            discount = int((1 - price / original) * 100) if original > price else 0

            affiliate_url = (
                f"https://www.mercadolivre.com.br/offsite?id={item['id']}"
                f"&matt_tool={ML_AFFILIATE_ID}&utm_source=ofertasnow&utm_medium=affiliate"
                if ML_AFFILIATE_ID
                else item.get("permalink", "#")
            )

            products.append({
                "id": f"ml_{item['id']}",
                "title": item["title"],
                "price": price,
                "original_price": original,
                "discount": discount,
                "image": item.get("thumbnail", "").replace("-I.jpg", "-O.jpg"),
                "marketplace": "mercadolivre",
                "rating": 4.0,
                "reviews": 0,
                "affiliate_url": affiliate_url,
                "category": "busca",
                "tag": "🟡 Mercado Livre",
                "free_shipping": item.get("shipping", {}).get("free_shipping", False),
            })

        return products

    except Exception as e:
        st.warning(f"⚠️ Erro na busca ML: {e}")
        return []
