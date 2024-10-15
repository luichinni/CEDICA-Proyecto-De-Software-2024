from datetime import datetime, timezone
from src.core.database import db

class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dni = db.Column(db.String(50), nullable=False) 

    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))  
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)) 
    deleted = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"<Client id={self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            'dni': self.dni,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
