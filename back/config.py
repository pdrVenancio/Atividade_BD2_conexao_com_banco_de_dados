from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB_CONFIG = {
    'url': 'postgresql+psycopg://postgres:root@localhost/postgres'
}

# Criar engine e sessão
engine = create_engine(DB_CONFIG['url'])
Session = sessionmaker(bind=engine)