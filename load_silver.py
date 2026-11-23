from sqlalchemy import text
from sqlalchemy.engine import Engine

from database import get_engine


def _safe_text(col: str) -> str:
    """Normaliza espaços e converte vazio ou '-' em NULL."""
    return f"NULLIF(NULLIF(TRIM({col}), ''), '-')"


def _safe_numeric(col: str, precision: int, scale: int) -> str:
    """Normaliza vírgula decimal e converte apenas valores numéricos válidos."""
    cleaned = f"REPLACE(TRIM({col}), ',', '.')"
    regex = r"'^-?[0-9]+(\.[0-9]+)?$'"
    return (
        f"CASE WHEN {cleaned} ~ {regex} "
        f"THEN ROUND(({cleaned})::NUMERIC, {scale})::NUMERIC({precision}, {scale}) "
        f"ELSE NULL END"
    )


def _safe_int(col: str, target_type: str = "INTEGER") -> str:
    """Converte inteiros válidos removendo espaços e '-'."""
    return (
        f"CASE WHEN TRIM({col}) ~ '^[0-9]+$' "
        f"THEN TRIM({col})::{target_type} ELSE NULL END"
    )


def _safe_date(col: str) -> str:
    """Converte datas no formato brasileiro DD/MM/YYYY."""
    return (
        f"CASE WHEN TRIM({col}) ~ '^[0-9]{{2}}/[0-9]{{2}}/[0-9]{{4}}$' "
        f"THEN TO_DATE(TRIM({col}), 'DD/MM/YYYY') ELSE NULL END"
    )


