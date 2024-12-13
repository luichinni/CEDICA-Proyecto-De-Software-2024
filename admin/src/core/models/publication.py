import enum
from datetime import datetime, timezone

from sqlalchemy import Enum

from src.core.database import db


class PublicationStatusEnum(enum.Enum):
    BORRADOR = 1
    PUBLICADO = 2
    ARCHIVADO = 3


class Publication(db.Model):
    __tablename__ = 'publications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    status = db.Column(Enum(PublicationStatusEnum, name='status_type'), nullable=False)
    published_date = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_date = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Publicacion: {self.title}>"

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.title,
            "copete": self.summary,
            "contenido": self.content,
            "autor": self.author,
            "estado": self.status.name.capitalize(),
            "fecha de publicacion": self.published_date.strftime("%d-%m-%Y"),
            "fecha de creacion": self.created_date.strftime("%d-%m-%Y"),
            "fecha de modificacion": self.updated_date if self.updated_date else 'No tiene'
        }
