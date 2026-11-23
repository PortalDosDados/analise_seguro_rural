from setup_db import DDL_STATEMENTS, setup_medallion_schemas


class _FakeConn:
    def __init__(self) -> None:
        self.executed: list[str] = []

    def execute(self, statement: object) -> None:
        self.executed.append(str(statement))

    def __enter__(self) -> "_FakeConn":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class _FakeEngine:
    def __init__(self) -> None:
        self.conn = _FakeConn()

    def begin(self) -> _FakeConn:
        return self.conn


def test_ddl_contem_schemas_medalhao() -> None:
    """Garante criação dos três schemas e omissão de PII na camada silver."""
    sql_all = "\n".join(DDL_STATEMENTS)
    assert "CREATE SCHEMA IF NOT EXISTS bronze;" in sql_all
    assert "CREATE SCHEMA IF NOT EXISTS silver;" in sql_all
    assert "CREATE SCHEMA IF NOT EXISTS gold;" in sql_all
    assert "CREATE TABLE IF NOT EXISTS bronze.psr_raw" in sql_all
    assert "CREATE TABLE IF NOT EXISTS silver.psr_clean" in sql_all

    silver_ddl = DDL_STATEMENTS[-1]
    assert "nm_segurado" not in silver_ddl
    assert "nr_documento_segurado" not in silver_ddl


def test_setup_medallion_schemas_executa_todas_ddls() -> None:
    """Garante que todas as instruções DDL são executadas em transação."""
    fake_engine = _FakeEngine()
    setup_medallion_schemas(engine=fake_engine)  # type: ignore[arg-type]

    assert len(fake_engine.conn.executed) == len(DDL_STATEMENTS)