def build_silver_upsert_sql() -> str:
    """Monta a query ELT idempotente de bronze.psr_raw para silver.psr_clean."""
    return f"""
    WITH cleaned AS (
        SELECT
            {_safe_int("id_proposta", "BIGINT")} AS id_proposta,
            {_safe_text("nm_razao_social")}::VARCHAR(255) AS nm_razao_social,
            {_safe_int("cd_processo_susep", "BIGINT")} AS cd_processo_susep,
            {_safe_text("nr_proposta")}::VARCHAR(100) AS nr_proposta,
            {_safe_date("dt_proposta")} AS dt_proposta,
            {_safe_date("dt_inicio_vigencia")} AS dt_inicio_vigencia,
            {_safe_date("dt_fim_vigencia")} AS dt_fim_vigencia,
            {_safe_text("nm_municipio_propriedade")}::VARCHAR(255)
                AS nm_municipio_propriedade,
            UPPER({_safe_text("sg_uf_propriedade")})::CHAR(2) AS sg_uf_propriedade,
            {_safe_text("latitude")}::VARCHAR(50) AS latitude,
            {_safe_text("nr_grau_lat")}::VARCHAR(10) AS nr_grau_lat,
            {_safe_text("nr_min_lat")}::VARCHAR(10) AS nr_min_lat,
            {_safe_text("nr_seg_lat")}::VARCHAR(10) AS nr_seg_lat,
            {_safe_text("longitude")}::VARCHAR(50) AS longitude,
            {_safe_text("nr_grau_long")}::VARCHAR(10) AS nr_grau_long,
            {_safe_text("nr_min_long")}::VARCHAR(10) AS nr_min_long,
            {_safe_text("nr_seg_long")}::VARCHAR(10) AS nr_seg_long,
            {_safe_numeric("nr_decimal_latitude", 15, 10)} AS nr_decimal_latitude,
            {_safe_numeric("nr_decimal_longitude", 15, 10)} AS nr_decimal_longitude,
            {_safe_text("nm_classif_produto")}::VARCHAR(100) AS nm_classif_produto,
            {_safe_text("nm_cultura_global")}::VARCHAR(100) AS nm_cultura_global,
            {_safe_numeric("nr_area_total", 12, 4)} AS nr_area_total,
            {_safe_numeric("nr_animal", 10, 2)} AS nr_animal,
            {_safe_numeric("nr_produtividade_estimada", 12, 2)}
                AS nr_produtividade_estimada,
            {_safe_numeric("nr_produtividade_segurada", 12, 2)}
                AS nr_produtividade_segurada,
            {_safe_numeric("nivel_de_cobertura", 10, 2)} AS nivel_de_cobertura,
            {_safe_numeric("vl_limite_garantia", 18, 2)} AS vl_limite_garantia,
            {_safe_numeric("vl_premio_liquido", 18, 2)} AS vl_premio_liquido,
            {_safe_numeric("pe_taxa", 10, 4)} AS pe_taxa,
            {_safe_numeric("vl_subvencao_federal", 18, 2)} AS vl_subvencao_federal,
            {_safe_text("nr_apolice")}::VARCHAR(100) AS nr_apolice,
            {_safe_date("dt_apolice")} AS dt_apolice,
            {_safe_int("ano_apolice", "INTEGER")} AS ano_apolice,
            {_safe_text("cd_geocmu")}::VARCHAR(20) AS cd_geocmu,
            {_safe_numeric("valor_indenizacao", 18, 2)} AS valor_indenizacao,
            {_safe_text("evento_preponderante")}::VARCHAR(255) AS evento_preponderante,
            arquivo_origem,
            dt_ingestao
        FROM bronze.psr_raw
        WHERE TRIM(id_proposta) ~ '^[0-9]+$'
    ),
    deduplicated AS (
        SELECT
            *,
            ROW_NUMBER() OVER (
                PARTITION BY id_proposta
                ORDER BY arquivo_origem DESC, dt_ingestao DESC
            ) AS rn
        FROM cleaned
    )
    INSERT INTO silver.psr_clean (
        id_proposta,
        nm_razao_social,
        cd_processo_susep,
        nr_proposta,
        dt_proposta,
        dt_inicio_vigencia,
        dt_fim_vigencia,
        nm_municipio_propriedade,
        sg_uf_propriedade,
        latitude,
        nr_grau_lat,
        nr_min_lat,
        nr_seg_lat,
        longitude,
        nr_grau_long,
        nr_min_long,
        nr_seg_long,
        nr_decimal_latitude,
        nr_decimal_longitude,
        nm_classif_produto,
        nm_cultura_global,
        nr_area_total,
        nr_animal,
        nr_produtividade_estimada,
        nr_produtividade_segurada,
        nivel_de_cobertura,
        vl_limite_garantia,
        vl_premio_liquido,
        pe_taxa,
        vl_subvencao_federal,
        nr_apolice,
        dt_apolice,
        ano_apolice,
        cd_geocmu,
        valor_indenizacao,
        evento_preponderante,
        dt_carga
    )
    SELECT
        id_proposta,
        nm_razao_social,
        cd_processo_susep,
        nr_proposta,
        dt_proposta,
        dt_inicio_vigencia,
        dt_fim_vigencia,
        nm_municipio_propriedade,
        sg_uf_propriedade,
        latitude,
        nr_grau_lat,
        nr_min_lat,
        nr_seg_lat,
        longitude,
        nr_grau_long,
        nr_min_long,
        nr_seg_long,
        nr_decimal_latitude,
        nr_decimal_longitude,
        nm_classif_produto,
        nm_cultura_global,
        nr_area_total,
        nr_animal,
        nr_produtividade_estimada,
        nr_produtividade_segurada,
        nivel_de_cobertura,
        vl_limite_garantia,
        vl_premio_liquido,
        pe_taxa,
        vl_subvencao_federal,
        nr_apolice,
        dt_apolice,
        ano_apolice,
        cd_geocmu,
        valor_indenizacao,
        evento_preponderante,
        NOW()
    FROM deduplicated
    WHERE rn = 1
    ON CONFLICT (id_proposta) DO UPDATE SET
        nm_razao_social           = EXCLUDED.nm_razao_social,
        cd_processo_susep         = EXCLUDED.cd_processo_susep,
        nr_proposta               = EXCLUDED.nr_proposta,
        dt_proposta               = EXCLUDED.dt_proposta,
        dt_inicio_vigencia        = EXCLUDED.dt_inicio_vigencia,
        dt_fim_vigencia           = EXCLUDED.dt_fim_vigencia,
        nm_municipio_propriedade  = EXCLUDED.nm_municipio_propriedade,
        sg_uf_propriedade         = EXCLUDED.sg_uf_propriedade,
        latitude                  = EXCLUDED.latitude,
        nr_grau_lat               = EXCLUDED.nr_grau_lat,
        nr_min_lat                = EXCLUDED.nr_min_lat,
        nr_seg_lat                = EXCLUDED.nr_seg_lat,
        longitude                 = EXCLUDED.longitude,
        nr_grau_long              = EXCLUDED.nr_grau_long,
        nr_min_long               = EXCLUDED.nr_min_long,
        nr_seg_long               = EXCLUDED.nr_seg_long,
        nr_decimal_latitude       = EXCLUDED.nr_decimal_latitude,
        nr_decimal_longitude      = EXCLUDED.nr_decimal_longitude,
        nm_classif_produto        = EXCLUDED.nm_classif_produto,
        nm_cultura_global         = EXCLUDED.nm_cultura_global,
        nr_area_total             = EXCLUDED.nr_area_total,
        nr_animal                 = EXCLUDED.nr_animal,
        nr_produtividade_estimada = EXCLUDED.nr_produtividade_estimada,
        nr_produtividade_segurada = EXCLUDED.nr_produtividade_segurada,
        nivel_de_cobertura        = EXCLUDED.nivel_de_cobertura,
        vl_limite_garantia        = EXCLUDED.vl_limite_garantia,
        vl_premio_liquido         = EXCLUDED.vl_premio_liquido,
        pe_taxa                   = EXCLUDED.pe_taxa,
        vl_subvencao_federal      = EXCLUDED.vl_subvencao_federal,
        nr_apolice                = EXCLUDED.nr_apolice,
        dt_apolice                = EXCLUDED.dt_apolice,
        ano_apolice               = EXCLUDED.ano_apolice,
        cd_geocmu                 = EXCLUDED.cd_geocmu,
        valor_indenizacao         = EXCLUDED.valor_indenizacao,
        evento_preponderante      = EXCLUDED.evento_preponderante,
        dt_carga                  = NOW();
    """


