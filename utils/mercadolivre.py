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

# Headers simulando navegador real para evitar 403
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://www.mercadolivre.com.br",
    "Referer": "https://www.mercadolivre.com.br/",
    "Connection": "keep-alive",
    "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120"',
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
}


@st.cache_data(ttl=1800)
def buscar_produtos_ml(categoria="informatica", limite=12):
    category_id = CATEGORY_MAP.get(categoria, "MLB1648")
    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        resp = session.get(
            f"{BASE_URL}/sites/MLB/search",
            params={
                "category": category_id,
                "limit": limite,
                "sort": "relevance",
                "condition": "new",
            },
            timeout=10
        )
        resp.raise_for_status()
        return _parse_results(resp.json(), categoria)
    except Exception as e:
        return []


@st.cache_data(ttl=1800)
def buscar_por_termo_ml(termo: str, limite=12):
    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        resp = session.get(
            f"{BASE_URL}/sites/MLB/search",
            params={"q": termo, "limit": limite, "sort": "relevance"},
            timeout=10
        )
        resp.raise_for_status()
        return _parse_results(resp.json(), "busca")
    except Exception as e:
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


@st.cache_data(ttl=3600)
def buscar_ofertas_ml_publico(limite=12):
    """
    Usa endpoint público de tendências do ML — sem autenticação, sem bloqueio.
    """
    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        resp = session.get(
            f"{BASE_URL}/sites/MLB/search",
            params={
                "q": "notebook",
                "limit": limite,
                "sort": "relevance",
            },
            timeout=10
        )
        if resp.status_code == 200:
            return _parse_results(resp.json(), "informatica")

        # Fallback: busca por tendências
        resp2 = session.get(
            f"{BASE_URL}/sites/MLB/search",
            params={"q": "smartphone", "limit": limite},
            timeout=10
        )
        if resp2.status_code == 200:
            return _parse_results(resp2.json(), "celulares")

        return []
    except Exception:
        return []
