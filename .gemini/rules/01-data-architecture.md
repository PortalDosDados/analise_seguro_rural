# 01 - Arquitetura de Dados (Modelo Medalhão)

## Estrutura Atual vs. Alvo
- `OBSERVADO` `[download_csv.py]`: Extração salva CSVs brutos e consolidado em `data/` (ignorado no `[.gitignore]`).
- `OBSERVADO` `[database.py]`: Conexão única com PostgreSQL `db_seguro_rural` (apenas ambiente local de desenvolvimento via `.env`).
- `DIRETRIZ` (confirmado): Estruturar `db_seguro_rural` em 3 schemas (**Modelo Medalhão**):
  - `bronze`: dados brutos (`TEXT`), espelho fiel dos CSVs + metadados (`arquivo_origem`, `dt_ingestao`).
  - `silver`: dados limpos, tipados (`DATE`, `NUMERIC`, `BIGINT`, `CHAR(2)`), deduplicados, grão **1 linha por `id_proposta`** (`PRIMARY KEY`).
  - `gold`: tabelas/views agregadas para consumo analítico (ex.: por ano/UF, cultura, evento).
- `DIRETRIZ` (confirmado): Remover `public.tb_seguro_rural` (vazia) após criar os 3 schemas.

## Regras de Dependência e Linhagem
- **Linhagem:** Fontes SISSER (`data/*.csv`) → `bronze` → `silver` → `gold`.
- `NUNCA` fazer `gold` ler diretamente de `bronze` ou `data/*.csv` pulando `silver`.
- `NUNCA` manter tabelas analíticas ou de staging no schema `public`.
- `SEMPRE` usar nomes qualificados com schema (`bronze.*`, `silver.*`, `gold.*`).
- `NUNCA` assumir separação `dev`/`prod` sem criação explícita de novos alvos; atualmente há apenas banco local `[.env]`.
