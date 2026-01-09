import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# Pega a URL do ambiente (Vercel ou .env)
uri = os.getenv("DATABASE_URL")

if not uri:
    raise ValueError("A variável DATABASE_URL não foi encontrada.")

# Ajuste crucial: PostgreSQL exige que a URL comece com postgresql://
# E forçamos o uso do driver psycopg2 que você instalou
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql+psycopg2://", 1)
elif uri.startswith("postgresql://"):
    uri = uri.replace("postgresql://", "postgresql+psycopg2://", 1)

# Removemos o "check_same_thread" pois ele quebra no Postgres
engine = create_engine(uri)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
