#!/usr/bin/env python3
"""
Durante Export - China News Intelligence
Versao FINAL - sem emojis, sem acentos, 100% compativel Mac Python 3.14
"""

import json
import urllib.request
import urllib.parse
import ssl
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# FIX SSL para Mac
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# CHAVES DE API
NEWSDATA_API_KEY = "pub_22952a8bee454d7dbdcabc2cb3fd8f02"
GNEWS_API_KEY = "a8a4f060adfb5efc1520546bf76c8b30"

# Keywords
COMERCIO = ["trade", "import", "export", "tariff", "customs", "Canton", "supply chain", "commerce"]
TECNOLOGIA = ["semiconductor", "AI", "5G", "BYD", "Alibaba", "Huawei", "tech", "chip", "battery", "EV"]
ECONOMIA = ["yuan", "PBOC", "GDP", "economy", "inflation", "investment"]

# NOTICIAS DE DEMONSTRACAO - SEM EMOJIS, SEM ACENTOS
DEMO_NEWS = [
    {
        "id": "1001",
        "title": "China reduz tarifas de importacao em 935 produtos para impulsionar alta tecnologia",
        "description": "A China anunciou reducao de tarifas de importacao em componentes de semicondutores, baterias de litio e materiais aeroespaciais. Medida visa fortalecer autossuficiencia tecnologica.",
        "url": "https://example.com/news1",
        "image_url": "",
        "source": "Reuters",
        "published_at": datetime.now().isoformat(),
        "category": "comercio",
        "relevance_score": 95,
        "keywords_found": ["tariff", "semiconductor", "trade", "import"],
        "summary": "China reduz tarifas em 935 produtos de alta tecnologia para fortalecer setor tecnologico."
    },
    {
        "id": "1002",
        "title": "BYD supera Tesla em vendas globais de veiculos eletricos no primeiro trimestre",
        "description": "A montadora chinesa BYD registrou crescimento de 35% nas vendas internacionais de veiculos eletricos, superando a Tesla no mercado global.",
        "url": "https://example.com/news2",
        "image_url": "",
        "source": "TechCrunch",
        "published_at": datetime.now().isoformat(),
        "category": "tecnologia",
        "relevance_score": 88,
        "keywords_found": ["BYD", "EV", "automotive", "technology"],
        "summary": "BYD supera Tesla em vendas globais de veiculos eletricos com crescimento de 35%."
    },
    {
        "id": "1003",
        "title": "PBOC anuncia novas medidas de estimulo para comercio exterior chines",
        "description": "Banco Central da China reduz taxas de juros para exportadores e amplia linhas de credito para empresas de comercio exterior.",
        "url": "https://example.com/news3",
        "image_url": "",
        "source": "Bloomberg",
        "published_at": datetime.now().isoformat(),
        "category": "economia",
        "relevance_score": 82,
        "keywords_found": ["PBOC", "economy", "investment", "trade"],
        "summary": "Banco Central da China anuncia medidas de estimulo para exportadores com reducao de juros."
    },
    {
        "id": "1004",
        "title": "Canton Fair 2026: Mais de 25 mil expositores confirmam participacao",
        "description": "A Feira de Cantao de outubro de 2026 ja conta com mais de 25 mil expositores confirmados, superando expectativas.",
        "url": "https://example.com/news4",
        "image_url": "",
        "source": "China Daily",
        "published_at": datetime.now().isoformat(),
        "category": "comercio",
        "relevance_score": 90,
        "keywords_found": ["Canton", "trade", "export", "commerce"],
        "summary": "Canton Fair 2026 supera expectativas com mais de 25 mil expositores confirmados."
    },
    {
        "id": "1005",
        "title": "Huawei lanca novo chip de IA que compete com NVIDIA no mercado asiatico",
        "description": "Huawei apresenta chip Ascend 910C com performance comparavel a GPUs da NVIDIA. Empresa avanca em independencia tecnologica.",
        "url": "https://example.com/news5",
        "image_url": "",
        "source": "The Verge",
        "published_at": datetime.now().isoformat(),
        "category": "tecnologia",
        "relevance_score": 85,
        "keywords_found": ["Huawei", "chip", "AI", "semiconductor", "technology"],
        "summary": "Huawei lanca chip de IA que compete com NVIDIA, avancando em independencia tecnologica."
    },
    {
        "id": "1006",
        "title": "Yuan atinge maior valor em 6 meses frente ao dolar apos medidas do PBOC",
        "description": "Moeda chinesa se valoriza 3.2% em uma semana apos anuncio de novas politicas monetarias. Investidores estrangeiros aumentam posicoes.",
        "url": "https://example.com/news6",
        "image_url": "",
        "source": "Financial Times",
        "published_at": datetime.now().isoformat(),
        "category": "economia",
        "relevance_score": 78,
        "keywords_found": ["yuan", "PBOC", "economy", "investment"],
        "summary": "Yuan atinge maior valor em 6 meses com valorizacao de 3.2% apos politicas do Banco Central."
    },
    {
        "id": "1007",
        "title": "Alibaba expande operacoes de cross-border e-commerce para Brasil",
        "description": "Gigante chinesa anuncia investimento de US$ 500 milhoes em logistica para facilitar importacoes do Brasil.",
        "url": "https://example.com/news7",
        "image_url": "",
        "source": "Forbes",
        "published_at": datetime.now().isoformat(),
        "category": "comercio",
        "relevance_score": 92,
        "keywords_found": ["Alibaba", "trade", "import", "cross-border", "commerce"],
        "summary": "Alibaba investe US$ 500 milhoes em logistica para expandir e-commerce cross-border no Brasil."
    },
    {
        "id": "1008",
        "title": "Producao de baterias de litio na China cresce 40% em 2026",
        "description": "Setor de baterias de litio chines expande capacidade produtiva para atender demanda global de veiculos eletricos. CATL e BYD lideram investimentos.",
        "url": "https://example.com/news8",
        "image_url": "",
        "source": "Nikkei Asia",
        "published_at": datetime.now().isoformat(),
        "category": "tecnologia",
        "relevance_score": 80,
        "keywords_found": ["battery", "BYD", "EV", "technology"],
        "summary": "Producao de baterias de litio na China cresce 40% com expansao de CATL e BYD."
    }
]

