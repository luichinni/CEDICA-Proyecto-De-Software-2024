from datetime import datetime
from src.core.database import db

class UserPermission(db.Model):
    __tablename__ = 'user_permissions'  

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)  
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), primary_key=True)  

    created_at = db.Column(db.DateTime, default=datetime.now(datetime.timezone.utc))  
    updated_at = db.Column(db.DateTime, default=datetime.now(datetime.timezone.utc), onupdate=datetime.now(datetime.timezone.utc)) 
    
    user = db.relationship('User', backref='user_permissions')
    permission = db.relationship('Permission', backref='user_permissions')

    def __repr__(self):
        return f'<UserPermission user_id={self.user_id}, permission_id={self.permission_id}>'
