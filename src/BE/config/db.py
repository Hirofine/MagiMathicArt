from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

# Créez une instance de moteur de base de données en utilisant l'URL de connexion configurée dans les paramètres.
database_url = settings.database_url
engine = create_engine(database_url)

# Créez une classe de base pour les modèles SQLAlchemy.
Base = DeclarativeBase()

# Créez une classe de session pour interagir avec la base de données.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
