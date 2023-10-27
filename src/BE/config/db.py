from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from config.settings import Settings

# Créez une instance de moteur de base de données en utilisant l'URL de connexion configurée dans les paramètres.
database_url = Settings.database_url
meta = MetaData()
engine = create_engine(database_url)

# Créez une classe de base pour les modèles SQLAlchemy.
Base = declarative_base()
conn = engine.connect()
# Créez une classe de session pour interagir avec la base de données.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()