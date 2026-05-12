
import os
import requests
import streamlit as st
import csv
import io

SHOPEE_FEED_URL = os.environ.get("SHOPEE_FEED_URL", "")

def get_secret(key, default=""):
    val = os.environ.get(key, "")
    if val:
        return val
    try:
        return st.secrets.get(key, default)
    except Exception:
        return default


@st.cache_data(ttl=3600)  # Cache de 1 hora
def buscar_produtos_shopee(categoria="", limite=12):
    """
    Baixa o feed CSV da Shopee Affiliate e retorna produtos formatados.
    """
    feed_url = get_secret("SHOPEE_FEED_URL", "")
    if not feed_url:
        return []

    try:
        resp = requests.get(feed_url, timeout=30,
                           headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()

        # Decodifica o CSV
        content = resp.content.decode("utf-8", errors="ignore")
        reader = csv.DictReader(io.StringIO(content))

        products = []
        keywords = {
            "informatica": ["notebook", "computador", "pc", "monitor", "teclado", "mouse", "ssd"],
            "celulares":   ["celular", "smartphone", "iphone", "samsung", "xiaomi", "redmi"],
            "games":       ["gamer", "game", "controle", "headset", "playstation", "xbox"],
            "audio":       ["fone", "headphone", "caixa de som", "speaker", "bluetooth"],
            "casa":        ["aspirador", "ventilador", "liquidificador", "cafeteira", "fritadeira"],
            "tv":          ["tv", "televisão", "smart tv", "televisor"],
        }

        for row in reader:
            if len(products) >= limite:
                break

            try:
                title = row.get("product_name", "") or row.get("name", "") or row.get("titulo", "")
                price_str = row.get("price", "") or row.get("preco", "") or row.get("sale_price", "")
                original_str = row.get("original_price", "") or row.get("preco_original", "") or price_str
                image = row.get("image_url", "") or row.get("imagem", "") or row.get("image", "")
                affiliate_url = row.get("affiliate_link", "") or row.get("link", "") or row.get("url", "")

                if not title or not affiliate_url:
                    continue

                # Limpa preço
                price = float(str(price_str).replace("R$", "").replace(".", "").replace(",", ".").strip() or 0)
                original = float(str(original_str).replace("R$", "").replace(".", "").replace(",", ".").strip() or price)

                if price <= 0:
                    continue

                discount = int((1 - price / original) * 100) if original > price else 0

                # Detecta categoria pelo título
                cat = "eletronicos"
                title_lower = title.lower()
                for cat_key, kws in keywords.items():
                    if any(kw in title_lower for kw in kws):
                        cat = cat_key
                        break

                # Filtra por categoria se especificado
                if categoria and categoria != "todos" and cat != categoria:
                    continue

                products.append({
                    "id": f"shopee_{hash(title) % 99999}",
                    "title": title,
                    "price": price,
                    "original_price": original,
                    "discount": discount,
                    "image": image,
                    "marketplace": "shopee",
                    "rating": 4.3,
                    "reviews": 0,
                    "affiliate_url": affiliate_url,
                    "category": cat,
                    "tag": "Shopee",
                    "free_shipping": True,
                })

            except Exception:
                continue

        return products

    except Exception as e:
        return []
