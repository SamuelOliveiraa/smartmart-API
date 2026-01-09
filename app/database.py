import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# Pega a URL do ambiente
uri = os.getenv("DATABASE_URL")

if not uri:
    raise ValueError("A variável DATABASE_URL não foi encontrada.")

if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql+psycopg2://", 1)
elif uri.startswith("postgresql://"):
    uri = uri.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(
    uri,
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
