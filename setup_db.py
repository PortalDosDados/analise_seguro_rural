from sqlalchemy import text
from sqlalchemy.engine import Engine

from database import get_engine

DDL_STATEMENTS: tuple[str, ...] = (
    "CREATE SCHEMA IF NOT EXISTS bronze;",
    "CREATE SCHEMA IF NOT EXISTS silver;",
    "CREATE SCHEMA IF NOT EXISTS gold;",
    "DROP TABLE IF EXISTS public.tb_seguro_rural;",
    """
    CREATE TABLE IF NOT EXISTS bronze.psr_raw (
        nm_razao_social           TEXT,
        cd_processo_susep         TEXT,
        nr_proposta               TEXT,
        id_proposta               TEXT,
        dt_proposta               TEXT,
        dt_inicio_vigencia        TEXT,
        dt_fim_vigencia           TEXT,
        nm_segurado               TEXT,
        nr_documento_segurado     TEXT,
        nm_municipio_propriedade  TEXT,
        sg_uf_propriedade         TEXT,
        latitude                  TEXT,
        nr_grau_lat               TEXT,
        nr_min_lat                TEXT,
        nr_seg_lat                TEXT,
        longitude                 TEXT,
        nr_grau_long              TEXT,
        nr_min_long               TEXT,
        nr_seg_long               TEXT,
        nr_decimal_latitude       TEXT,
        nr_decimal_longitude      TEXT,
        nm_classif_produto        TEXT,
        nm_cultura_global         TEXT,
        nr_area_total             TEXT,
        nr_animal                 TEXT,
        nr_produtividade_estimada TEXT,
        nr_produtividade_segurada TEXT,
        nivel_de_cobertura        TEXT,
        vl_limite_garantia        TEXT,
        vl_premio_liquido         TEXT,
        pe_taxa                   TEXT,
        vl_subvencao_federal      TEXT,
        nr_apolice                TEXT,
        dt_apolice                TEXT,
        ano_apolice               TEXT,
        cd_geocmu                 TEXT,
        valor_indenizacao         TEXT,
        evento_preponderante      TEXT,
        arquivo_origem            TEXT,
        dt_ingestao               TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS silver.tb_seguro_rural (
        id_proposta               BIGINT PRIMARY KEY,
        nm_razao_social           VARCHAR(255),
        cd_processo_susep         BIGINT,
        nr_proposta               VARCHAR(100),
        dt_proposta               DATE,
        dt_inicio_vigencia        DATE,
        dt_fim_vigencia           DATE,
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
        evento_preponderante      VARCHAR(255),
        dt_carga                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """,
)


def setup_medallion_schemas(engine: Engine | None = None) -> None:
    """Cria os schemas bronze, silver e gold e as tabelas iniciais."""
    db_engine = engine or get_engine()
    with db_engine.begin() as conn:
        for stmt in DDL_STATEMENTS:
            conn.execute(text(stmt))
    print("Schemas bronze, silver e gold estruturados com sucesso.")


if __name__ == "__main__":
    setup_medallion_schemas()
