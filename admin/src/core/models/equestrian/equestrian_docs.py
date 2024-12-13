from datetime import datetime, timezone

from sqlalchemy import Enum

from core.enums.equestrian_enum import TipoEnum
from src.core.database import db


class EquestrianDocument(db.Model):
    """Representa el documento adicional que posee el ecuestre"""
    __tablename__ = 'additional_documents'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(60), nullable=False)
    tipo = db.Column(Enum(TipoEnum), nullable=False)
    ubicacion = db.Column(db.String(255), nullable=False)
    es_link = db.Column(db.Boolean, default=False)

    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    equestrian_id = db.Column(db.Integer, db.ForeignKey('equestrians.id'), nullable=False)
    equestrian = db.relationship('Equestrian', back_populates='equestrian_documents', uselist=False)

    def __repr__(self):
        return f"documento adicional: {self.titulo},  tipo: {self.tipo}, ubicacion: {self.ubicacion}, es link: {self.es_link}"

    def to_dict(self):
        """Convierte la instancia del documento adicional a un diccionario."""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "tipo": self.tipo.value,
            "ubicacion": self.ubicacion,
            "es_link": self.es_link,
            "created_at": self.created_at.isoformat(),

        }
