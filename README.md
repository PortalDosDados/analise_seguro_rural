# 🌾 Análise de Seguro Rural (PSR - Brasil)

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-blue?style=for-the-badge&logo=postgresql&logoColor=white)
![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow?style=for-the-badge)

## 👋 Sobre o Projeto

Neste projeto, desenvolvi uma solução de ponta a ponta (End-to-End) para a análise de dados do **Programa de Subvenção ao Prêmio do Seguro Rural (PSR)**, gerido pelo Ministério da Agricultura (MAPA).

Meu objetivo principal é extrair inteligência de mercado e avaliar riscos agrícolas aplicando técnicas de Engenharia de Dados e Data Science. Em vez de apenas visualizar dados, construí uma arquitetura robusta para ingerir, armazenar e analisar milhões de registros de apólices rurais.

## 🎯 Meus Objetivos

Com esta aplicação, busco responder a perguntas críticas do agronegócio:

- **Análise de Sinistralidade:** Quais culturas e regiões apresentam maior risco financeiro?
- **Inteligência Geográfica:** Onde estão concentrados os subsídios do governo?
- **Modelagem Financeira:** Qual a correlação real entre o valor garantido e o prêmio pago?
- **Insights de Negócio:** Fornecer dados acionáveis para seguradoras (InsurTechs) e produtores.

---

## 🏗️ Engenharia de Dados e Modelagem

Uma das decisões mais importantes deste projeto foi a arquitetura do banco de dados. Para garantir a integridade dos cálculos financeiros e a precisão das coordenadas geográficas, optei por **não utilizar a inferência automática de tipos do Pandas** (`to_sql` padrão), que frequentemente trata datas como texto e valores monetários como float impreciso.

Em vez disso, desenhei explicitamente o **Schema** do banco de dados PostgreSQL.

### 🛠️ Decisões de Arquitetura

O script `manual_sql.py` contém a DDL (Data Definition Language) que desenvolvi, garantindo:

1. **Integridade Única (`PRIMARY KEY`):** Defini a coluna `id_proposta` como chave primária, impedindo a duplicação de apólices na minha base analítica.

2. **Precisão Financeira (`NUMERIC`):** Para todas as colunas monetárias (como `vl_premio_liquido` e `valor_indenizacao`), utilizei `NUMERIC(18,2)`. Isso evita os erros clássicos de arredondamento de ponto flutuante (*floating point errors*) que ocorrem ao usar `FLOAT` ou `DOUBLE` em sistemas financeiros.

3. **Alta Precisão Geográfica:**
    - Utilizei `NUMERIC(15,10)` para `latitude` e `longitude` decimais, garantindo a precisão necessária para plotagem futura em mapas de calor.
    - Mantive as colunas de coordenadas originais (graus/minutos) como `VARCHAR` para preservação do dado bruto (*raw data*).

4. **Tipagem Temporal:** Forcei a conversão de colunas de data para o tipo `DATE` nativo do PostgreSQL, o que facilita queries de séries temporais (ex: análises por safra ou ano fiscal).

### 📝 O Schema da Tabela (`tb_seguro_rural`)

Abaixo, apresento a estrutura SQL que criei para suportar o volume de dados:

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
````

---

## 📊 Os Dados

Os dados utilizados são públicos e originários do **SISSER** (Sistema de Subvenção Econômica ao Prêmio do Seguro Rural).

- **Fonte Oficial:** [Dados Abertos - Agricultura](https://dados.agricultura.gov.br/dataset/sisser3)

### Dicionário de Variáveis

Baseado na documentação oficial, foquei nas seguintes variáveis para a modelagem:

| Categoria | Variáveis Principais | Descrição |
| :--- | :--- | :--- |
| **📍 Localização** | `LATITUDE`, `LONGITUDE`, `UF` | Coordenadas e estado da propriedade rural. |
| **🚜 Produção** | `NM_CULTURA_GLOBAL`, `AREA_TOTAL` | Tipo de cultura (ex: Soja, Milho) e tamanho da área em hectares. |
| **💰 Financeiro** | `VL_LIMITE_GARANTIA` | Valor total da proteção (seguro). |
| **📉 Custo** | `VL_PREMIO_LIQUIDO` | Custo do seguro sem taxas. |
| **🏛️ Governo** | `VL_SUBVENCAO_FEDERAL` | Valor subsidiado pelo governo. |

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.11+

- PostgreSQL instalado e rodando

- Arquivo `.env` configurado na raiz (veja abaixo)

### 1\. Configuração de Ambiente

Crie um arquivo `.env` na raiz do projeto para proteger suas credenciais:

```ini
DB_USER=seu_usuario
DB_PASS=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=db_seguro_rural
```

### 2\. Instalação das Dependências

```bash
pip install -r requirements.txt
```

### 3\. Criação do Banco de Dados

Execute o script de modelagem para criar a tabela com o schema otimizado:

```bash
python manual_sql.py
```

---

## 🛠 Tecnologias

- **Python:** Linguagem principal.
- **PostgreSQL:** Banco de dados relacional robusto.
- **SQLAlchemy:** ORM e gerenciamento de conexões.
- **Pandas:** Manipulação e limpeza de dados (ETL).
- **Matplotlib/Seaborn:** Visualização de dados.

<!-- end list -->
