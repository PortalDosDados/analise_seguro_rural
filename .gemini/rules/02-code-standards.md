# 02 - Padrões de Código (Python e SQL)

## Python
- `OBSERVADO` `[database.py]`: Funções pequenas com docstrings, type hints (`-> Engine`, `-> bool`), validação explícita de configs (`_load_db_config`) e `URL.create` para conexão SQLAlchemy 2.0.
- `OBSERVADO` `[download_csv.py]`: Sem type hints, sem retry/timeout HTTP e com `on_bad_lines='skip'` silencioso.
- `DIRETRIZ`: Seguir estilo de `[database.py]` (type hints, docstrings concisas, tratamento explícito de erros).
- `DIRETRIZ`: `PREFIRA` leitura em `chunks` para CSVs grandes (`data/seguro_rural_total.csv` ~516 MB) para evitar estouro de RAM.
- `NUNCA` usar caminhos absolutos locais (ex.: `C:/Users/...`) no código; `SEMPRE` usar caminhos relativos à raiz ou `pathlib.Path`.
- `NUNCA` duplicar lógica de conexão; `SEMPRE` importar `get_engine()` de `[database.py]`.

## Transformação CSV → PostgreSQL (`OBSERVADO` no schema)
- `SEMPRE` mapear colunas do CSV para snake_case do banco (`NivelDeCobertura` → `nivel_de_cobertura`, `VALOR_INDENIZAÇÃO` → `valor_indenizacao`).
- `SEMPRE` converter `'-'` para `NULL` antes de tipar colunas numéricas/data.
- `SEMPRE` normalizar vírgula decimal (`,` → `.`) em campos `NUMERIC` (ex.: `pe_taxa`, `vl_subvencao_federal`).
- `SEMPRE` parsear datas no padrão brasileiro `%d/%m/%Y`.

## SQL
- `DIRETRIZ`: `PREFIRA` CTEs nomeadas, palavras-chave em MAIÚSCULO, identificadores em `snake_case`.
- `NUNCA` usar `SELECT *` na camada `gold`.
- `SEMPRE` garantir idempotência nas cargas (ex.: `ON CONFLICT (id_proposta) DO UPDATE` ou staging + merge).
