from datetime import datetime, timezone
from src.core.database import db
from src.core.enums.client_enum import * # solo hay enums

class ClientDocuments(db.Model):
    __tablename__ = "client_documents"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    """
    título, fecha en la que se agregó el enlace, tipo
    """
    titulo = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.Enum(TipoDocs), nullable=False)
    ubicacion = db.Column(db.Text, nullable=False)
    es_link = db.Column(db.Boolean, nullable=False)
    
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    cliente = db.relationship('Clients', back_populates='archivos')
    
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    deleted = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"<ClientDocument id={self.id} titulo={self.titulo}>"

    def to_dict(self):
        return {
            "id": self.id,
            'titulo': self.titulo,
            'tipo': self.tipo,
            'ubicacion':self.ubicacion,
            "created_at": self.created_at.isoformat(),
        }