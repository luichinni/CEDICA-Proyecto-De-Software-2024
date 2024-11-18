from src.core.database import db
from datetime import datetime
import enum
from sqlalchemy import Enum

class PublicationStatusEnum(enum.Enum):
    BORRADOR: 1
    PUBLICADO: 2
    ARCHIVADO: 3

class Publication(db.Model):
    __tablename__ = 'publications'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    status = db.Column(Enum(PublicationStatusEnum), nullable=False)
    published_date = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, default=datetime.now())
    updated_date = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self):
        return f"<Publicacion: {self.title}>"