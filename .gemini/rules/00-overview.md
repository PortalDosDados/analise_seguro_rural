# 00 - Visão Geral do Projeto

## Domínio e Escopo
- `OBSERVADO` `[README.md]`: Análise do **PSR** (Programa de Subvenção ao Prêmio do Seguro Rural - MAPA), dados públicos SISSER (2006–2025).
- `OBSERVADO` `[download_csv.py]`: Fonte oficial `dados.agricultura.gov.br` (3 CSVs: `2006-2015`, `2016-2024`, `2025`) consolidados em `data/seguro_rural_total.csv`.
- `OBSERVADO` `[database.py]`: Banco alvo PostgreSQL (`db_seguro_rural` local via `.env`).
- `DIRETRIZ` (confirmado): Consumidor final **Power BI** (camada `gold` do PostgreSQL).

## Stack e Versões
- `OBSERVADO` `[README.md]`: Python 3.11+ (local: Python 3.12.10).
- `OBSERVADO` `[requirements.txt]`: `pandas==2.3.3`, `requests==2.32.5`, `SQLAlchemy==2.0.36`, `psycopg2-binary==2.9.10`, `python-dotenv==1.0.1`, `ruff==0.17.6`, `pytest==9.2.0`.
- `OBSERVADO` `[pyproject.toml]`: Configuração de `ruff` (`py312`, `E/F/I/W`) e `pytest` (`testpaths = ["tests"]`).

## Comandos Comprovados
- Instalar deps: `pip install -r requirements.txt` `[README.md]`
- Extrair/consolidar CSVs: `python download_csv.py` `[README.md]`
- Testar conexão PostgreSQL: `python database.py` `[database.py]`
- Estruturar schemas Medalhão: `python setup_db.py` `[setup_db.py]`
- Carregar camada bronze: `python load_bronze.py` `[load_bronze.py]`
- Carregar camada silver: `python load_silver.py` `[load_silver.py]`
- Lint Python: `ruff check .` `[pyproject.toml]`
- Testes unitários: `pytest` `[pyproject.toml]`
