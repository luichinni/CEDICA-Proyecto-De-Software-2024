from datetime import datetime
from src.core.database import db

class Permission(db.Model):
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    name = db.Column(db.String(50), nullable=False) 
    
    created_at = db.Column(db.DateTime, default=datetime.now(datetime.timezone.utc))  
    updated_at = db.Column(db.DateTime, default=datetime.now(datetime.timezone.utc), onupdate=datetime.now(datetime.timezone.utc)) 
    
    def __repr__(self):
        return f'<Permission {self.name}, created_at={self.created_at}, updated_at={self.updated_at}>'
