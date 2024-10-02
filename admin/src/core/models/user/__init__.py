from datetime import datetime, timezone
from src.core.database import db
from core.admin_data import AdminData

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'))
    alias = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)  
    
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    empleado = db.relationship('Empleado', backref='users')
    role = db.relationship('Role', backref='users')  
    
    def __repr__(self):
        email = self.empleado.email if self.empleado else 'Sin email'
        return f'<User alias={self.alias}, email={email}, activo={self.activo}, rol={self.role.name}, created_at={self.created_at}, updated_at={self.updated_at}>'

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.empleado.email if self.empleado else 'Sin email',
            'alias': self.alias,
            'activo': self.activo,
            'role': self.role.name, 
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
