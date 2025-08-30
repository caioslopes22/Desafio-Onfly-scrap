
# PokeAPI ETL Pipeline (Python + pandas + Docker)

Este projeto implementa um pipeline completo de **extração**, **transformação** e **relatório** usando a **PokeAPI** como fonte de dados.

## O que o pipeline faz

1. **Extrai** 100 Pokémon (`/pokemon?limit=100&offset=0`) e consulta detalhes individuais (`/pokemon/{id}`).
2. Constrói um `DataFrame` com as colunas: `ID`, `Nome`, `Experiência Base`, `Tipos`, `HP`, `Ataque`, `Defesa`.
3. **Transforma** os dados:
   - Adiciona a coluna **Categoria**: `Fraco` (<50), `Médio` (50–100), `Forte` (>100).
   - **Contagem por tipo** de Pokémon.
   - **Médias de HP, Ataque e Defesa por tipo**.
   - **Top 5 por experiência base**.
4. **Gera e exporta relatórios**:
   - CSVs: `pokemon_por_tipo.csv`, `media_stats_por_tipo.csv`, `top5_experiencia.csv`, `pokemon_dataset.csv`.
   - Gráfico PNG: `distribuicao_por_tipo.png`.

## Requisitos

- Docker (recomendado) ou Python 3.11+ com `pip`.
- Internet para acessar a PokeAPI.

## Rodando com Docker (recomendado)

```bash
# 1) Build
docker build -t pokeapi-pipeline .

# 2) Run (salvando saídas em ./outputs na máquina local)
docker run --rm -v "$(pwd)/outputs:/app/outputs" pokeapi-pipeline

# Opções
# - Limitar/offset e delay entre requests (para evitar rate limit)
docker run --rm -v "$(pwd)/outputs:/app/outputs" pokeapi-pipeline \
  python /app/src/poke_pipeline/main.py --limit 100 --offset 0 --output-dir /app/outputs --request-delay 0.05
```

> **Nota:** Você pode customizar a base da API com a variável de ambiente `POKEAPI_BASE` (default: `https://pokeapi.co/api/v2`).

## Rodando localmente (sem Docker)

```bash
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt

# Executar
export PYTHONPATH=src
python src/poke_pipeline/main.py --limit 100 --offset 0 --output-dir outputs --request-delay 0.05
```

## Estrutura do projeto

```text
.
├── Dockerfile
├── README.md
├── requirements.txt
├── run.py
├── src/
│   └── poke_pipeline/
│       ├── __init__.py
│       ├── extract.py
│       ├── main.py
│       ├── report.py
│       ├── transform.py
│       └── utils.py
└── outputs/            # (criado em runtime)
```

## Logs e Tratamento de Erros

- Uso da biblioteca `logging` com saída padronizada para `stdout`.
- `requests` configurado com **retries e backoff** para respostas 429/5xx.
- Atraso configurável entre requisições (`--request-delay`) para evitar rate limit.
- Registros detalhados de progresso e de eventuais falhas de consulta por Pokémon.

## Observações de Design

- **Modularidade:** extração, transformação e relatório em módulos separados.
- **PEP 8:** nomes claros e funções pequenas (fácil teste e manutenção).
- **Eficiência:** uma chamada inicial para a lista e 100 chamadas para detalhes (mínimo necessário para o escopo). `requests.Session` + retries aproveitam conexões persistentes.
- **Visualização:** gráfico de barras com `matplotlib` (labels rotacionados, `tight_layout`).

## Como validar as saídas

Após rodar o pipeline, procure os arquivos em `outputs/`:
- `pokemon_dataset.csv`
- `pokemon_por_tipo.csv`
- `media_stats_por_tipo.csv`
- `top5_experiencia.csv`
- `distribuicao_por_tipo.png`

## Licença

MIT
