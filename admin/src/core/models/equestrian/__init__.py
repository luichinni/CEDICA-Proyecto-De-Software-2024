from datetime import datetime, timezone
from core.enums.equestrian_enum import SexoEnum, TipoClienteEnum
from src.core.database import db


# Representa la tabla intermedia de la relacion muchos a muchos entre empleado y ecuestre
associates= db.Table('associates',
    db.Column('employee_id',db.Integer, db.ForeignKey('employees.id'), primary_key=True) ,
    db.Column('equestrian_id', db.Integer, db.ForeignKey('equestrians.id'), primary_key=True),
    extend_existing=True
)
 
class Equestrian (db.Model):
    """Representa un ecuestre """
    __tablename__ = 'equestrians'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    sexo = db.Column(db.Enum(SexoEnum), nullable=False)
    raza = db.Column(db.String(50), nullable=False)
    pelaje = db.Column(db.String(50), nullable=False)
    compra = db.Column(db.Boolean, default=False)
    fecha_nacimiento =  db.Column(db.DateTime, nullable=False)
    fecha_ingreso = db.Column(db.DateTime, nullable=False)
    sede_asignada = db.Column(db.String(50), nullable=False)
    tipo_de_jya_asignado = db.Column(db.Enum(TipoClienteEnum), nullable=False)
    
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    empleados_asociados = db.relationship('Employee',secondary=associates,back_populates='equestrians_asociados')
    equestrian_documents = db.relationship('EquestrianDocument', back_populates='equestrian')

    def __repr__(self):
        return f"""Ecuestre: 
            'nombre': {self.nombre},
            sexo: {self.sexo.value},
            raza: {self.raza},
            pelaje: {self.pelaje},
            compra: {self.compra},
            fecha_ingreso: {self.fecha_ingreso},
            fecha_nacimiento:{self.fecha_nacimiento}
            sede_asignada: {self.sede_asignada},
            tipo_de_jya_asignado: {self.tipo_de_jya_asignado.value}"""

    def to_dict(self):
        """Convierte la instancia del ecuestre a un diccionario."""
        if self.compra :
           compra = ' comprado '
        else: 
           compra= 'donado'
        return {
            "id": self.id,
            "nombre": self.nombre,
            "sexo": self.sexo.value,
            "raza": self.raza,
            "pelaje": self.pelaje,
            "compra": compra,
            "fecha_nacimiento": self.fecha_nacimiento.isoformat(),
            "fecha_ingreso": self.fecha_ingreso.isoformat(),
            "sede_asignada": self.sede_asignada,
            "tipo_de_jya_asignado": self.tipo_de_jya_asignado.value
        }
  
