# 🌾 Análise de Seguro Rural (PSR - Brasil)

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python&logoColor=white)

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

## 🗄️ Modelagem do Banco de Dados

Para garantir a integridade e a precisão das análises financeiras e geográficas, optamos por não utilizar a inferência automática de tipos do Pandas (`to_sql` padrão). Em vez disso, definimos explicitamente o esquema (Schema) do banco de dados PostgreSQL.

O script `manual_sql.py` é responsável pela DDL (Data Definition Language), criando a tabela `tb_seguro_rural` com as seguintes características de robustez:

### 🛠️ Decisões de Arquitetura de Dados

- **Chave Primária (`PRIMARY KEY`):** A coluna `id_proposta` foi definida como identificador único, garantindo que não haja duplicidade de apólices na base.
- **Precisão Financeira (`NUMERIC`):** Para colunas monetárias (ex: `vl_premio_liquido`, `valor_indenizacao`), utilizamos `NUMERIC(18,2)` em vez de `FLOAT`. Isso evita erros de arredondamento de ponto flutuante, cruciais em cálculos financeiros.

- **Dados Geográficos:**
- Utilizamos `NUMERIC(15,10)` para `latitude` e `longitude` decimais, garantindo precisão máxima para plotagem em mapas.
- Mantivemos as colunas de coordenadas originais (graus/minutos/segundos) como `VARCHAR` para preservação do dado bruto (raw data).

- **Tipagem Temporal:** Conversão explícita de colunas de data para o tipo `DATE` (PostgreSQL), facilitando análises de séries temporais e coortes (ex: safras).

### 📝 Esquema da Tabela (`tb_seguro_rural`)

```sql
CREATE TABLE tb_seguro_rural (
    nm_razao_social           VARCHAR(255),
    cd_processo_susep         BIGINT,
    nr_proposta               VARCHAR(100),
    id_proposta               BIGINT PRIMARY KEY,
    dt_proposta               DATE,
    dt_inicio_vigencia        DATE,
    dt_fim_vigencia           DATE,
    nm_segurado               VARCHAR(255),
    nr_documento_segurado     VARCHAR(50),
    nm_municipio_propriedade  VARCHAR(255),
    sg_uf_propriedade         CHAR(2),
    latitude                  VARCHAR(50),
    nr_grau_lat               VARCHAR(10),
    nr_min_lat                VARCHAR(10),
    nr_seg_lat                VARCHAR(10),
    longitude                 VARCHAR(50),
    nr_grau_long              VARCHAR(10),
    nr_min_long               VARCHAR(10),
    nr_seg_long               VARCHAR(10),
    nr_decimal_latitude       NUMERIC(15, 10),
    nr_decimal_longitude      NUMERIC(15, 10),
    nm_classif_produto        VARCHAR(100),
    nm_cultura_global         VARCHAR(100),
    nr_area_total             NUMERIC(12, 4),
    nr_animal                 NUMERIC(10, 2),
    nr_produtividade_estimada NUMERIC(12, 2),
    nr_produtividade_segurada NUMERIC(12, 2),
    nivel_de_cobertura        NUMERIC(10, 2),
    vl_limite_garantia        NUMERIC(18, 2),
    vl_premio_liquido         NUMERIC(18, 2),
    pe_taxa                   NUMERIC(10, 4),
    vl_subvencao_federal      NUMERIC(18, 2),
    nr_apolice                VARCHAR(100),
    dt_apolice                DATE,
    ano_apolice               INTEGER,
    cd_geocmu                 VARCHAR(20),
    valor_indenizacao         NUMERIC(18, 2),
    evento_preponderante      VARCHAR(255)
);

