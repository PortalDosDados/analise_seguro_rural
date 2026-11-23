import pandas as pd

from load_bronze import BRONZE_COLUMNS, normalize_bronze_chunk


def test_normalize_bronze_chunk_mapeia_colunas_e_origem() -> None:
    """Deve renomear colunas especiais e adicionar arquivo_origem na ordem."""
    csv_cols = [
        "NM_RAZAO_SOCIAL",
        "CD_PROCESSO_SUSEP",
        "NR_PROPOSTA",
        "ID_PROPOSTA",
        "DT_PROPOSTA",
        "DT_INICIO_VIGENCIA",
        "DT_FIM_VIGENCIA",
        "NM_SEGURADO",
        "NR_DOCUMENTO_SEGURADO",
        "NM_MUNICIPIO_PROPRIEDADE",
        "SG_UF_PROPRIEDADE",
        "LATITUDE",
        "NR_GRAU_LAT",
        "NR_MIN_LAT",
        "NR_SEG_LAT",
        "LONGITUDE",
        "NR_GRAU_LONG",
        "NR_MIN_LONG",
        "NR_SEG_LONG",
        "NR_DECIMAL_LATITUDE",
        "NR_DECIMAL_LONGITUDE",
        "NM_CLASSIF_PRODUTO",
        "NM_CULTURA_GLOBAL",
        "NR_AREA_TOTAL",
        "NR_ANIMAL",
        "NR_PRODUTIVIDADE_ESTIMADA",
        "NR_PRODUTIVIDADE_SEGURADA",
        "NivelDeCobertura",
        "VL_LIMITE_GARANTIA",
        "VL_PREMIO_LIQUIDO",
        "PE_TAXA",
        "VL_SUBVENCAO_FEDERAL",
        "NR_APOLICE",
        "DT_APOLICE",
        "ANO_APOLICE",
        "CD_GEOCMU",
        "VALOR_INDENIZAÇÃO",
        "EVENTO_PREPONDERANTE",
    ]
    df = pd.DataFrame([["x"] * len(csv_cols)], columns=csv_cols)

    result = normalize_bronze_chunk(df, "psr_teste.csv")

    assert tuple(result.columns) == BRONZE_COLUMNS
    assert result.loc[0, "arquivo_origem"] == "psr_teste.csv"
    assert result.loc[0, "nivel_de_cobertura"] == "x"
    assert result.loc[0, "valor_indenizacao"] == "x"
