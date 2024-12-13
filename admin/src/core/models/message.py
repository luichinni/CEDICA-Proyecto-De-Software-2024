from datetime import datetime, timezone
from core.enums.message import StatuEnum
from src.core.database import db
 
class Message (db.Model):
   """Representa un Mensaje """
   __tablename__ = 'Messages' 
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   title= db.Column(db.String(50), nullable=False)
   email =  db.Column(db.String(50), nullable=False)
   description= db.Column(db.Text, nullable=False)
   status = db.Column(db.Enum(StatuEnum), nullable=False)

   comentario = db.Column(db.Text, nullable=False, default= "NA")

   closed_at= db.Column(db.DateTime, nullable=True)#FECHA EN LA QUE SE CERRO EL MENSAJE

   created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
   updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

   deleted = db.Column(db.Boolean, nullable=False, default=False)

   def __repr__(self):
        return f"""Mensaje: 
            id: {self.id},
            title: {self.title},
            email: {self.email},
            description: {self.description},
            status:{self.status},
            comentario:{self.comentario},
            closet_at:{self.closed_at}
           """
   
   def to_dict(self):
        """Convierte la instancia de la relacion associates a un diccionario."""
        return{
            "id": self.id,
            "Titulo": self.title,
            "Email": self.email,
            "Description": self.description,
            "Estado":self.status.name.capitalize(),
            "Comentario":self.comentario,
            "Fecha de cierre":self.closed_at
       }
           
        

   
 