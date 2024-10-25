from datetime import datetime, timezone
from src.core.database import db 
from src.core.models.equestrian import Equestrian
from src.core.models.equestrian import SexoEnum
from src.core.models.equestrian import TipoClienteEnum

class EquestrianService :
    
    @staticmethod 
    def ensure_datetime(fecha_ingreso): 
        if isinstance(fecha_ingreso, datetime):
           return fecha_ingreso
        elif isinstance(fecha_ingreso, str):
            try:
                 return datetime.strptime(fecha_ingreso, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            except ValueError:
                   raise ValueError("La fecha ingresada no es válida, debe estar en formato YYYY-MM-DD.")
        else:
            raise TypeError("La fecha ingresada debe ser un objeto datetime o una cadena.")

    @staticmethod
    def validate_date(fecha_ingreso):
        fecha_ingreso = EquestrianService.ensure_datetime(fecha_ingreso)
        return fecha_ingreso <= datetime.now(timezone.utc) 
    
    @staticmethod
    def validar_arguments(**kwargs):
        """Valida que los parametros sean correctos para ecuestre"""
        dic = dict(**kwargs)
        sexo = kwargs.get('sexo')
        if sexo is not None and EquestrianService.es_enum_valido(sexo, SexoEnum ) :
            del dic['sexo']
       
        compra= kwargs.get('compra') 
        if compra is not None and EquestrianService.is_instance_with_exception(compra, bool):
            del dic['compra']

        fecha_ingreso = kwargs.get('fecha_ingreso')
        if fecha_ingreso is not None and EquestrianService.validate_date(fecha_ingreso):
            del dic['fecha_ingreso'] 

        tipo_cliente = kwargs.get('tipo_cliente') 
        if tipo_cliente is not None and  EquestrianService.es_enum_valido(tipo_cliente, TipoClienteEnum):
            del dic['tipo_cliente']

        for key, value in dic.items(): 
            if value is not None :
               EquestrianService.is_instance_with_exception(value, str)
                
        return True

    @staticmethod
    def add_equestrian(**kwargs):
        """Crea un ecuestre"""
        if EquestrianService.validar_arguments(**kwargs) :
           equestrian = Equestrian(**kwargs)    
        db.session.add(equestrian)
        db.session.commit()
        return equestrian
    
    @staticmethod
    def delete_equestrian (equestrian_id):
        """Elimina un ecuestre de manera logica"""
        equestrian = EquestrianService.get_equestrian_by_id(equestrian_id)
        equestrian.deleted = True
        db.session.commit()
        return equestrian
    
    @staticmethod
    def es_enum_valido(valor , enum):
       if not valor in enum.__members__ : 
            raise ValueError(f"No existe la clasificacion {valor} para ecuestre")
      
       return True

    def is_instance_with_exception(valor,tipo):
        if not isinstance(valor, tipo):
            raise ValueError(f" El {valor} no es de tipo {tipo}")
        return True

    @staticmethod
    def update_equestrian(equestrian_id, **kwargs):
        """Actualiza un ecuestre"""
        equestrian = EquestrianService.get_equestrian_by_id(equestrian_id)
        
        if EquestrianService.validar_arguments(**kwargs):
           for key, value in kwargs.items(): 
               if value is not None and getattr(equestrian, key) != value :
                  setattr(equestrian, key, value) 
        
        db.session.commit()
        return equestrian
    
    @staticmethod
    def get_all_equestrian (page=1, per_page=25, include_deleted=False):
        """Lista todos los cobros"""
        query = Equestrian.query
        if not include_deleted:
            query = query.filter_by(deleted=False)
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return pagination.items, pagination.total, pagination.pages
    
    @staticmethod
    def get_equestrian_by_id(equestrian_id, include_deleted=False)-> Equestrian:
        """Obtiene un cobro por su ID"""
        query = Equestrian.query.filter_by(id=equestrian_id)
        if not include_deleted:
            query = query.filter_by(deleted=False)
        equestrian = query.first()
        if not equestrian:
            raise ValueError(f"No existe el ecuestre con ID: {equestrian}")
        return equestrian
    

    @staticmethod
    def search_equestrian(filtro: dict = None, page: int = 1, per_page: int = 25, order_by: str = None, ascending: bool = True, include_deleted: bool = False, like:bool = False) -> tuple:
        """Lista los ecuestres segun los filtros especificados, en caso de no especificar retorna los primeros 25 ecuestres

        Args:
            filtro (dict, optional): Diccionario de { campo: valor_esperado } para filtrar. Defaults to None.
            page (int, optional): Nro de pagina esperada. Defaults to 1.
            per_page (int, optional): Cantidad de resultados por pagina. Defaults to 25.
            order_by (str, optional): Campo para ordenar. Defaults to None.
            ascending (bool, optional): Flag de ordenamiento asc o desc. Defaults to True.
            include_deleted (bool, optional): Flag de inclusión eliminados. Defaults to False.
            like (bool, optional): Flag de busqueda parcial en strings. Defaults to False.

        Returns:
            list: Listado de clientes obtenidos a partir de la busqueda
        """
        query = Equestrian.query.filter_by(deleted=include_deleted)
        
        if filtro:
            for key, value in filtro.items():
                if hasattr(Equestrian, key) and value is not None:
                    if isinstance(value, str) and like:
                        query = query.filter(getattr(Equestrian, key).like(f'%{value}%'))
                    else:
                        query = query.filter_by(**{key: value})

        if order_by:
            if ascending:
                query = query.order_by(getattr(Equestrian, order_by).asc())
            else:
                query = query.order_by(getattr(Equestrian, order_by).desc())
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.total, pagination.pages
