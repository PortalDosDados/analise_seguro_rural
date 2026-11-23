from sqlalchemy import text
from sqlalchemy.engine import Engine

from database import get_engine

GOLD_BUILD_STATEMENTS: tuple[str, ...] = (
    # 1. Dimensão Calendário (2006-01-01 a 2025-12-31)
    """
    CREATE TABLE IF NOT EXISTS gold.dim_calendario (
        dt_referencia  DATE PRIMARY KEY,
        ano            INTEGER NOT NULL,
        semestre       SMALLINT NOT NULL,
        trimestre      SMALLINT NOT NULL,
        mes            SMALLINT NOT NULL,
        nome_mes       VARCHAR(20) NOT NULL,
        ano_mes        CHAR(7) NOT NULL
    );
    """,
    """
    INSERT INTO gold.dim_calendario (
        dt_referencia, ano, semestre, trimestre, mes, nome_mes, ano_mes
    )
    WITH datas AS (
        SELECT generate_series(
            DATE '2006-01-01',
            DATE '2025-12-31',
            INTERVAL '1 day'
        )::DATE AS dt_referencia
    )
    SELECT
        dt_referencia,
        EXTRACT(YEAR FROM dt_referencia)::INTEGER AS ano,
        CASE WHEN EXTRACT(MONTH FROM dt_referencia) <= 6 THEN 1 ELSE 2 END::SMALLINT
            AS semestre,
        EXTRACT(QUARTER FROM dt_referencia)::SMALLINT AS trimestre,
        EXTRACT(MONTH FROM dt_referencia)::SMALLINT AS mes,
        CASE EXTRACT(MONTH FROM dt_referencia)::INTEGER
            WHEN 1 THEN 'Janeiro'
            WHEN 2 THEN 'Fevereiro'
            WHEN 3 THEN 'Março'
            WHEN 4 THEN 'Abril'
            WHEN 5 THEN 'Maio'
            WHEN 6 THEN 'Junho'
            WHEN 7 THEN 'Julho'
            WHEN 8 THEN 'Agosto'
            WHEN 9 THEN 'Setembro'
            WHEN 10 THEN 'Outubro'
            WHEN 11 THEN 'Novembro'
            WHEN 12 THEN 'Dezembro'
        END AS nome_mes,
        TO_CHAR(dt_referencia, 'YYYY-MM')::CHAR(7) AS ano_mes
    FROM datas
    ON CONFLICT (dt_referencia) DO NOTHING;
    """,
    # 2. Dimensão Localidade
    """
    CREATE TABLE IF NOT EXISTS gold.dim_localidade (
        sk_localidade  BIGSERIAL PRIMARY KEY,
        cd_geocmu      VARCHAR(20) NOT NULL,
        nm_municipio   VARCHAR(255) NOT NULL,
        sg_uf          CHAR(2) NOT NULL,
        regiao         VARCHAR(20) NOT NULL,
        UNIQUE (cd_geocmu, nm_municipio, sg_uf)
    );
    """,
    """
    INSERT INTO gold.dim_localidade (cd_geocmu, nm_municipio, sg_uf, regiao)
    WITH base AS (
        SELECT DISTINCT
            COALESCE(cd_geocmu, 'N/I') AS cd_geocmu,
            COALESCE(nm_municipio_propriedade, 'Não Informado') AS nm_municipio,
            sg_uf_propriedade AS sg_uf
        FROM silver.psr_clean
    )
    SELECT
        cd_geocmu,
        nm_municipio,
        sg_uf,
        CASE sg_uf
            WHEN 'AC' THEN 'Norte'
            WHEN 'AM' THEN 'Norte'
            WHEN 'AP' THEN 'Norte'
            WHEN 'PA' THEN 'Norte'
            WHEN 'RO' THEN 'Norte'
            WHEN 'RR' THEN 'Norte'
            WHEN 'TO' THEN 'Norte'
            WHEN 'AL' THEN 'Nordeste'
            WHEN 'BA' THEN 'Nordeste'
            WHEN 'CE' THEN 'Nordeste'
            WHEN 'MA' THEN 'Nordeste'
            WHEN 'PB' THEN 'Nordeste'
            WHEN 'PE' THEN 'Nordeste'
            WHEN 'PI' THEN 'Nordeste'
            WHEN 'RN' THEN 'Nordeste'
            WHEN 'SE' THEN 'Nordeste'
            WHEN 'DF' THEN 'Centro-Oeste'
            WHEN 'GO' THEN 'Centro-Oeste'
            WHEN 'MS' THEN 'Centro-Oeste'
            WHEN 'MT' THEN 'Centro-Oeste'
            WHEN 'ES' THEN 'Sudeste'
            WHEN 'MG' THEN 'Sudeste'
            WHEN 'RJ' THEN 'Sudeste'
            WHEN 'SP' THEN 'Sudeste'
            WHEN 'PR' THEN 'Sul'
            WHEN 'RS' THEN 'Sul'
            WHEN 'SC' THEN 'Sul'
            ELSE 'Não Informada'
        END AS regiao
    FROM base
    ON CONFLICT (cd_geocmu, nm_municipio, sg_uf) DO NOTHING;
    """,
    # 3. Dimensão Cultura
    """
    CREATE TABLE IF NOT EXISTS gold.dim_cultura (
        sk_cultura          BIGSERIAL PRIMARY KEY,
        nm_cultura_global   VARCHAR(100) NOT NULL,
        nm_classif_produto  VARCHAR(100) NOT NULL,
        UNIQUE (nm_cultura_global, nm_classif_produto)
    );
    """,
    """
    INSERT INTO gold.dim_cultura (nm_cultura_global, nm_classif_produto)
    SELECT DISTINCT
        COALESCE(nm_cultura_global, 'Não Informada') AS nm_cultura_global,
        COALESCE(nm_classif_produto, 'Não Informada') AS nm_classif_produto
    FROM silver.psr_clean
    ON CONFLICT (nm_cultura_global, nm_classif_produto) DO NOTHING;
    """,
    # 4. Dimensão Seguradora
    """
    CREATE TABLE IF NOT EXISTS gold.dim_seguradora (
        sk_seguradora    BIGSERIAL PRIMARY KEY,
        nm_razao_social  VARCHAR(255) NOT NULL UNIQUE
    );
    """,
    """
    INSERT INTO gold.dim_seguradora (nm_razao_social)
    SELECT DISTINCT COALESCE(nm_razao_social, 'Não Informada') AS nm_razao_social
    FROM silver.psr_clean
    ON CONFLICT (nm_razao_social) DO NOTHING;
    """,
    # 5. Dimensão Evento Preponderante
    """
    CREATE TABLE IF NOT EXISTS gold.dim_evento (
        sk_evento             BIGSERIAL PRIMARY KEY,
        evento_preponderante  VARCHAR(255) NOT NULL UNIQUE
    );
    """,
    """
    INSERT INTO gold.dim_evento (evento_preponderante)
    SELECT DISTINCT
        COALESCE(evento_preponderante, 'Sem Sinistro / Não Informado')
            AS evento_preponderante
    FROM silver.psr_clean
    ON CONFLICT (evento_preponderante) DO NOTHING;
    """,
    # 6. Fato Apólices (grão: 1 linha por id_proposta)
    """
    CREATE TABLE IF NOT EXISTS gold.fct_apolices (
        id_proposta           BIGINT PRIMARY KEY,
        dt_apolice            DATE NOT NULL
            REFERENCES gold.dim_calendario (dt_referencia),
        sk_localidade         BIGINT NOT NULL
            REFERENCES gold.dim_localidade (sk_localidade),
        sk_cultura            BIGINT NOT NULL
            REFERENCES gold.dim_cultura (sk_cultura),
        sk_seguradora         BIGINT NOT NULL
            REFERENCES gold.dim_seguradora (sk_seguradora),
        sk_evento             BIGINT NOT NULL
            REFERENCES gold.dim_evento (sk_evento),
        ano_apolice           INTEGER NOT NULL,
        nr_area_total         NUMERIC(12, 4),
        vl_limite_garantia    NUMERIC(18, 2),
        vl_premio_liquido     NUMERIC(18, 2),
        vl_subvencao_federal  NUMERIC(18, 2),
        vl_premio_produtor    NUMERIC(18, 2),
        pe_taxa               NUMERIC(10, 4),
        nivel_de_cobertura    NUMERIC(10, 2),
        valor_indenizacao     NUMERIC(18, 2) NOT NULL DEFAULT 0,
        fl_sinistro           BOOLEAN NOT NULL DEFAULT FALSE,
        nr_decimal_latitude   NUMERIC(15, 10),
        nr_decimal_longitude  NUMERIC(15, 10)
    );
    """,
    """
    WITH base AS (
        SELECT
            s.id_proposta,
            s.dt_apolice,
            dl.sk_localidade,
            dc.sk_cultura,
            ds.sk_seguradora,
            de.sk_evento,
            s.ano_apolice,
            s.nr_area_total,
            s.vl_limite_garantia,
            s.vl_premio_liquido,
            s.vl_subvencao_federal,
            CASE
                WHEN s.vl_premio_liquido IS NOT NULL THEN
                    s.vl_premio_liquido - COALESCE(s.vl_subvencao_federal, 0)
                ELSE NULL
            END AS vl_premio_produtor,
            s.pe_taxa,
            s.nivel_de_cobertura,
            COALESCE(s.valor_indenizacao, 0)::NUMERIC(18, 2) AS valor_indenizacao,
            (COALESCE(s.valor_indenizacao, 0) > 0) AS fl_sinistro,
            s.nr_decimal_latitude,
            s.nr_decimal_longitude
        FROM silver.psr_clean AS s
        INNER JOIN gold.dim_localidade AS dl
            ON dl.cd_geocmu = COALESCE(s.cd_geocmu, 'N/I')
           AND dl.nm_municipio = COALESCE(s.nm_municipio_propriedade, 'Não Informado')
           AND dl.sg_uf = s.sg_uf_propriedade
        INNER JOIN gold.dim_cultura AS dc
            ON dc.nm_cultura_global = COALESCE(s.nm_cultura_global, 'Não Informada')
           AND dc.nm_classif_produto = COALESCE(s.nm_classif_produto, 'Não Informada')
        INNER JOIN gold.dim_seguradora AS ds
            ON ds.nm_razao_social = COALESCE(s.nm_razao_social, 'Não Informada')
        INNER JOIN gold.dim_evento AS de
            ON de.evento_preponderante = COALESCE(
                s.evento_preponderante, 'Sem Sinistro / Não Informado'
            )
    )
    INSERT INTO gold.fct_apolices (
        id_proposta,
        dt_apolice,
        sk_localidade,
        sk_cultura,
        sk_seguradora,
        sk_evento,
        ano_apolice,
        nr_area_total,
        vl_limite_garantia,
        vl_premio_liquido,
        vl_subvencao_federal,
        vl_premio_produtor,
        pe_taxa,
        nivel_de_cobertura,
        valor_indenizacao,
        fl_sinistro,
        nr_decimal_latitude,
        nr_decimal_longitude
    )
    SELECT
        id_proposta,
        dt_apolice,
        sk_localidade,
        sk_cultura,
        sk_seguradora,
        sk_evento,
        ano_apolice,
        nr_area_total,
        vl_limite_garantia,
        vl_premio_liquido,
        vl_subvencao_federal,
        vl_premio_produtor,
        pe_taxa,
        nivel_de_cobertura,
        valor_indenizacao,
        fl_sinistro,
        nr_decimal_latitude,
        nr_decimal_longitude
    FROM base
    ON CONFLICT (id_proposta) DO UPDATE SET
        dt_apolice           = EXCLUDED.dt_apolice,
        sk_localidade        = EXCLUDED.sk_localidade,
        sk_cultura           = EXCLUDED.sk_cultura,
        sk_seguradora        = EXCLUDED.sk_seguradora,
        sk_evento            = EXCLUDED.sk_evento,
        ano_apolice          = EXCLUDED.ano_apolice,
        nr_area_total        = EXCLUDED.nr_area_total,
        vl_limite_garantia   = EXCLUDED.vl_limite_garantia,
        vl_premio_liquido    = EXCLUDED.vl_premio_liquido,
        vl_subvencao_federal = EXCLUDED.vl_subvencao_federal,
        vl_premio_produtor   = EXCLUDED.vl_premio_produtor,
        pe_taxa              = EXCLUDED.pe_taxa,
        nivel_de_cobertura   = EXCLUDED.nivel_de_cobertura,
        valor_indenizacao    = EXCLUDED.valor_indenizacao,
        fl_sinistro          = EXCLUDED.fl_sinistro,
        nr_decimal_latitude  = EXCLUDED.nr_decimal_latitude,
        nr_decimal_longitude = EXCLUDED.nr_decimal_longitude;
    """,
    # Índices para performance em joins e filtros do Power BI
    "CREATE INDEX IF NOT EXISTS idx_fct_apolices_dt ON gold.fct_apolices (dt_apolice);",
    (
        "CREATE INDEX IF NOT EXISTS idx_fct_apolices_loc "
        "ON gold.fct_apolices (sk_localidade);"
    ),
    (
        "CREATE INDEX IF NOT EXISTS idx_fct_apolices_cult "
        "ON gold.fct_apolices (sk_cultura);"
    ),
    (
        "CREATE INDEX IF NOT EXISTS idx_fct_apolices_seg "
        "ON gold.fct_apolices (sk_seguradora);"
    ),
    # 7. View Analítica Agregada (KPIs por Ano / UF / Região)
    """
    CREATE OR REPLACE VIEW gold.vw_kpi_anual_uf AS
    SELECT
        f.ano_apolice,
        dl.sg_uf,
        dl.regiao,
        COUNT(*) AS qtd_apolices,
        COUNT(*) FILTER (WHERE f.fl_sinistro) AS qtd_sinistros,
        COALESCE(SUM(f.nr_area_total), 0)::NUMERIC(18, 2) AS total_area_ha,
        COALESCE(SUM(f.vl_limite_garantia), 0)::NUMERIC(18, 2)
            AS total_limite_garantia,
        COALESCE(SUM(f.vl_premio_liquido), 0)::NUMERIC(18, 2) AS total_premio_liquido,
        COALESCE(SUM(f.vl_subvencao_federal), 0)::NUMERIC(18, 2)
            AS total_subvencao_federal,
        COALESCE(SUM(f.valor_indenizacao), 0)::NUMERIC(18, 2) AS total_indenizacao,
        ROUND(
            COALESCE(SUM(f.valor_indenizacao), 0)
            / NULLIF(SUM(f.vl_premio_liquido), 0),
            4
        ) AS indice_sinistralidade
    FROM gold.fct_apolices AS f
    INNER JOIN gold.dim_localidade AS dl
        ON dl.sk_localidade = f.sk_localidade
    GROUP BY f.ano_apolice, dl.sg_uf, dl.regiao;
    """,
)

