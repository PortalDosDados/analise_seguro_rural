import io
from pathlib import Path

import pandas as pd
from sqlalchemy.engine import Engine

from database import get_engine

SOURCE_FILES: tuple[Path, ...] = (
    Path("data/psr_2006_2015.csv"),
    Path("data/psr_2016_2024.csv"),
    Path("data/psr_2025.csv"),
)

COLUMN_RENAME_MAP: dict[str, str] = {
    "NivelDeCobertura": "nivel_de_cobertura",
    "VALOR_INDENIZAÇÃO": "valor_indenizacao",
}

BRONZE_COLUMNS: tuple[str, ...] = (
    "nm_razao_social",
    "cd_processo_susep",
    "nr_proposta",
    "id_proposta",
    "dt_proposta",
    "dt_inicio_vigencia",
    "dt_fim_vigencia",
    "nm_segurado",
    "nr_documento_segurado",
    "nm_municipio_propriedade",
    "sg_uf_propriedade",
    "latitude",
    "nr_grau_lat",
    "nr_min_lat",
    "nr_seg_lat",
    "longitude",
    "nr_grau_long",
    "nr_min_long",
    "nr_seg_long",
    "nr_decimal_latitude",
    "nr_decimal_longitude",
    "nm_classif_produto",
    "nm_cultura_global",
    "nr_area_total",
    "nr_animal",
    "nr_produtividade_estimada",
    "nr_produtividade_segurada",
    "nivel_de_cobertura",
    "vl_limite_garantia",
    "vl_premio_liquido",
    "pe_taxa",
    "vl_subvencao_federal",
    "nr_apolice",
    "dt_apolice",
    "ano_apolice",
    "cd_geocmu",
    "valor_indenizacao",
    "evento_preponderante",
    "arquivo_origem",
)


def normalize_bronze_chunk(df: pd.DataFrame, arquivo_origem: str) -> pd.DataFrame:
    """Padroniza nomes de colunas e adiciona coluna de rastreabilidade."""
    renamed = df.rename(
        columns=lambda col: COLUMN_RENAME_MAP.get(col, col.lower())
    ).copy()
    renamed["arquivo_origem"] = arquivo_origem
    return renamed[list(BRONZE_COLUMNS)]


def load_file_to_bronze(
    file_path: Path, engine: Engine, chunksize: int = 50_000
) -> int:
    """Carrega um CSV bruto para bronze.psr_raw via COPY de forma idempotente."""
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    arquivo_origem = file_path.name
    cols_sql = ", ".join(BRONZE_COLUMNS)
    copy_sql = f"COPY bronze.psr_raw ({cols_sql}) FROM STDIN WITH (FORMAT csv)"

    total_rows = 0
    raw_conn = engine.raw_connection()
    try:
        with raw_conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM bronze.psr_raw WHERE arquivo_origem = %s",
                (arquivo_origem,),
            )
            reader = pd.read_csv(
                file_path,
                sep=";",
                encoding="latin1",
                dtype=str,
                keep_default_na=False,
                chunksize=chunksize,
                on_bad_lines="warn",
            )
            for chunk in reader:
                df_norm = normalize_bronze_chunk(chunk, arquivo_origem)
                buf = io.StringIO()
                df_norm.to_csv(buf, index=False, header=False)
                buf.seek(0)
                cursor.copy_expert(copy_sql, buf)
                total_rows += len(df_norm)
        raw_conn.commit()
    except Exception:
        raw_conn.rollback()
        raise
    finally:
        raw_conn.close()

    return total_rows


def run_bronze_load(
    files: tuple[Path, ...] = SOURCE_FILES, engine: Engine | None = None
) -> int:
    """Executa a carga completa da camada bronze para os arquivos configurados."""
    db_engine = engine or get_engine()
    total = 0
    for file_path in files:
        count = load_file_to_bronze(file_path, db_engine)
        print(f"Carregado {file_path.name}: {count:,} linhas")
        total += count
    print(f"Total ingerido em bronze.psr_raw: {total:,} linhas")
    return total


if __name__ == "__main__":
    run_bronze_load()
