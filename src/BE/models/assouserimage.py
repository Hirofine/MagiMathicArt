from sqlalchemy import Column, Integer, ForeignKey
from app.config.database import Base

# Modèle SQLAlchemy pour la table d'association "AssoUserImage"
class AssoUserImage(Base):
    __tablename__ = "AssoUserImage"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    image_id = Column(Integer, ForeignKey("images.id"), primary_key=True)