GOLD_VALIDATION_SQL = """
SELECT
    (SELECT COUNT(*) FROM gold.dim_calendario) AS dim_calendario,
    (SELECT COUNT(*) FROM gold.dim_localidade) AS dim_localidade,
    (SELECT COUNT(*) FROM gold.dim_cultura) AS dim_cultura,
    (SELECT COUNT(*) FROM gold.dim_seguradora) AS dim_seguradora,
    (SELECT COUNT(*) FROM gold.dim_evento) AS dim_evento,
    (SELECT COUNT(*) FROM gold.fct_apolices) AS fct_apolices,
    (SELECT COUNT(*) FROM gold.vw_kpi_anual_uf) AS vw_kpi_anual_uf;
"""


def run_gold_load(engine: Engine | None = None) -> dict[str, int]:
    """Constrói e atualiza o Star Schema da camada gold para o Power BI."""
    db_engine = engine or get_engine()
    with db_engine.begin() as conn:
        for stmt in GOLD_BUILD_STATEMENTS:
            conn.execute(text(stmt))
        stats = dict(conn.execute(text(GOLD_VALIDATION_SQL)).mappings().one())

    for table_name, count in stats.items():
        print(f"gold.{table_name}: {count:,} linhas")
    return stats


if __name__ == "__main__":
    run_gold_load()
