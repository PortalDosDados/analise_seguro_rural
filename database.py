import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL, Engine

load_dotenv()

REQUIRED_ENV_VARS = ("DB_USER", "DB_PASS", "DB_HOST", "DB_PORT", "DB_NAME")


def _load_db_config() -> dict[str, str]:
    """Lê e valida as variáveis de ambiente necessárias para conexão."""
    config = {var: os.getenv(var, "").strip() for var in REQUIRED_ENV_VARS}
    missing = [var for var, val in config.items() if not val]
    if missing:
        raise ValueError(
            f"Variáveis de ambiente ausentes no .env: {', '.join(missing)}"
        )
    return config


def get_engine() -> Engine:
    """Cria e retorna a engine SQLAlchemy para o PostgreSQL."""
    cfg = _load_db_config()
    url = URL.create(
        drivername="postgresql+psycopg2",
        username=cfg["DB_USER"],
        password=cfg["DB_PASS"],
        host=cfg["DB_HOST"],
        port=int(cfg["DB_PORT"]),
        database=cfg["DB_NAME"],
    )
    return create_engine(url, pool_pre_ping=True)


def test_connection() -> bool:
    """Testa a conectividade com o banco executando uma consulta simples."""
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();")).scalar()
        print(f"Conexão estabelecida com sucesso: {result}")
    return True


if __name__ == "__main__":
    test_connection()
