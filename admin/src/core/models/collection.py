from datetime import datetime, timezone
from src.core.database import db
import enum

class PaymentMethod(enum.Enum):
    CASH = "Efectivo"
    CREDIT_CARD = "Tarjeta de Crédito"
    DEBIT_CARD = "Tarjeta de Débito"
    TRANSFER = "Transferencia"
    OTHER = "Otro"

    @classmethod
    def from_value(cls, value):
        for method in cls:
            if method.value == value:
                return method
        raise ValueError(f"No se encontró un método de pago con el valor: {value}")

class Collection(db.Model):
    __tablename__ = 'collections'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    employee = db.relationship('Employee', backref='collections')

    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship('Clients', backref='collections')

    payment_date = db.Column(db.DateTime, nullable=False)
    payment_method = db.Column(db.Enum(PaymentMethod), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    observations = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))  
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)) 
    deleted = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"<Collection id={self.id}, employee_id={self.employee_id}, client_id={self.client_id}, amount={self.amount}, payment_method={self.payment_method.value}>"

    def to_dict(self):
        return {
            "id": self.id,
            "Nombre del empleado": self.employee.nombre if self.employee and self.employee.nombre else "Sin Nombre",
            "Apellido del empleado": self.employee.apellido if self.employee and self.employee.apellido else "Sin apellido",
            "Email del empleado": self.employee.email if self.employee and self.employee.email else "Sin empleado asignado",
            "Dni del cliente": self.client.dni if self.client and self.client.dni else "Sin cliente asignado",
            "Fecha de pago": self.payment_date.strftime('%Y-%m-%d'),
            "Metodo de pago": self.payment_method.value,
            "Monto": self.amount,
            "Observaciones": self.observations,
            #"created_at": self.created_at.isoformat(),
            #"updated_at": self.updated_at.isoformat()
        }
