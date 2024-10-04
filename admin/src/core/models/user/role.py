from datetime import datetime, timezone
from src.core.database import db

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    permissions = db.relationship('RolePermission', back_populates='role') 
    
    def __repr__(self):
        return f'<Role {self.name}, created_at={self.created_at}, updated_at={self.updated_at}>'
