# 🌾 Análise de Seguro Rural (PSR - Brasil)

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18%2B-blue?style=for-the-badge&logo=postgresql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?style=for-the-badge&logo=powerbi&logoColor=black)

## 👋 Sobre o Projeto

Projeto de Engenharia e Análise de Dados sobre o **Programa de Subvenção ao Prêmio do Seguro Rural (PSR)**, gerido pelo Ministério da Agricultura e Pecuária (MAPA), com visualização final no **Power BI**.

Os dados são públicos e originários do **SISSER** (Sistema de Subvenção Econômica ao Prêmio do Seguro Rural):
- **Fonte Oficial:** [Dados Abertos - Agricultura](https://dados.agricultura.gov.br/dataset/sisser3)

---

## 🏗️ Arquitetura (Modelo Medalhão)

O banco PostgreSQL (`db_seguro_rural`) segue a arquitetura em 3 schemas:
- **`bronze`**: dados brutos (`TEXT`), espelho fiel dos CSVs originais.
- **`silver`**: dados limpos, tipados, deduplicados (`1` linha por `id_proposta`) e com colunas PII (`nm_segurado`, `nr_documento_segurado`) omitidas/mascaradas.
- **`gold`**: tabelas e views analíticas prontas para consumo no **Power BI**.

---

## 📁 Estrutura Atual

```text
analise_seguro_rural/
├── .agents/          # Isolamento de workspace (plugins/skills)
├── .gemini/rules/    # Diretrizes modulares de engenharia e governança
├── tests/            # Testes unitários (pytest)
├── .gitignore
├── GEMINI.md
├── pyproject.toml    # Configuração do ruff e pytest
├── README.md
├── requirements.txt
├── download_csv.py   # Extração e consolidação dos CSVs do PSR (2006–2025)
├── database.py       # Conexão SQLAlchemy com PostgreSQL via .env
├── setup_db.py       # Criação dos schemas bronze/silver/gold e tabelas iniciais
├── load_bronze.py    # Carga bruta dos CSVs para bronze.psr_raw via COPY
└── load_silver.py    # Transformação ELT idempotente bronze -> silver
```

---

## 🚀 Como Executar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Baixar e consolidar os dados

```bash
python download_csv.py
```

### 3. Testar conexão e estruturar o banco (Medalhão)

Configure o `.env` (`DB_USER`, `DB_PASS`, `DB_HOST`, `DB_PORT`, `DB_NAME`) e execute:

```bash
python database.py
python setup_db.py
python load_bronze.py
python load_silver.py
```

### 4. Lint e Testes

```bash
ruff check .
pytest
```
