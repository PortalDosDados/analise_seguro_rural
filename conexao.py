import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from sqlalchemy import create_engine

# 1. Carrega as variáveis do .env
load_dotenv()

USER = os.getenv('DB_USER')
PASS = os.getenv('DB_PASS')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')
DB   = os.getenv('DB_NAME')

def get_engine():
    """
    Retorna a engine de conexão do SQLAlchemy pronta para uso.
    """
    try:
        # Tratamento de caracteres especiais na senha (seu fix anterior)
        pass_encoded = quote_plus(PASS)
        user_encoded = quote_plus(USER)

        # String de conexão
        connection_str = f'postgresql+psycopg2://{user_encoded}:{pass_encoded}@{HOST}:{PORT}/{DB}'

        # Cria e retorna a engine
        engine = create_engine(connection_str, client_encoding='utf8')
        return engine

    except Exception as e:
        print(f"❌ Erro ao configurar engine: {e}")
        return None