# kebab_app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Crea un file locale 'kebab.db'.
# L'argomento check_same_thread=False è necessario in SQLite per richieste asincrone concorrenti.
SQLALCHEMY_DATABASE_URL = "sqlite:///./kebab.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
