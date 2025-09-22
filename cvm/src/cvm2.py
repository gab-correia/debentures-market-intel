import os
import requests
import pandas as pd

# Pasta onde vamos salvar o resultado
OUTPUT_DIR = os.path.join("data", "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# URL da API de detalhe
URL_DETALHE = "https://web.cvm.gov.br/sre-publico-cvm/rest/sitePublico/pesquisar/requerimento/{}"

def fetch_requerimento(id_requerimento: int):
    """Busca os detalhes da oferta na CVM"""
    resp = requests.get(URL_DETALHE.format(id_requerimento), timeout=60)
    resp.raise_for_status()
    return resp.json()

def extract_info(data: dict):
    """Extrai os campos relevantes do JSON detalhado"""
    info = data.get("informacoesGerais", {})
    grupos = data.get("grupos", [])

    rows = []
    for grupo in grupos:
        for serie in grupo.get("series", []):
            lote_final = serie.get("loteFinal", {})
            lote_inicial = serie.get("loteInicial", {})

            campos = {c["campoNome"]: c.get("campoValor") for c in lote_final.get("camposCadastrados", [])}

            row = {
                # Infos gerais
                "numeroProcesso": info.get("numeroProcesso"),
                "numeroRegistro": serie.get("numeroRegistro", info.get("numeroRegistro")),
                "nomeValorMobiliario": info.get("nomeValorMobiliario"),
                "valorTotalInicial": info.get("valorTotalInicial"),
                "valorTotalFinal": info.get("valorTotalFinal"),
                "dataOferta": info.get("data"),
                "nomeTipoRequerimento": info.get("nomeTipoRequerimento"),
                "status": info.get("status"),

                # Infos da série
                "serie_nome": lote_final.get("valorMobiliario", lote_inicial.get("valorMobiliario")),
                "quantidadeAtivos": lote_final.get("loteBase", {}).get("quantidadeAtivos"),
                "valorNominal": lote_final.get("loteBase", {}).get("valorNominal"),
                "valorTotalLote": lote_final.get("valorTotalLote"),
                "taxaRemuneracao": lote_final.get("taxaRemuneracao"),

                # Campos cadastrados principais
                "dataEmissao": campos.get("Data de emissão"),
                "dataVencimento": campos.get("Data de vencimento"),
                "especie": campos.get("Espécie"),
                "avaliacaoRisco": campos.get("Avaliação de risco"),
                "remuneracaoFinal": campos.get("Informações sobre remuneração final (pós bookbuilding)"),
                "amortizacao": campos.get("Informações sobre amortização"),
                "incentivado": campos.get("Título incentivado - Lei 12.431/11"),
                "infraLei14801": campos.get("Debêntures de infraestrutura - Lei 14.801/24"),
                "resgateAntecipado": campos.get("Possibilidade de resgate antecipado"),
            }
            rows.append(row)

    # Caso não haja séries
    if not rows:
        rows.append({
            "numeroProcesso": info.get("numeroProcesso"),
            "numeroRegistro": info.get("numeroRegistro"),
            "nomeValorMobiliario": info.get("nomeValorMobiliario"),
            "valorTotalInicial": info.get("valorTotalInicial"),
            "valorTotalFinal": info.get("valorTotalFinal"),
            "dataOferta": info.get("data"),
            "nomeTipoRequerimento": info.get("nomeTipoRequerimento"),
            "status": info.get("status"),
            "serie_nome": None,
            "quantidadeAtivos": None,
            "valorNominal": None,
            "valorTotalLote": None,
            "taxaRemuneracao": None,
            "dataEmissao": None,
            "dataVencimento": None,
            "especie": None,
            "avaliacaoRisco": None,
            "remuneracaoFinal": None,
            "amortizacao": None,
            "incentivado": None,
            "infraLei14801": None,
            "resgateAntecipado": None,
        })
    return rows
