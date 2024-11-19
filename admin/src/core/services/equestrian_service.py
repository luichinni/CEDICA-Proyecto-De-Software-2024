from datetime import date, datetime, timedelta, timezone
from core.enums.client_enum import ExtensionesPermitidas
from core.services.employee_service import EmployeeService
from sqlalchemy import Enum
from src.core.database import db 
from src.core.models.equestrian import Associated, Equestrian
from src.core.models.equestrian import SexoEnum
from src.core.models.equestrian import TipoClienteEnum
from src.core.models.equestrian.equestrian_docs import EquestrianDocument, TipoEnum
from urllib.parse import urlparse
from src.core.storage import storage
from os import path 

class EquestrianService :
    
    @staticmethod 
    def ensure_datetime(fecha_ingreso): 
        if isinstance(fecha_ingreso, datetime):
           return fecha_ingreso
        elif isinstance(fecha_ingreso, date): 
           return datetime(fecha_ingreso.year, fecha_ingreso.month, fecha_ingreso.day, tzinfo=timezone.utc)
        elif isinstance(fecha_ingreso, str):
            try:
                 return datetime.strptime(fecha_ingreso, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            except ValueError:
                   raise ValueError("La fecha ingresada no es válida, debe estar en formato YYYY-MM-DD.")
        else:
            raise TypeError("La fecha ingresada debe ser un objeto datetime o una cadena.")

    @staticmethod
    def validate_date(fecha_nacimiento):
        fecha_nacimiento = EquestrianService.ensure_datetime(fecha_nacimiento)
        return fecha_nacimiento <= datetime.now(timezone.utc) 
    
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
        if fecha_ingreso is not None and EquestrianService.ensure_datetime(fecha_ingreso):
             del dic['fecha_ingreso']

        fecha_nacimiento = kwargs.get('fecha_nacimiento')
        if fecha_nacimiento is not None and EquestrianService.validate_date(fecha_nacimiento):
            del dic['fecha_nacimiento']

        tipo_cliente = kwargs.get('tipo_cliente') 
        if tipo_cliente is not None and  EquestrianService.es_enum_valido(tipo_cliente, TipoClienteEnum):
            del dic['tipo_cliente']
        print(dic)
        for value in dic.values(): 
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
    def get_all_equestrian (page=1, per_page=5, include_deleted=False):
        """Lista todos los ecuestres"""
        query = Equestrian.query
        if not include_deleted:
            query = query.filter_by(deleted=False)
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return pagination.items, pagination.total, pagination.pages
    
    @staticmethod
    def get_equestrian_by_id(equestrian_id, include_deleted=False)-> Equestrian:
        """Obtiene un ecuestre por su ID"""
        query = Equestrian.query.filter_by(id=equestrian_id)
        if not include_deleted:
            query = query.filter_by(deleted=False)
        equestrian = query.first()
        if not equestrian:
            raise ValueError(f"No existe el ecuestre con ID: {equestrian_id}")
        return equestrian
    

    @staticmethod
    def search_equestrian(filtro: dict = None, page: int = 1, per_page: int = 5, order_by: str = None, ascending: bool = True, include_deleted: bool = False, like:bool = False) -> tuple:
        """Lista los ecuestres segun los filtros especificados, en caso de no especificar retorna los primeros 5 ecuestres

        Args:
            filtro (dict, optional): Diccionario de { campo: valor_esperado } para filtrar. Defaults to None.
            page (int, optional): Nro de pagina esperada. Defaults to 1.
            per_page (int, optional): Cantidad de resultados por pagina. Defaults to 5.
            order_by (str, optional): Campo para ordenar. Defaults to None.
            ascending (bool, optional): Flag de ordenamiento asc o desc. Defaults to True.
            include_deleted (bool, optional): Flag de inclusión eliminados. Defaults to False.
            like (bool, optional): Flag de busqueda parcial en strings. Defaults to False.

        Returns:
            list: Listado de ecuestres obtenidos a partir de la busqueda
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

    @staticmethod
    def obtener_clave_por_valor(enum_class: Enum, valor):
        """Retorna la Key segun el valor asociado del enum

        Args:
            enum_class (Enum): Enumerable a analizar
            valor (Any): Clave a buscar

        Returns:
            (Any | None): Valor de la clave si es encontrado, sino None
        """
        if not (valor in enum_class):
            return None
        
        for valor_enum in enum_class:
            if valor == valor_enum.value:
                return valor_enum.name



    @staticmethod
    def add_document(equestrian_id: int | str, titulo:str, document, tipo: TipoEnum, es_link: bool) -> EquestrianDocument:
        """Permite cargarle un documento o link a un ecuestre

        Args:
            equestrian_id (int | str): ID del ecuestre al que se le añadirá el document
            document (Any): Documento o link a agregar
            tipo (TipoEnum): Tipo del documento
            es_link (bool): Flag de confirmación si es link

        Returns:
           EquestrianDocument: Retorna el objeto con la información del archivo guardado
        """
        ecuestre = EquestrianService.get_equestrian_by_id(equestrian_id)
        
        ubicacion_archivo = ""
        nombre_archivo = ""
        
        if (int(tipo) not in TipoEnum):
            raise ValueError("Tipo de documento no es válido")
        
        if es_link:
            ubicacion_archivo = document # si es link, seria la url
            url_parseada = urlparse(document)
            nombre_archivo = url_parseada.hostname if url_parseada.hostname is not None else url_parseada.netloc # puede tomar por ej: drive.google.com o drive.google.com:port
            nombre_archivo = "Archivo de \"" + nombre_archivo + "\"" if not titulo else titulo # ej: Archivo de "drive.google.com"
            
        else:
            last_file = ecuestre.equestrian_documents
            last_id = 1
            
            if last_file:
                ultimo_documento = (
                    db.session.query(EquestrianDocument)
                    .filter(EquestrianDocument.equestrian_id == ecuestre.id)
                    .order_by(EquestrianDocument.id.desc())
                    .first()
                )
                last_id = ultimo_documento.id + 1
            
            nombre_archivo = str(ecuestre.id) + '_' + str(last_id) + '_' + (document.filename if not titulo else titulo.replace(' ','_')+path.splitext(document.filename)[1])  
            # 1234_4_fotocopiadni.pdf o con titulo 44130359_4_titulo_agregado.pdf
            ubicacion_archivo = 'equestrian_files/' + nombre_archivo  # ej: equestrian_files/1234_4_fotocopiadni.pdf o 1234_4_titulo_agregado.pdf
            
            
            try:
                result = storage.client.put_object("grupo23",ubicacion_archivo,document.stream,length=-1, part_size=5 * 1024 * 1024)
                print("!subido!" , result)
            except:
                raise ValueError("Hubo un problema al cargar el archivo, intenta nuevamente")
        
        new_file = EquestrianDocument(
                titulo=nombre_archivo, 
                tipo=EquestrianService.obtener_clave_por_valor(TipoEnum,int(tipo)), 
                ubicacion=ubicacion_archivo, 
                es_link=es_link,
                equestrian_id=equestrian_id  )

        db.session.add(new_file)
        db.session.commit()
        
        return new_file
    
    @staticmethod
    def get_document(id:int):
        archivo = EquestrianDocument.query.get(id)
        if archivo.es_link:
            url = archivo.ubicacion
        else:
            formatos = {ext.name:ext.value for ext in ExtensionesPermitidas}
            headers = {"response-content-type": formatos[path.splitext(archivo.ubicacion)[1][1:].upper()]}  # Cambia según el archivo
            url = storage.client.presigned_get_object('grupo23',archivo.ubicacion,expires=timedelta(hours=1),response_headers=headers)
        
        return url
    @staticmethod
    def get_document_by_id(id: int)-> EquestrianDocument:
        """Obtiene un ecuestre por su ID"""
        archivo=  EquestrianDocument.query.get(id)
         
        if not archivo:
            raise ValueError(f"No existe el documento con ID: {id}")
        return archivo
    

    def get_documents(equestrian_id: int | str, filtro: dict = None, extension: str = None, page: int = 1, per_page: int = 5, order_by: str = None, ascending: bool = True, include_deleted: bool = False, like: bool = False):
        """
        Obtiene por página y filtro los documentos de un ecuestre específico.

        Args:
            equestrian_id (int | str): ID del cliente cuyos documentos son requeridos.
            filtro (dict, optional): Diccionario de filtros para los archivos. Defaults to None.
            page (int, optional): Número de página requerida. Defaults to 1.
            per_page (int, optional): Cantidad de archivos por página. Defaults to 5.
            order_by (str, optional): Campo de orden para los elementos. Defaults to None.
            ascending (bool, optional): Flag de datos ascendentes o descendentes. Defaults to True.
            include_deleted (bool, optional): Flag de inclusión de archivos con borrado lógico. Defaults to False.
            like (bool, optional): Flag de búsqueda parcial en strings. Defaults to False.
        """
        if isinstance(equestrian_id,str):
            equestrian_id = int(equestrian_id)
        
        query = EquestrianDocument.query.filter(EquestrianDocument.equestrian_id == equestrian_id, EquestrianDocument.deleted == include_deleted)

        if filtro:
            for key, value in filtro.items():
                if hasattr(EquestrianDocument, key) and value is not None:
                    if isinstance(value, str) and like:
                        query = query.filter(getattr(EquestrianDocument, key).like(f'%{value}%'))
                    else:
                        query = query.filter(getattr(EquestrianDocument, key) == value)
                    
        if extension:
            extension = extension.lower()
            if extension != 'link':
                query = query.filter(EquestrianDocument.ubicacion.like(f'%.{extension}'))
            elif extension == 'link':
                query = query.filter_by(es_link=True)

        if order_by and hasattr(EquestrianDocument, order_by):
            if ascending:
                query = query.order_by(getattr(EquestrianDocument, order_by).asc())
            else:
                query = query.order_by(getattr(EquestrianDocument, order_by).desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return pagination.items, pagination.total, pagination.pages
    
    @staticmethod
    def delete_document(docs_id: int | str):
        """Eliminación lógica de un documento o link en particular

        Args:
            docs_id (int | str): ID del documento o link a dar de baja
        """
        document = EquestrianDocument.query.get(docs_id)
        if not document :
            raise ValueError(f'No existe el ecuestre con id: {docs_id}')
        document.deleted = True
        db.session.commit()
    @staticmethod
    def update_document(document_id: int | str, titulo:str, tipo: TipoEnum, url:str, es_link: bool) -> EquestrianDocument:
        """Permite actualizar un documento o link a un ecuestre

        Args:
            document_id (int | str): ID del documento al que se actualizará
            titulo (Any): titulo nuevo para documento
            tipo (TipoDocs): Tipo del documento
            url (str): url actualizada
            es_link (bool): Flag de confirmación si es link

        Returns:
            EquestrianDocuments: Retorna el objeto con la información del archivo guardado
        """
        archivo = EquestrianService.get_document_by_id(document_id)
        
        ubicacion_archivo = url
        nombre_archivo = titulo
        
        if (int(tipo) not in TipoEnum):
            raise ValueError("Tipo de documento no es válido")
        
        if es_link:
            url_parseada = urlparse(ubicacion_archivo)
            nombre_archivo = url_parseada.hostname if url_parseada.hostname is not None else url_parseada.netloc # puede tomar por ej: drive.google.com o drive.google.com:port
            nombre_archivo = "Archivo de \"" + nombre_archivo + "\"" if not titulo else titulo # ej: Archivo de "drive.google.com"
            archivo.ubicacion = ubicacion_archivo
            
        else:
            partes = str(archivo.titulo).split('_')
            nombre_archivo = partes[0] + '_' + partes[1] + '_' + titulo # 1234_4_titulo_agregado
        
        archivo.titulo = nombre_archivo

        db.session.commit()
        
        return archivo
    
class AssociatesService :

    def validate_participants (employee_id, equestrian_id):
         equestrian = EquestrianService.get_equestrian_by_id( equestrian_id)
         employee = EmployeeService.get_employee_by_id(employee_id) 
         return   equestrian is not None  and employee is not None
        

    def add_associated ( employee_id, equestrian_id): 
        """Crea la relacion entre un empleado y un ecuestre"""
       
        AssociatesService.validate_participants(employee_id, equestrian_id) 
        existe = AssociatesService.get_associated_by_ids(equestrian_id, employee_id)
        if existe is not None :
            raise ValueError(f"La asignacion ya existe para este ecuestre")
       
        associated = Associated(employee_id=employee_id , equestrian_id= equestrian_id)
        db.session.add(associated)
        db.session.commit()
        return associated

    def delete_associated (equestrian_id, employee_id):
        """Elimina un asociado de manera logica"""
        equestrian_id = int(equestrian_id)
        employee_id = int(employee_id)
        associated = AssociatesService.get_associated_by_ids(equestrian_id, employee_id)
        associated.deleted = True
        db.session.commit()
        return associated

    def get_associate_of_an_equestrian (equestrian_id, page=1, per_page=25, include_deleted=False):
        """Lista todos los asociados de un ecuestre""" 
        equestrian_id = int(equestrian_id)
        query = Associated.query.filter(Associated.equestrian_id == equestrian_id)
         
        if not include_deleted:
            query = query.filter(Associated.deleted == False)
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return pagination.items, pagination.total, pagination.pages

    def get_associated_by_ids(equestrian_id,employee_id, include_deleted=False)-> Associated:
         """Obtiene una asociacion de un id de un equestre y un empleado"""
         query = Associated.query.filter(Associated.equestrian_id == equestrian_id 
                                         and Associated.employee_id == employee_id )
         if not include_deleted:
             query = query.filter_by(deleted=False)
         associated = query.first()
         if not associated:
             raise ValueError(f"No existe la relacion para los id de ecuestre {equestrian_id} y empleado{employee_id }")
         return associated