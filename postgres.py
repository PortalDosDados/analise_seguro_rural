from sqlalchemy import text
from conexao import get_engine

def executar_comando_manual():
    engine = get_engine()
    if engine is None: return

    # --- COMANDO SQL DO CIENTISTA DE DADOS ---
    # Criação da tabela tb_seguro_rural
    # Observações:
    # 1. Usei BIGINT para IDs que podem ser grandes.
    # 2. Usei NUMERIC(18,2) para dinheiro.
    # 3. Usei VARCHAR para textos variáveis.
    # 4. id_proposta foi definido como PRIMARY KEY (chave única).

    MEU_COMANDO_SQL = """
    DROP TABLE IF EXISTS tb_seguro_rural; -- Cuidado: Apaga a tabela se existir para recriar do zero

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
        latitude                  VARCHAR(50), -- Mantive texto pois seus dados originais têm formatação suja
        nr_grau_lat               VARCHAR(10),
        nr_min_lat                VARCHAR(10),
        nr_seg_lat                VARCHAR(10),
        longitude                 VARCHAR(50),
        nr_grau_long              VARCHAR(10),
        nr_min_long               VARCHAR(10),
        nr_seg_long               VARCHAR(10),
        nr_decimal_latitude       NUMERIC(15, 10), -- Alta precisão para GPS
        nr_decimal_longitude      NUMERIC(15, 10),
        nm_classif_produto        VARCHAR(100),
        nm_cultura_global         VARCHAR(100),
        nr_area_total             NUMERIC(12, 4), -- Área pode ter casas decimais
        nr_animal                 NUMERIC(10, 2), -- Aceita NULL (vimos que tem 0 non-null)
        nr_produtividade_estimada NUMERIC(12, 2),
        nr_produtividade_segurada NUMERIC(12, 2),
        nivel_de_cobertura        NUMERIC(10, 2),
        vl_limite_garantia        NUMERIC(18, 2), -- Dinheiro
        vl_premio_liquido         NUMERIC(18, 2), -- Dinheiro
        pe_taxa                   NUMERIC(10, 4), -- Taxa percentual
        vl_subvencao_federal      NUMERIC(18, 2),
        nr_apolice                VARCHAR(100),
        dt_apolice                DATE,
        ano_apolice               INTEGER,
        cd_geocmu                 VARCHAR(20),
        valor_indenizacao         NUMERIC(18, 2), -- Removi acento e cedilha
        evento_preponderante      VARCHAR(255)
    );
    """
    # ----------------------------------------

    try:
        print("🔨 Criando a estrutura da tabela 'tb_seguro_rural'...")
        with engine.connect() as conn:
            conn.execute(text(MEU_COMANDO_SQL))
            conn.commit()
        print("✅ Tabela criada com sucesso! Pronta para receber dados.")

    except Exception as e:
        print(f"❌ Erro ao criar tabela: {e}")

if __name__ == "__main__":
    executar_comando_manual()