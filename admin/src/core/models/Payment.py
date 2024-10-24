from src.core.database import db
from datetime import datetime, timezone
from enum import Enum

class PaymentEnum(Enum):
    HONORARIOS = 1
    PROVEEDOR = 2
    GASTOS_VARIOS = 3

class Payment(db.Model):
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    beneficiario_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    monto = db.Column(db.Float, nullable=False)
    fecha_pago = db.Column(db.Date, nullable=False, default=datetime.now())
    tipo_pago = db.Column(db.Enum(PaymentEnum), nullable=False)
    descripcion = db.Column(db.String, nullable=False)
    empleado = db.relationship('Employee', backref='payments')
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def __repr__(self):
        return f"Pago: {self.tipo_pago.name} - {self.monto} on {self.fecha_pago}"

    def to_dict(self):
        return {
            "id": self.id,
            "beneficiario_id": self.beneficiario_id,
            "monto": self.monto,
            "fecha_pago": self.fecha_pago,
            "tipo_pago": self.tipo_pago,
            "descripcion": self.descripcion,
            "empleado": self.empleado,
        }