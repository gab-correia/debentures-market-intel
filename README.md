# Debentures Market Intel

Este projeto tem como objetivo coletar, processar e analisar dados do mercado primário de debêntures no Brasil, utilizando técnicas de web scraping e agentes de inteligência artificial para buscas inteligentes na internet.

A estrutura do projeto foi desenvolvida de forma modular, permitindo a evolução desde a coleta de dados básicos até a construção de dashboards e relatórios analíticos.

## Objetivos

- Automatizar a coleta de dados de debêntures emitidas no mercado primário (CVM, ANBIMA, B3).
- Criar pipelines de tratamento e padronização dos dados.
- Desenvolver indicadores e métricas de crédito privado, como prazo, taxa, spread, rating e setor.
- Implementar agentes de inteligência artificial para buscar, resumir e enriquecer informações relevantes, como notícias, comunicados e documentos.
- Disponibilizar dashboards interativos para análise.

## Estrutura do Projeto

```
debentures-market-intel/
│── README.md               # Documentação do projeto
│── requirements.txt         # Lista de dependências
│── .gitignore               # Arquivos a serem ignorados no Git
│
├── data/                    # Armazenamento de dados
│   ├── raw/                 # Dados brutos coletados
│   ├── processed/           # Dados tratados
│   └── reports/             # Relatórios e saídas
│
├── notebooks/               # Jupyter notebooks para exploração
│
├── src/                     # Código-fonte
│   ├── scraping/            # Scripts de coleta de dados (CVM, ANBIMA, B3)
│   ├── agents/              # Agentes de IA (busca e resumo de informações)
│   ├── processing/          # Limpeza, transformação e armazenamento
│   └── visualization/       # Visualizações e dashboards
│
└── tests/                   # Testes unitários
```

## Tecnologias

- **Linguagem:** Python 3.x
- **Scraping:** requests, beautifulsoup4, scrapy, playwright
- **Processamento:** pandas, numpy
- **Inteligência Artificial/Agentes:** langchain, openai, serpapi (ou equivalente)
- **Visualização:** matplotlib, plotly, streamlit
- **Banco de dados (opcional):** sqlite3 ou postgresql

## Como Rodar o Projeto

1. Clone o repositório:

    ```bash
    git clone https://github.com/seuusuario/debentures-market-intel.git
    cd debentures-market-intel
    ```

2. Crie e ative um ambiente virtual:

    ```bash
    python -m venv venv
    .\venv\Scripts\activate   # Windows
    source venv/bin/activate  # Linux/Mac
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

4. Execute os notebooks ou scripts de scraping:

    ```bash
    jupyter notebook
    ```

## Próximos Passos

- Implementar o scraper da CVM para coleta de dados de ofertas públicas.
- Conectar o processo de scraping com pipelines de tratamento automático de dados.
- Desenvolver os primeiros indicadores de análise, como prazo médio, taxa média e emissões por setor.
- Construir um dashboard interativo utilizando Streamlit ou Plotly.
- Integrar agentes de inteligência artificial para enriquecer as análises.

