from load_gold import GOLD_BUILD_STATEMENTS, run_gold_load


class _FakeResult:
    def mappings(self) -> "_FakeResult":
        return self

    def one(self) -> dict[str, int]:
        return {
            "dim_calendario": 7305,
            "dim_localidade": 4348,
            "dim_cultura": 69,
            "dim_seguradora": 20,
            "dim_evento": 16,
            "fct_apolices": 1000,
            "vw_kpi_anual_uf": 540,
        }


class _FakeConn:
    def __init__(self) -> None:
        self.executed: list[str] = []

    def execute(self, statement: object) -> _FakeResult:
        self.executed.append(str(statement))
        return _FakeResult()

    def __enter__(self) -> "_FakeConn":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class _FakeEngine:
    def __init__(self) -> None:
        self.conn = _FakeConn()

    def begin(self) -> _FakeConn:
        return self.conn


def test_gold_sql_respeita_arquitetura_e_lgpd() -> None:
    """Garante leitura exclusiva da silver, sem SELECT * e sem PII."""
    sql_all = "\n".join(GOLD_BUILD_STATEMENTS)

    assert "bronze.psr_raw" not in sql_all
    assert "SELECT *" not in sql_all
    assert "nm_segurado" not in sql_all
    assert "nr_documento_segurado" not in sql_all
    assert "gold.dim_calendario" in sql_all
    assert "gold.dim_localidade" in sql_all
    assert "gold.dim_cultura" in sql_all
    assert "gold.dim_seguradora" in sql_all
    assert "gold.dim_evento" in sql_all
    assert "gold.fct_apolices" in sql_all
    assert "gold.vw_kpi_anual_uf" in sql_all


def test_run_gold_load_executa_todas_instrucoes() -> None:
    """Garante execução completa da camada gold e retorno de contagens."""
    fake_engine = _FakeEngine()
    stats = run_gold_load(engine=fake_engine)  # type: ignore[arg-type]

    assert len(fake_engine.conn.executed) == len(GOLD_BUILD_STATEMENTS) + 1
    assert stats["fct_apolices"] == 1000
