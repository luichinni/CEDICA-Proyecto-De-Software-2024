from src.core.database import db
from datetime import datetime, timezone
import enum
from sqlalchemy import Enum


class TipoEnum(enum.Enum):
   FICHA_GENERAL_DEL_CABALLO = 1
   PLANIFICACION_DE_ENTRENAMIENTO = 2
   INFORME_DE_EVOLUCION = 3
   CARGA_DE_IMAGENES = 4
   REGISTRO_VETERINARIO = 5


class DocumentAdditional (db.Model):
    """Representa el documento adicional que posee el ecuestre"""
    __tablename__ ='additional_documents'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre =db.Column(db.string(60), nullable= False)
    tipo = db.Column(Enum(TipoEnum), nullable=False)
    ruta = db.Column(db.String(255), nullable=False) 
    es_link = db.column( db.Boolean, defaul= False)

    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    equestrian_id = db.column(db.Integer, db.ForeignKey('equestrians.id'), nullable=False)
    equestrian =  db.relationship('Equestrian', back_populates='additional_documents', uselist=False)
    
    def __repr__(self):
        return f"documento adicional: {self.nombre},  tipo: {self.tipo}, ruta: {self.ruta}, es link: {self.es_link}"

    def to_dict(self):
        """Convierte la instancia del documento adicional a un diccionario."""
        return {
            "id": self.id,
            "tipo": self.tipo.value,
            "ruta": self.ruta,
            "es_link": self.es_link,
             
        }