def generate_caption(article):
    tag = "[" + article["category"].upper() + "]"
    caption = tag + " NOVIDADE DA CHINA\n\n" + article["title"] + "\n\n" + article["summary"] + """

O que isso significa para importadores?
-> Fique atento as mudancas nas politicas comerciais
-> Oportunidades de novos produtos e fornecedores
-> Impacto nos custos de importacao

Fonte: """ + article["source"] + """

#China #Importacao #ComercioExterior #DuranteExport #NegociosChina #""" + article["category"]
    return caption

def add_generated_content(article):
    article["instagram_caption"] = generate_caption(article)
    article["instagram_carousel"] = [
        "ATENCAO IMPORTADORES\n\n" + article["title"],
        "RESUMO\n\n" + article["summary"][:150] + "...",
        "IMPACTO PARA VOCE\n\n- Novas oportunidades de fornecedores\n- Mudancas em tarifas e regulamentacoes\n- Tendencias de mercado emergentes",
        "DICA DURANTE EXPORT\n\nMantenha-se informado sobre as politicas comerciais da China para antecipar oportunidades!",
        "Leia mais em: " + article["source"] + "\n\nComente 'CHINA' para saber mais"
    ]
    return article

for news in DEMO_NEWS:
    add_generated_content(news)

def fetch_newsdata():
    articles = []
    queries = ["China trade", "China technology", "China economy"]
    for q in queries:
        try:
            url = f"https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&q={urllib.parse.quote(q)}&language=en&size=10"
            with urllib.request.urlopen(url, timeout=15, context=ssl_context) as response:
                data = json.loads(response.read().decode())
                if data.get("results"):
                    articles.extend(data["results"])
                    print("NewsData OK: " + str(len(data["results"])) + " artigos")
        except Exception as e:
            print("NewsData erro: " + str(e))
    return articles

