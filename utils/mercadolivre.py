import streamlit as st
import requests

ML_AFFILIATE_ID = st.secrets.get("ML_AFFILIATE_ID", "")

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

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
}


@st.cache_data(ttl=1800)
def buscar_produtos_ml(categoria="informatica", limite=12):
    category_id = CATEGORY_MAP.get(categoria, "MLB1648")
    try:
        resp = requests.get(
            f"{BASE_URL}/sites/MLB/search",
            params={"category": category_id, "limit": limite, "sort": "relevance"},
            headers=HEADERS,
            timeout=10
        )
        resp.raise_for_status()
        return _parse_results(resp.json(), categoria)
    except Exception as e:
        st.warning(f"Erro ML: {e}")
        return []


@st.cache_data(ttl=1800)
def buscar_por_termo_ml(termo: str, limite=12):
    try:
        resp = requests.get(
            f"{BASE_URL}/sites/MLB/search",
            params={"q": termo, "limit": limite, "sort": "relevance"},
            headers=HEADERS,
            timeout=10
        )
        resp.raise_for_status()
        return _parse_results(resp.json(), "busca")
    except Exception as e:
        st.warning(f"Erro ML busca: {e}")
        return []


def _parse_results(data, categoria):
    products = []
    for item in data.get("results", []):
        original = item.get("original_price") or item["price"]
        price = item["price"]
        discount = int((1 - price / original) * 100) if original > price else 0

        # Permalink é a URL direta e pública do produto no ML
        url = item.get("permalink", "https://www.mercadolivre.com.br")

        thumbnail = item.get("thumbnail", "")
        # Força imagem maior
        image = thumbnail.replace("-I.jpg", "-O.jpg").replace("http://", "https://")

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
            "affiliate_url": url,
            "category": categoria,
            "tag": "Mercado Livre",
            "free_shipping": item.get("shipping", {}).get("free_shipping", False),
        })
    return products
