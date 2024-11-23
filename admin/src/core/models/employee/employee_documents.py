from datetime import datetime, timezone
from src.core.database import db
from src.core.enums.employee_enum.tipo_doc import TipoDoc


class EmployeeDocuments(db.Model):
    __tablename__ = "employee_documents"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.Enum(TipoDoc), nullable=False)
    ubicacion = db.Column(db.Text, nullable=False)
    es_link = db.Column(db.Boolean, nullable=False)

    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    employee = db.relationship('Employee', back_populates='archivos')

    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<EmployeeDocument id={self.id} titulo={self.titulo}>"

    def to_dict(self):
        return {
            "id": self.id,
            'titulo': self.titulo,
            'tipo': self.tipo,
            'es_link': self.es_link,
            'ubicacion': self.ubicacion,
            "created_at": self.created_at,
        }