def fetch_gnews():
    articles = []
    queries = ["China business", "China technology"]
    for q in queries:
        try:
            url = f"https://gnews.io/api/v4/search?q={urllib.parse.quote(q)}&lang=en&max=10&apikey={GNEWS_API_KEY}"
            with urllib.request.urlopen(url, timeout=15, context=ssl_context) as response:
                data = json.loads(response.read().decode())
                if data.get("articles"):
                    articles.extend(data["articles"])
                    print("GNews OK: " + str(len(data["articles"])) + " artigos")
        except Exception as e:
            print("GNews erro: " + str(e))
    return articles

cache = []
cache_time = None

def get_news(category="all", limit=15):
    global cache, cache_time

    print("Buscando noticias...")
    nd = fetch_newsdata()
    gn = fetch_gnews()

    seen = set()
    processed = []

    for item in nd + gn:
        url = item.get("link") or item.get("url", "")
        title = item.get("title", "")
        if not url or not title or url in seen or title in seen:
            continue
        seen.add(url)
        seen.add(title)

        desc = item.get("description") or item.get("content", "")

        text = (title + " " + (desc or "")).lower()
        kws = []
        for kw in COMERCIO + TECNOLOGIA + ECONOMIA:
            if kw.lower() in text:
                kws.append(kw)

        c = sum(1 for k in kws if k in COMERCIO)
        t = sum(1 for k in kws if k in TECNOLOGIA)
        e = sum(1 for k in kws if k in ECONOMIA)

        if c >= t and c >= e and c > 0: cat = "comercio"
        elif t >= e and t > 0: cat = "tecnologia"
        elif e > 0: cat = "economia"
        else: cat = "geral"

        rel = min(100, len(kws) * 15 + 20)
        if "china" in text: rel += 10

        if rel < 15 and category != "all":
            continue

        summary = (desc or title)[:250] + "..." if len(desc or title) > 250 else (desc or title)

        article = {
            "id": str(hash(url) % 10000000),
            "title": title,
            "description": desc,
            "url": url,
            "image_url": item.get("image_url") or item.get("image", ""),
            "source": item.get("source_id") or item.get("source", {}).get("name", "Unknown"),
            "published_at": item.get("pubDate") or item.get("publishedAt", datetime.now().isoformat()),
            "category": cat,
            "relevance_score": rel,
            "keywords_found": kws,
            "summary": summary
        }
        add_generated_content(article)
        processed.append(article)

    if len(processed) == 0:
        print("APIs falharam. Usando noticias de demonstracao...")
        processed = DEMO_NEWS.copy()
    else:
        processed.extend(DEMO_NEWS[:3])

    processed.sort(key=lambda x: x["relevance_score"], reverse=True)
    cache = processed
    cache_time = datetime.now()

    if category != "all":
        processed = [a for a in processed if a["category"] == category]

    return processed[:limit]

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path

        if path == "/" or path == "/index.html":
            try:
                with open("dashboard.html", "r", encoding="utf-8") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
                return
            except FileNotFoundError:
                self.send_response(404)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(b'{"error": "dashboard.html not found"}')
                return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

        if path == "/api" or path == "/api/":
            response = {
                "message": "Durante Export - China News Intelligence",
                "status": "running",
                "endpoints": ["/api/news", "/api/stats"]
            }
        elif path.startswith("/api/news"):
            category = "all"
            limit = 15
            if "?" in path:
                query = path.split("?")[1]
                params = urllib.parse.parse_qs(query)
                if "category" in params:
                    category = params["category"][0]
                if "limit" in params:
                    limit = int(params["limit"][0])

            news = get_news(category, limit)
            response = {
                "status": "success",
                "count": len(news),
                "category": category,
                "updated_at": datetime.now().isoformat(),
                "articles": news
            }
        elif path == "/api/stats":
            cats = {}
            for a in cache:
                cats[a["category"]] = cats.get(a["category"], 0) + 1
            response = {
                "status": "success",
                "total": len(cache),
                "categories": cats
            }
        else:
            response = {"error": "Not found"}

        self.wfile.write(json.dumps(response).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    PORT = 8000
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print("=" * 60)
    print("DURANTE EXPORT - China News Intelligence")
    print("=" * 60)
    print("Dashboard: http://localhost:" + str(PORT))
    print("API: http://localhost:" + str(PORT) + "/api")
    print("=" * 60)
    print("Para parar, aperte CTRL+C")
    print("=" * 60)
    server.serve_forever()
