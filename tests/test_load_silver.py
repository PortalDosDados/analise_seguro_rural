from load_silver import build_silver_upsert_sql, run_silver_load


class _FakeResult:
    def mappings(self) -> "_FakeResult":
        return self

    def one(self) -> dict[str, int]:
        return {
            "total_bronze": 100,
            "total_silver": 99,
            "ano_min": 2006,
            "ano_max": 2025,
            "taxa_nula": 1,
            "apolices_indenizadas": 10,
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


def test_silver_sql_omite_pii_e_garante_idempotencia() -> None:
    """Garante omissão de colunas PII, deduplicação e upsert idempotente."""
    sql = build_silver_upsert_sql()

    assert "FROM bronze.psr_raw" in sql
    assert "INSERT INTO silver.psr_clean" in sql
    assert "ROW_NUMBER() OVER" in sql
    assert "ON CONFLICT (id_proposta) DO UPDATE SET" in sql
    assert "nm_segurado" not in sql
    assert "nr_documento_segurado" not in sql


def test_run_silver_load_retorna_metricas() -> None:
    """Garante execução transacional e retorno das métricas de validação."""
    fake_engine = _FakeEngine()
    stats = run_silver_load(engine=fake_engine)  # type: ignore[arg-type]

    assert len(fake_engine.conn.executed) == 2
    assert stats["total_silver"] == 99
    assert stats["ano_min"] == 2006
