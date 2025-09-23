import psycopg2
import pandas as pd
import os

# ----------------------------
# 1. Carregar o CSV
# ----------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "cvm_detalhes.csv")

df = pd.read_csv(csv_path)

# Função para limpar números (remover separador milhar e trocar vírgula por ponto)
def to_numeric(col):
    return (
        col.astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )

# Converter colunas numéricas
num_cols = ["valorTotalInicial", "valorTotalFinal", "quantidadeAtivos", "valorNominal", "valorTotalLote"]
for col in num_cols:
    df[col] = to_numeric(df[col])
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Converter datas
date_cols = ["dataOferta", "dataEmissao", "dataVencimento"]
for col in date_cols:
    df[col] = pd.to_datetime(df[col], format="%d/%m/%Y", errors="coerce")

# Substituir NaN por None
df = df.where(pd.notnull(df), None)

# ----------------------------
# 2. Conectar ao Supabase
# ----------------------------
conn = psycopg2.connect(
    "postgresql://postgres:hswGzsMSUB5H93QQ@db.bruzpbiokafrbsksmiod.supabase.co:5432/postgres"
)
cur = conn.cursor()

# ----------------------------
# 3. Inserir dados
# ----------------------------
for i, row in df.iterrows():
    values = {
        "numeroProcesso": row["numeroProcesso"],
        "numeroRegistro": row["numeroRegistro"],
        "nomeValorMobiliario": row["nomeValorMobiliario"],
        "valorTotalInicial": row["valorTotalInicial"],
        "valorTotalFinal": row["valorTotalFinal"],
        "dataOferta": row["dataOferta"].date() if pd.notnull(row["dataOferta"]) else None,
        "nomeTipoRequerimento": row["nomeTipoRequerimento"],
        "status": row["status"],
        "serie_nome": row["serie_nome"],
        "quantidadeAtivos": None if pd.isna(row["quantidadeAtivos"]) else row["quantidadeAtivos"],
        "valorNominal": None if pd.isna(row["valorNominal"]) else row["valorNominal"],
        "valorTotalLote": None if pd.isna(row["valorTotalLote"]) else row["valorTotalLote"],
        "taxaRemuneracao": row["taxaRemuneracao"],
        "dataEmissao": row["dataEmissao"].date() if pd.notnull(row["dataEmissao"]) else None,
        "dataVencimento": row["dataVencimento"].date() if pd.notnull(row["dataVencimento"]) else None,
        "especie": row["especie"],
        "avaliacaoRisco": row["avaliacaoRisco"],
        "remuneracaoFinal": row["remuneracaoFinal"],
        "amortizacao": row["amortizacao"],
        "incentivado": row["incentivado"],
        "infraLei14801": row["infraLei14801"],
        "resgateAntecipado": row["resgateAntecipado"],
    }

    try:
        cur.execute(
            """
            INSERT INTO cvm_detalhes (
                numeroProcesso, numeroRegistro, nomeValorMobiliario,
                valorTotalInicial, valorTotalFinal, dataOferta,
                nomeTipoRequerimento, status, serie_nome,
                quantidadeAtivos, valorNominal, valorTotalLote,
                taxaRemuneracao, dataEmissao, dataVencimento,
                especie, avaliacaoRisco, remuneracaoFinal,
                amortizacao, incentivado, infraLei14801, resgateAntecipado
            ) VALUES (
                %(numeroProcesso)s, %(numeroRegistro)s, %(nomeValorMobiliario)s,
                %(valorTotalInicial)s, %(valorTotalFinal)s, %(dataOferta)s,
                %(nomeTipoRequerimento)s, %(status)s, %(serie_nome)s,
                %(quantidadeAtivos)s, %(valorNominal)s, %(valorTotalLote)s,
                %(taxaRemuneracao)s, %(dataEmissao)s, %(dataVencimento)s,
                %(especie)s, %(avaliacaoRisco)s, %(remuneracaoFinal)s,
                %(amortizacao)s, %(incentivado)s, %(infraLei14801)s, %(resgateAntecipado)s
            )
            """,
            values,
        )
        print(f"✅ Linha {i} inserida com sucesso")
    except Exception as e:
        print(f"❌ Erro na linha {i}")
        print("Valores:", values)
        print("Erro:", e)
        raise


# ----------------------------
# 4. Finalizar
# ----------------------------
conn.commit()
cur.close()
conn.close()

print("✅ Dados importados com sucesso para cvm_detalhes!")
