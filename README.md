# 🌾 Análise de Seguro Rural (PSR - Brasil)

Este projeto realiza a análise exploratória e modelagem de dados do **Programa de Subvenção ao Prêmio do Seguro Rural (PSR)**, gerido pelo Ministério da Agricultura, Pecuária e Abastecimento (MAPA).

O objetivo é extrair inteligência de mercado e avaliar riscos agrícolas utilizando Python e Data Science.

## 🎯 Objetivos do Projeto

- **Análise de Sinistralidade:** Identificar quais culturas e regiões apresentam maior risco.
- **Mapeamento Geográfico:** Visualizar a distribuição dos subsídios pelo Brasil.
- **Modelagem Financeira:** Analisar a relação entre o *Valor da Garantia* e o *Prêmio Líquido*.
- **Business Intelligence:** Fornecer insights para seguradoras (InsurTech) e produtores rurais (AgTech).

## 📊 Fonte dos Dados

Os dados são públicos e originários do **SISSER** (Sistema de Subvenção Econômica ao Prêmio do Seguro Rural).

- **Fonte Oficial:** [Dados Abertos - Agricultura](https://dados.agricultura.gov.br/dataset/sisser3)
- **Período Analisado:** 2006 a 2015 (Base histórica)

## 🗂 Dicionário de Dados

Com base na documentação oficial (`dicionariodedados-sisser.pdf`), as principais variáveis analisadas são:

### 📍 Localização

- **LATITUDE / LONGITUDE**: Coordenadas geográficas da propriedade rural.
- **UF / MUNICIPIO**: Estado e cidade da propriedade.

### 🚜 Produção

- **NM_CULTURA_GLOBAL**: A cultura ou atividade segurada (Ex: Soja, Milho, Trigo, Uva).
- **NM_CLASSIF_PRODUTO**: Classificação do tipo de seguro contratado.
- **AREA_TOTAL**: Área total segurada (em hectares).
- **ANIMAL**: Número de animais segurados (para pecuária).
- **PRODUTIVIDADE_ESTIMADA**: Expectativa de produção indicada na apólice.

### 💰 Valores Financeiros

- **VL_LIMITE_GARANTIA**: Valor total segurado (o valor da proteção).
- **VL_PREMIO_LIQUIDO**: Custo do seguro (sem taxas).
- **VL_SUBVENCAO_FEDERAL**: Valor pago pelo Governo Federal para ajudar o produtor.
- **PE_TAXA**: Percentual da taxa do prêmio sobre o valor segurado.

## 🛠 Tecnologias Utilizadas

- **Python 3.x**
- **Pandas:** Manipulação e limpeza de dados.
- **NumPy:** Cálculos matemáticos.
- **Matplotlib / Seaborn:** Visualização de dados.
- **Jupyter Notebooks:** Prototipagem e análise interativa.
