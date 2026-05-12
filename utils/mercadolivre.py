import os
import requests
import streamlit as st

def get_secret(key, default=""):
    val = os.environ.get(key, "")
    if val:
        return val
    try:
        return st.secrets.get(key, default)
    except Exception:
        return default

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


@st.cache_data(ttl=3600)
def get_access_token():
    """Gera token via Client Credentials — não precisa de autorização do usuário."""
    client_id = get_secret("ML_CLIENT_ID", "")
    client_secret = get_secret("ML_CLIENT_SECRET", "")
    if not client_id or not client_secret:
        return ""
    try:
        resp = requests.post(
            "https://api.mercadolibre.com/oauth/token",
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
            headers={"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        resp.raise_for_status()
        return resp.json().get("access_token", "")
    except Exception as e:
        return ""


@st.cache_data(ttl=1800)
def buscar_produtos_ml(categoria="informatica", limite=12):
    token = get_access_token()
    category_id = CATEGORY_MAP.get(categoria, "MLB1648")
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        resp = requests.get(
            f"{BASE_URL}/sites/MLB/search",
            params={"category": category_id, "limit": limite, "sort": "relevance"},
            headers=headers,
            timeout=10
        )
        resp.raise_for_status()
        return _parse_results(resp.json(), categoria)
    except Exception as e:
        st.warning(f"Erro ML: {e}")
        return []


@st.cache_data(ttl=1800)
def buscar_por_termo_ml(termo: str, limite=12):
    token = get_access_token()
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        resp = requests.get(
            f"{BASE_URL}/sites/MLB/search",
            params={"q": termo, "limit": limite, "sort": "relevance"},
            headers=headers,
            timeout=10
        )
        resp.raise_for_status()
        return _parse_results(resp.json(), "busca")
    except Exception as e:
        st.warning(f"Erro ML busca: {e}")
        return []


def _parse_results(data, categoria):
    products = []
    affiliate_id = get_secret("ML_AFFILIATE_ID", "")
    for item in data.get("results", []):
        original = item.get("original_price") or item["price"]
        price = item["price"]
        discount = int((1 - price / original) * 100) if original > price else 0
        url = item.get("permalink", "https://www.mercadolivre.com.br")
        if affiliate_id:
            url = (f"https://www.mercadolivre.com.br/offsite?id={item['id']}"
                   f"&matt_tool={affiliate_id}&utm_source=ofertasnow&utm_medium=affiliate")
        thumbnail = item.get("thumbnail", "")
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
