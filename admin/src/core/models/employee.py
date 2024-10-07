from datetime import datetime, timezone
from src.core.database import db

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    email = db.Column(db.String(50), nullable=False) 
    
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))  
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)) 
    
    def __repr__(self):
        return f'<Permission {self.email}, created_at={self.created_at}, updated_at={self.updated_at}>'

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }