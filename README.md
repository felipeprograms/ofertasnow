# ⚡ OfertasNow — Plataforma de Afiliados

Plataforma de recomendação de produtos com links de afiliados, integrada com Mercado Livre, Amazon, Shopee, KaBuM! e Pichau.

## 🚀 Como rodar localmente

### 1. Instale o Python (se não tiver)
Baixe em: https://www.python.org/downloads/

### 2. Clone o repositório
```bash
git clone https://github.com/SEUUSUARIO/ofertasnow.git
cd ofertasnow
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Rode o projeto
```bash
streamlit run app.py
```

A plataforma abrirá em: http://localhost:8501

---

## ☁️ Deploy gratuito no Streamlit Cloud

1. Suba o código para o GitHub (pasta `ofertasnow/`)
2. Acesse https://streamlit.io/cloud
3. Clique em **"New app"**
4. Selecione seu repositório e o arquivo `app.py`
5. Clique em **Deploy** — pronto, seu site está no ar!

---

## 📁 Estrutura do projeto

```
ofertasnow/
├── app.py                  # Arquivo principal
├── requirements.txt        # Dependências
├── data/
│   └── products.py         # Produtos e categorias (edite aqui!)
├── components/
│   ├── header.py           # Cabeçalho e busca
│   ├── feed.py             # Grid de produtos
│   └── sidebar.py          # Barra lateral (alertas, top ofertas)
└── utils/
    └── config.py           # Configuração visual e CSS
```

---

## 🛒 Como adicionar seus links de afiliado

Edite o arquivo `data/products.py` e substitua os links:

```python
# Amazon Associates
"affiliate_url": "https://www.amazon.com.br/dp/CODIGO?tag=SEU-TAG-20",

# Mercado Livre Afiliados
"affiliate_url": "https://mercadolivre.com/sec/CODIGO?matt_tool=SEU-ID",

# Shopee
"affiliate_url": "https://shope.ee/SEU-CODIGO",

# KaBuM!
"affiliate_url": "https://www.kabum.com.br/produto/CODIGO?utm_source=SEU-UTM",
```

---

## 📲 Personalize para seu Instagram

No arquivo `components/sidebar.py`, linha final:
```python
href="https://instagram.com/SEUUSUARIO"  # Troque pelo seu @
```

No arquivo `components/header.py`:
```python
📲 130k no Instagram  # Troque pelo seu número de seguidores
```

---

## 🔜 Próximos passos (em desenvolvimento)

- [ ] Integração real com API Mercado Livre
- [ ] Integração real com Amazon Product Advertising API
- [ ] Sistema de alerta de preço com e-mail (Gmail SMTP)
- [ ] Página de comparativo entre produtos
- [ ] Blog com reviews gerados por IA
- [ ] Painel admin com analytics de cliques
- [ ] Histórico de preços com gráfico
- [ ] Chatbot recomendador com IA

---

## 💰 Programas de afiliados para se cadastrar (gratuito)

| Programa | Link de cadastro |
|----------|-----------------|
| Amazon Associates | https://associados.amazon.com.br |
| Mercado Livre Afiliados | https://afiliados.mercadolivre.com.br |
| Shopee Affiliate | https://affiliate.shopee.com.br |
| Lomadee | https://www.lomadee.com |
| Awin | https://www.awin.com/br |
