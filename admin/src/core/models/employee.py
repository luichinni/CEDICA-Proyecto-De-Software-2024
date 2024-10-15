from src.core.database import db
import enum
from sqlalchemy import Enum

class ProfesionEnum(enum.Enum):
    PSICOLOGO = 1
    PSICOMOTRICISTA = 2
    MEDICO = 3
    KINESIOLOGO = 4
    TERAPISTA_OCUPACIONAL= 5
    PSICOPEDAGOGO = 6
    DOCENTE = 7
    PROFESOR = 8
    FONOAUDIOLOGO = 9
    VETERINARIO = 10
    OTRO = 11

class CondicionEnum(enum.Enum):
    VOLUNTARIO = 1
    PERSONAL_RENTADO = 2

class PuestoLaboralEnum(enum.Enum):
    ADMINISTRATIVO = 1
    TERAPEUTA = 2
    CONDUCTOR = 3
    AUXILIAR_DE_PISTA = 4
    HERRERO = 5
    VETERINARIO = 6
    ENTRENADOR_DE_CABALLOS = 7
    DOMADOR = 8
    PROFESOR_DE_EQUITACIÓN = 9
    DOCENTE_DE_CAPACITACIÓN = 10
    AUXILIAR_DE_MANTENIMIENTO = 11
    OTRO = 12

class Employee(db.Model):
    """Representa un miembro del equipo de CEDICA"""
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(8), unique=True, nullable=False)
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

    def to_dict(self):
        """Convierte la instancia del empleado a un diccionario."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "domicilio": self.domicilio,
            "email": self.email,
            "localidad": self.localidad,
            "telefono": self.telefono,
            "profesion": self.profesion.value,
            "puesto_laboral": self.puesto_laboral.value,
            "fecha_inicio": self.fecha_inicio,
            "fecha_cese": self.fecha_cese,
            "contacto_emergencia_nombre": self.contacto_emergencia_nombre,
            "contacto_emergencia_telefono": self.contacto_emergencia_telefono,
            "obra_social": self.obra_social,
            "numero_afiliado": self.numero_afiliado,
            "condicion": self.condicion,
            "activo": self.activo,
        }