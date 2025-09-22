import psycopg2
import pandas as pd
import os

# ----------------------------
# 1. Carregar o CSV
# ----------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "dados_cvm_filtrando_status.csv")

df = pd.read_csv(csv_path)

# Corrigir coluna de valores (trocar vírgula por ponto e remover separador de milhar)
df["valorTotalEmReais"] = (
    df["valorTotalEmReais"]
    .astype(str)
    .str.replace(".", "", regex=False)   # remove separador de milhar
    .str.replace(",", ".", regex=False)  # troca vírgula por ponto
)

# Converter para float (se der erro vira None)
df["valorTotalEmReais"] = pd.to_numeric(df["valorTotalEmReais"], errors="coerce")

# Converter coluna data para datetime
df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y", errors="coerce")

# Substituir NaN por None para Postgres aceitar
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
    try:
        cur.execute(
            """
            INSERT INTO ofertas_cvm (
                idRequerimento, totalRegistros, numeroProtocolo, numeroProcesso,
                numeroRegistro, nomeValorMobiliario, tipoDeOferta, statusDaOferta,
                nomeEmissor, cnpjEmissor, nomeCoordenadorLider, cnpjCoordenadorLider,
                valorTotalEmReais, data, nomeTipoRequerimento,
                vasoComunicante, possuiBook, registroAutomatico
            )
            VALUES (
                %(idRequerimento)s, %(totalRegistros)s, %(numeroProtocolo)s, %(numeroProcesso)s,
                %(numeroRegistro)s, %(nomeValorMobiliario)s, %(tipoDeOferta)s, %(statusDaOferta)s,
                %(nomeEmissor)s, %(cnpjEmissor)s, %(nomeCoordenadorLider)s, %(cnpjCoordenadorLider)s,
                %(valorTotalEmReais)s, %(data)s, %(nomeTipoRequerimento)s,
                %(vasoComunicante)s, %(possuiBook)s, %(registroAutomatico)s
            );
            """,
            {
                "idRequerimento": row["idRequerimento"],
                "totalRegistros": row["totalRegistros"],
                "numeroProtocolo": row["numeroProtocolo"],
                "numeroProcesso": row["numeroProcesso"],
                "numeroRegistro": row["numeroRegistro"],
                "nomeValorMobiliario": row["nomeValorMobiliario"],
                "tipoDeOferta": row["tipoDeOferta"],
                "statusDaOferta": row["statusDaOferta"],
                "nomeEmissor": row["nomeEmissor"],
                "cnpjEmissor": row["cnpjEmissor"],
                "nomeCoordenadorLider": row["nomeCoordenadorLider"],
                "cnpjCoordenadorLider": row["cnpjCoordenadorLider"],
                "valorTotalEmReais": row["valorTotalEmReais"],
                "data": row["data"].date() if row["data"] else None,
                "nomeTipoRequerimento": row["nomeTipoRequerimento"],
                "vasoComunicante": row["vasoComunicante"],
                "possuiBook": row["possuiBook"],
                "registroAutomatico": row["registroAutomatico"],
            }
        )

        print(f"✅ Linha {i} inserida com sucesso")
    except Exception as e:
        print(f"❌ Erro na linha {i}")
        raise

# ----------------------------
# 4. Finalizar
# ----------------------------
conn.commit()
cur.close()
conn.close()

print("✅ Dados importados com sucesso para ofertas_cvm!")
