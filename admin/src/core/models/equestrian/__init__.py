from datetime import datetime, timezone
from core.enums.equestrian_enum import SexoEnum, TipoClienteEnum
from src.core.database import db


# Representa la tabla intermedia de la relacion muchos a muchos entre empleado y ecuestre
class Associated (db.Model):
   """Representa un asociado """
   __tablename__ = 'associates'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   employee_id =  db.Column('employee_id',db.Integer, db.ForeignKey('employees.id'), primary_key=True) 
   equestrian_id = db.Column('equestrian_id', db.Integer, db.ForeignKey('equestrians.id'), primary_key=True)
   deleted = db.Column('activo', db.Boolean, default=True)

   employee = db.relationship('Employee', back_populates='equestrians_asociados')
   equestrian = db.relationship('Equestrian', back_populates='empleados_asociados')

   created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
   updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

   def __repr__(self):
        return f"""Asociado: 
            empleado id: {self.employee_id},
            ecuestre id: {self.equestrian_id},
            activo: {self.activo},
           """
   
   def to_dict(self):
        """Convierte la instancia de la relacion associates a un diccionario."""
        return{
            "id": self.id,
            "employee_id": self.employee_id,
            "equestrian_id": self.equestrian_id,
            "activo": self.activo
       }
           
        

   
 
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

    empleados_asociados =  db.relationship('Associated',back_populates='equestrian')
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
            "sexo": self.sexo.name.capitalize(),
            "raza": self.raza,
            "pelaje": self.pelaje,
            "compra": compra,
            "fecha_nacimiento": self.fecha_nacimiento.strftime("%d-%m-%Y"),
            "fecha_ingreso": self.fecha_ingreso.strftime("%d-%m-%Y"),
            "sede_asignada": self.sede_asignada,
            "tipo_de_jya_asignado": self.tipo_de_jya_asignado.name.capitalize()
        }
  
