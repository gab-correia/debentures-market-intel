import os
import json
import requests

DATA_PATH = os.path.join("data", "raw", "cvm_jsons")

def fetch_requerimento(id_requerimento: int):
    url = f"https://web.cvm.gov.br/sre-publico-cvm/rest/sitePublico/pesquisar/requerimento/{id_requerimento}"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return response.json()

def save_json(data: dict, id_requerimento: int):
    os.makedirs(DATA_PATH, exist_ok=True)
    filepath = os.path.join(DATA_PATH, f"{id_requerimento}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"✅ JSON salvo em {filepath}")

if __name__ == "__main__":
    ids = [22032, 21838, 21842, 21841, 21863, 21069, 21567, 21972, 21984, 21899]

    for id_req in ids:
        try:
            data = fetch_requerimento(id_req)
            save_json(data, id_req)
        except Exception as e:
            print(f"⚠️ Erro ao processar {id_req}: {e}")
