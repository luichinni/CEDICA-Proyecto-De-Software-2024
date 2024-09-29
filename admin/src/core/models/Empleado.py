from src.core.database import db
from enum import Enum
from src.core.enums.equipo import ProfesionEnum
from src.core.enums.equipo import PuestoLaboralEnum
from src.core.enums.equipo import CondicionEnum


class Empleado(db.Model):
    """Representa un miembro del equipo de CEDICA"""
    __tablename__ = 'Empleado'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(50), unique=True, nullable=False)
    domicilio = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    localidad = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    profesion = db.Column(Enum(ProfesionEnum), nullable=False)
    puesto_laboral = db.Column(Enum(PuestoLaboralEnum), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_cese = db.Column(db.Date, nullable=True)
    contacto_emergencia = db.Column(db.String(100), nullable=False)
    obra_social = db.Column(db.String(100), nullable=True)
    nro_afiliado = db.Column(db.String(50), nullable=False)
    condicion = db.Column(Enum(CondicionEnum), nullable=False)
    activo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"Empleado {self.nombre} {self.apellido}"
