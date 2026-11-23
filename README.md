# 🌾 Análise de Seguro Rural (PSR - Brasil)

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow?style=for-the-badge)

## 👋 Sobre o Projeto

Projeto de Engenharia de Dados e Análise de Dados sobre o **Programa de Subvenção ao Prêmio do Seguro Rural (PSR)**, gerido pelo Ministério da Agricultura e Pecuária (MAPA).

Os dados são públicos e originários do **SISSER** (Sistema de Subvenção Econômica ao Prêmio do Seguro Rural):
- **Fonte Oficial:** [Dados Abertos - Agricultura](https://dados.agricultura.gov.br/dataset/sisser3)

---

## 📁 Estrutura Atual

```text
analise_seguro_rural/
├── .gitignore
├── README.md
├── requirements.txt
└── download_csv.py   # Download e consolidação dos CSVs do PSR (2006–2025)
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

O script cria a pasta `data/` (ignorada pelo Git), baixa os arquivos anuais (`2006–2015`, `2016–2024` e `2025`) e gera o dataset consolidado em `data/seguro_rural_total.csv`.
