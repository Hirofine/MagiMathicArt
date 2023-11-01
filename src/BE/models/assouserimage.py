from sqlalchemy import Column, Integer, ForeignKey
from config.db import Base

# Modèle SQLAlchemy pour la table d'association "AssoUserImage"
class AssoUserImage(Base):
    __tablename__ = "AssoUserImage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    image_id = Column(Integer, ForeignKey("Images.id"))