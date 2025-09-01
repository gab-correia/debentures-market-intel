import os
import requests
import pandas as pd

URL = "https://web.cvm.gov.br/sre-publico-cvm/rest/sitePublico/pesquisar/detalhado"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://web.cvm.gov.br",
    "Referer": "https://web.cvm.gov.br/sre-publico-cvm/",
}

payload = {
    "periodoCriacaoProcesso": {"de": "01/09/2024", "ate": "01/09/2025"},
    "opa": False,
    "tipoOferta": "OFERTA_REGULAR",
    "modalidade": "TODAS",
    "direcaoOrdenacao": "DESC",
    "colunaOrdenacao": "data",
    "pagina": 1,       # primeira página
    "tamanhoPagina": 5
}

resp = requests.post(URL, json=payload, headers=HEADERS, timeout=60)
resp.raise_for_status()
data = resp.json()

registros = data.get("registros", [])

df = pd.DataFrame(registros)

# garante que a pasta data/raw exista
output_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "detalhado_primeira_pagina.csv")
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print("Arquivo salvo em:", os.path.abspath(output_path))
print("totalRegistros:", data.get("totalRegistros"))
print("registros coletados nesta página:", len(registros))
