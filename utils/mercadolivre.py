import streamlit as st
import requests

ML_CLIENT_ID = st.secrets.get("ML_CLIENT_ID", "")
ML_AFFILIATE_ID = st.secrets.get("ML_AFFILIATE_ID", "")  # Opcional por enquanto

BASE_URL = "https://api.mercadolibre.com"

CATEGORY_MAP = {
    "informatica": "MLB1648",
    "celulares":   "MLB1051",
    "tv":          "MLB1000",
    "games":       "MLB1144",
    "casa":        "MLB1574",
    "audio":       "MLB1000",
    "eletronicos": "MLB1132",
    "todos":       "MLB1648",
}


@st.cache_data(ttl=1800)  # Cache de 30 minutos para não sobrecarregar a API
def buscar_produtos_ml(categoria="informatica", limite=12):
    if not ML_CLIENT_ID:
        return []

    category_id = CATEGORY_MAP.get(categoria, "MLB1648")

    try:
        url = f"{BASE_URL}/sites/MLB/search"
        params = {
            "category": category_id,
            "limit": limite,
            "sort": "relevance",
            "condition": "new",
        }
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()

        products = []
        for item in data.get("results", []):
            original = item.get("original_price") or item["price"]
            price = item["price"]
            discount = int((1 - price / original) * 100) if original > price else 0

            # Link direto ao produto (sem afiliado por enquanto)
            product_url = item.get("permalink", "#")

            # Se tiver ID de afiliado no futuro, monta link rastreado
            if ML_AFFILIATE_ID:
                product_url = (
                    f"https://www.mercadolivre.com.br/offsite?id={item['id']}"
                    f"&matt_tool={ML_AFFILIATE_ID}&utm_source=ofertasnow&utm_medium=affiliate"
                )

            # Imagem em qualidade maior
            thumbnail = item.get("thumbnail", "")
            image = thumbnail.replace("-I.jpg", "-O.jpg") if thumbnail else ""

            products.append({
                "id": f"ml_{item['id']}",
                "title": item["title"],
                "price": price,
                "original_price": original,
                "discount": discount,
                "image": image,
                "marketplace": "mercadolivre",
                "rating": 4.2,
                "reviews": item.get("sold_quantity", 0) or 0,
                "affiliate_url": product_url,
                "category": categoria,
                "tag": "🟡 Mercado Livre",
                "free_shipping": item.get("shipping", {}).get("free_shipping", False),
            })

        return products

    except Exception as e:
        st.warning(f"⚠️ Erro ao buscar no Mercado Livre: {e}")
        return []


@st.cache_data(ttl=1800)
def buscar_por_termo_ml(termo: str, limite=12):
    if not ML_CLIENT_ID:
        return []

    try:
        url = f"{BASE_URL}/sites/MLB/search"
        params = {
            "q": termo,
            "limit": limite,
            "condition": "new",
            "sort": "relevance",
        }
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()

        products = []
        for item in data.get("results", []):
            original = item.get("original_price") or item["price"]
            price = item["price"]
            discount = int((1 - price / original) * 100) if original > price else 0
            thumbnail = item.get("thumbnail", "")
            image = thumbnail.replace("-I.jpg", "-O.jpg") if thumbnail else ""
            product_url = item.get("permalink", "#")

            if ML_AFFILIATE_ID:
                product_url = (
                    f"https://www.mercadolivre.com.br/offsite?id={item['id']}"
                    f"&matt_tool={ML_AFFILIATE_ID}&utm_source=ofertasnow&utm_medium=affiliate"
                )

            products.append({
                "id": f"ml_{item['id']}",
                "title": item["title"],
                "price": price,
                "original_price": original,
                "discount": discount,
                "image": image,
                "marketplace": "mercadolivre",
                "rating": 4.2,
                "reviews": item.get("sold_quantity", 0) or 0,
                "affiliate_url": product_url,
                "category": "busca",
                "tag": "🟡 Mercado Livre",
                "free_shipping": item.get("shipping", {}).get("free_shipping", False),
            })

        return products

    except Exception as e:
        st.warning(f"⚠️ Erro na busca ML: {e}")
        return []
