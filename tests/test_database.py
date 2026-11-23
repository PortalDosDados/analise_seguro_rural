import pytest

from database import _load_db_config, get_engine


def test_load_db_config_sucesso(monkeypatch: pytest.MonkeyPatch) -> None:
    """Deve carregar todas as variáveis quando definidas no ambiente."""
    monkeypatch.setenv("DB_USER", "usuario_teste")
    monkeypatch.setenv("DB_PASS", "senha@123")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "db_teste")

    cfg = _load_db_config()

    assert cfg["DB_USER"] == "usuario_teste"
    assert cfg["DB_PORT"] == "5432"
    assert cfg["DB_NAME"] == "db_teste"


def test_load_db_config_variavel_ausente(monkeypatch: pytest.MonkeyPatch) -> None:
    """Deve lançar ValueError quando faltar alguma variável obrigatória."""
    for var in ("DB_USER", "DB_PASS", "DB_HOST", "DB_PORT", "DB_NAME"):
        monkeypatch.setenv(var, "valor")
    monkeypatch.delenv("DB_PASS", raising=False)

    with pytest.raises(ValueError, match="DB_PASS"):
        _load_db_config()


def test_get_engine_cria_url_valida(monkeypatch: pytest.MonkeyPatch) -> None:
    """Deve retornar Engine SQLAlchemy com driver postgresql+psycopg2."""
    monkeypatch.setenv("DB_USER", "usr")
    monkeypatch.setenv("DB_PASS", "p@ss/word")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "db_seguro_rural")

    engine = get_engine()

    assert engine.url.drivername == "postgresql+psycopg2"
    assert engine.url.database == "db_seguro_rural"