VALIDATION_SQL = """
SELECT
    (SELECT COUNT(*) FROM bronze.psr_raw) AS total_bronze,
    COUNT(*) AS total_silver,
    MIN(ano_apolice) AS ano_min,
    MAX(ano_apolice) AS ano_max,
    COUNT(*) FILTER (WHERE pe_taxa IS NULL) AS taxa_nula,
    COUNT(*) FILTER (WHERE valor_indenizacao IS NOT NULL) AS apolices_indenizadas
FROM silver.psr_clean;
"""


def run_silver_load(engine: Engine | None = None) -> dict[str, int]:
    """Executa a transformação bronze -> silver e retorna métricas de qualidade."""
    db_engine = engine or get_engine()
    upsert_sql = build_silver_upsert_sql()

    with db_engine.begin() as conn:
        conn.execute(text(upsert_sql))
        stats = dict(conn.execute(text(VALIDATION_SQL)).mappings().one())

    duplicatas = stats["total_bronze"] - stats["total_silver"]
    print(f"Bronze: {stats['total_bronze']:,} linhas")
    print(f"Silver: {stats['total_silver']:,} linhas (deduplicadas: {duplicatas:,})")
    print(f"Período (ano_apolice): {stats['ano_min']} a {stats['ano_max']}")
    print(f"Apólices com indenização: {stats['apolices_indenizadas']:,}")
    return stats


if __name__ == "__main__":
    run_silver_load()
