from datetime import date, datetime, timedelta, timezone
from src.core.models.message import Message
from core.enums.message import StatuEnum
from sqlalchemy import Enum
from src.core.database import db 
import re 
from dateutil import parser

class MessageService :
    @staticmethod 
    def validate_email(email):
       patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
       return re.match(patron, email) is not None

    @staticmethod
    def ensure_datetime(fecha_ingreso): 
        if isinstance(fecha_ingreso, str):
            try:
                print("llega a la fecha")
                return parser.isoparse(fecha_ingreso.replace(" ", ""))
                
            except ValueError:
                raise ValueError("La fecha ingresada no es válida, debe estar en formato YYYY-MM-DD.")
        elif isinstance(fecha_ingreso, datetime) : 
            print("llega al reutnr")
            return fecha_ingreso
        else:
            raise TypeError("La fecha ingresada debe ser un objeto datetime o una cadena.")
    
    
    @staticmethod
    def es_enum_valido(valor , enum):
       if not valor in enum.__members__ : 
            raise ValueError(f"No existe la clasificacion {valor} para mensaje")
      
       return True

    def is_instance_with_exception(valor,tipo):
        if not isinstance(valor, tipo):
            raise ValueError(f" El {valor} no es de tipo {tipo}")
        return True

        
    @staticmethod
    def validar_arguments(**kwargs):
        """Valida que los parametros sean correctos para mensaje"""
        dic = dict(**kwargs)
        email= kwargs.get('email')
        if email is not None and MessageService.validate_email(email) :
            del dic['email']

        status = kwargs.get('status') 
        if status is not None and  MessageService.es_enum_valido(status, StatuEnum):
            del dic['status']
        for value in dic.values(): #verifica que sean str title, description, coments(si exist)
            if value is not None :
               MessageService.is_instance_with_exception(value, str)
                
        return True
    
    @staticmethod 
    def add_message(**kwargs): 
       """Crea un mensaje"""
       print("en el add")
       if MessageService.validar_arguments(**kwargs) :
           message = Message(**kwargs)    
       db.session.add(message)
       db.session.commit()
       return message

    @staticmethod 
    def delete_menssage(message_id): 
       """Elimina un mensaje de manera logica"""
       message = MessageService.get_message_by_id(message_id)
       message.deleted = True
       db.session.commit()
       return message

    @staticmethod 
    def update_message(message_id, **kwargs):
        """Actualiza un mensaje"""
        message = MessageService.get_message_by_id(message_id)
        
        if MessageService.validar_arguments(**kwargs):
           for key, value in kwargs.items(): 
               if value is not None and getattr(message, key) != value :
                  setattr(message, key, value) 
                  if key == 'status' and (value.upper() == StatuEnum.ACEPTED.name or value.upper() == StatuEnum.REJECTED.name):
                     message.closed_at = datetime.now(timezone.utc)
        db.session.commit()
        return message

    @staticmethod 
    def get_message_by_id(message_id, include_deleted=False)-> Message: 
        """Obtiene un mensaje por su ID"""
        query = Message.query.filter_by(id=message_id)
        if not include_deleted:
            query = query.filter_by(deleted=False)
        message = query.first()
        if not message:
            raise ValueError(f"No existe el mensaje con ID: {message_id}")
        return message

    @staticmethod
    def get_messages(filtro: dict = None, page: int = 1, per_page: int = 5, order_by: str = None, ascending: bool = True, include_deleted: bool = False, like:bool = False) -> tuple:
        """Listado de mensajes"""
        query = Message.query
        
        if not include_deleted:
            query = query.filter_by(deleted=include_deleted)
        
        if filtro:
            for key, value in filtro.items():
                if hasattr(Message, key) and value is not None:
                    if isinstance(value, str) and not issubclass(getattr(Message, key).type.python_type, Enum) and like:
                        query = query.filter(getattr(Message, key).like(f'%{value}%'))
                    else:
                        query = query.filter_by(**{key: value})

        if order_by:
            if ascending:
                query = query.order_by(getattr(Message, order_by).asc())
            else:
                query = query.order_by(getattr(Message, order_by).desc())
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.total, pagination.pages

