import urllib.parse
from src.core.database import db
from src.core.enums.client_enum import *
from src.core.services.employee_service import EmployeeService
from src.core.services.equestrian_service import EquestrianService
from src.core.models.client import Clients, ClientDocuments
from src.core.storage import storage
from urllib.parse import urlparse

class ClientService:
    @staticmethod
    def validate_data(**kwargs):
        """Verifica que los datos pasados cumplan las especificaciones para ser datos validos

        Raises:
            ValueError: Ya existe DNI
            ValueError: DNI no valido
            ValueError: Información de contacto incompleta
            ValueError: Campo booleano con valor incompatible
            ValueError: Campo enumerativo con valor incompatible
            ValueError: Afiliado ya existente a una misma obra social
            ValueError: Información escolar incompleta o erronea
            ValueError: Información de tutores legales incompleta o erronea
            ValueError: Dias de actividad invalidos
            ValueError: No existe profesor, conductor o auxiliar de pista
            ValueError: No existe ecuestre

        Returns:
            dict: diccionario con los campos realmente validos
        """
        copy = dict(kwargs)
        validos = dict()
        
        for campo in copy.keys():
            if not hasattr(Clients, campo): # salteo ejecucion de campos que no son válidos
                continue
            
            if (campo == 'dni' and (copy['update'] == False)): # comprobar solo numeros y buscar repetido
                if copy[campo].isdigit():
                    try:
                        ClientService.get_client_by_dni(copy[campo])
                        raise ValueError(f"Ya existe cliente con el dni ingresado: '{copy[campo]}'") 
                    except:
                        validos[campo] = copy[campo]
                else:
                    raise ValueError(f"El dni ingresado debe ser solo numérico")      
                  
            elif (campo == 'fecha_nacimiento'): # comprobar fecha 
                pass

            elif (campo == 'contacto_emergencia'): # nombre y telefono
                if (type(copy[campo]) == 'dict') and len(set('nombre','telefono').intersection(set(copy[campo].keys()))) == 2:
                    validos[campo] = copy[campo]
                else:
                    raise ValueError(f"La información del contacto de emergencia está incompleta")
            
            elif (campo == 'becado' or campo == 'curatela' or campo == 'condicion'): # 1, 0 o True, False
                if not (copy[campo] in ['True','False','0','1']):
                    raise ValueError(f"El campo {campo} no es válido")
                else:
                    validos[campo] = copy[campo]
            
            elif (campo == 'discapacidad' or campo == 'asignacion' or campo == 'pension' or campo == 'propuesta_trabajo'): # enum
                if not (copy[campo] in Discapacidad):
                    raise ValueError(f"{copy[campo]} no es {campo} válida")
                else:
                    validos[campo] = copy[campo]

            elif (campo == 'nro_afiliado' and (copy['update'] == False)): # repetido?
                if len(ClientService.get_clients({"nro_afiliado":copy[campo], "obra_social":copy['obra_social']})) != 0:
                    raise ValueError(f"Ya existe cliente con nro de afiliado {copy[campo]} para {copy['obra_social']}'")
                else:
                    validos[campo] = copy[campo]

            elif (campo == 'institucion_escolar'): # nombre, dir, tel, grado y obs
                if (type(copy[campo]) == 'dict') and len(set('nombre_esc','direccion_esc','tel_esc','grado_esc','obs_esc').intersection(set(copy[campo].keys()))) == 5:
                    validos[campo] = copy[campo]
                else:
                    raise ValueError(f"La información de institución escolar está incompleta")

            elif (campo == 'tutores_responsables'): # parentesco, nombre, apellido, dni, dir, cel, mail, nivel escolaridad maximo y ocupacion
                for idx,tutor in enumerate(copy[campo]):
                    if not ((type(tutor) == 'dict') and len(set('parentesco','nombre','apellido','dni','domicilio','tel','mail','nivel_edu','ocupacion').intersection(set(tutor.keys()))) == 9):
                        raise ValueError(f"La información del tutor legal {idx} está incompleta")
                validos[campo] = copy[campo]
                
            elif (campo == 'dias'): # dia valido?
                for idx, dia in enumerate(copy[campo]):
                    if not (dia in Dias):
                        raise ValueError(f"El dia {dia} no es válido")
                validos[campo] = copy[campo]
            
            elif (campo == 'profesor_id' or campo == 'conductor_id' or campo == 'auxiliar_pista_id'): # verificar existencia
                try:
                    EmployeeService.get_employee_by_id(copy[campo])
                    validos[campo] = copy[campo]
                except:
                    raise ValueError(f"El {campo.replace('_',' ')} no es válido")

            elif (campo == 'caballo_id'): # verificar existencia 
                try:
                    EquestrianService.get_Equestrian_by_id(copy[campo])
                    validos[campo] = copy[campo]
                except:
                    raise ValueError(f"El {campo.replace('_',' ')} no es válido")

            else: # si no necesita validación --> nombre, apellido, lugar_nacimiento, domicilio, telefono, obs_beca, cert_discapacidad, obra_social, observaciones, sede, atendido_por
                validos[campo] = copy[campo]

        return validos

    @staticmethod
    def create_client(**kwargs) -> Clients:
        """Crea un nuevo cliente a partir de los datos ingresados

        Args:
            **kwargs (Any): Conjunto de atributos sin especificar
        
        Returns:
            Clients: Cliente creado y cargado en la base de datos
        """
        kwargs['update'] = False
        validos = ClientService.validate_data(**kwargs)

        new_client = Clients(**validos)

        db.session.add(new_client)
        db.session.commit()

        return new_client
    
    @staticmethod
    def update_client(client: Clients, **kwargs) -> Clients:
        """Actualiza un cliente dado

        Args:
            client (Client): cliente a actualizar

        Returns:
            Clients: Cliente actualizado
        """
        kwargs['update'] = True
        validos = ClientService.validate_data(**kwargs)

        for key, value in validos.items():
            if value is not None and getattr(client, key) != value:
                setattr(client, key, value)
                
        db.session.commit()
        return client
    
    @staticmethod
    def delete_client(client_id: int | str):
        """Eliminación lógica de un cliente

        Args:
            client_id (int | str): id del cliente a eliminar
        """
        client = ClientService.get_client_by_id(client_id)
        client.deleted = True
        db.session.commit()

    @staticmethod
    def get_client_by_id(client_id: int | str, deleted=False) -> Clients:
        """Busca el cliente pasado por id

        Args:
            client_id (int | str): ID del cliente a buscar
            deleted (bool): Flag de eliminación lógica del cliente
            
        Raises:
            ValueError: ID inexistente
            ValueError: Cliente eliminado con busqueda filtrandolo

        Returns:
            Clients: Cliente obtenido de la busqueda
        """
        existing_client = Clients.query.get(client_id)
        if existing_client is None:
            raise ValueError(f"No existe cliente con el id ingresado: '{client_id}'")
        
        if deleted == False and existing_client.deleted == True:
            raise ValueError(f"El cliente ingresado fue eliminado previamente: '{client_id}'")
        
        return existing_client
    
    @staticmethod
    def get_client_by_dni(dni: str, deleted=False) -> Clients:
        """Obtiene un cliente segun un dni ingresado

        Args:
            dni (str): DNI del cliente que se busca
            deleted (bool, optional): _description_. Defaults to False.

        Raises:
            ValueError: DNI inexistente
            ValueError: Cliente eliminado con busqueda filtrandolo

        Returns:
            Clients: Cliente obtenido de la busqueda
        """
        existing_client = Clients.query.filter_by(dni=dni).first()
        if existing_client is None:
            raise ValueError(f"No existe cliente con el dni ingresado: '{dni}'")
        
        if deleted == False and existing_client.deleted == True:
            raise ValueError(f"El cliente ingresado fue eliminado previamente: '{dni}'")
        
        return existing_client
    
    @staticmethod
    def get_clients(filtro: dict = None, page: int = 1, per_page: int = 25, order_by: str = None, ascending: bool =True, include_deleted: bool =False) -> list:
        """Lista los clientes segun los filtros especificados, en caso de no especificar retorna los primeros 25 clientes

        Args:
            filtro (dict, optional): Diccionario de { campo: valor_esperado } para filtrar. Defaults to None.
            page (int, optional): Nro de pagina esperada. Defaults to 1.
            per_page (int, optional): Cantidad de resultados por pagina. Defaults to 25.
            order_by (str, optional): Campo para ordenar. Defaults to None.
            ascending (bool, optional): Flag de ordenamiento asc o desc. Defaults to True.
            include_deleted (bool, optional): Flag de inclusión eliminados. Defaults to False.

        Returns:
            list: Listado de clientes obtenidos a partir de la busqueda
        """
        query = Clients.query.filter_by(deleted=include_deleted)
        if filtro:
            valid_filters = {key:value for key, value in filtro.items() if hasattr(Clients, key) and value is not None}
            query = query.filter_by(**valid_filters)

        if order_by:
            if ascending:
                query = query.order_by(getattr(Clients, order_by).asc())
            else:
                query = query.order_by(getattr(Clients, order_by).desc())
                
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.total, pagination.pages
    
    @staticmethod
    def add_document(client_id: int | str, document, tipo: TipoDocs, es_link: bool) -> ClientDocuments:
        """Permite cargarle un documento o link a un cliente

        Args:
            client_id (int | str): ID del cliente al que se le añadirá el document
            document (Any): Documento o link a agregar
            tipo (TipoDocs): Tipo del documento
            es_link (bool): Flag de confirmación si es link

        Returns:
            ClientDocuments: Retorna el objeto con la información del archivo guardado
        """
        cliente = ClientService.get_client_by_id(client_id)
        
        ubicacion_archivo = ""
        nombre_archivo = ""
        
        if (tipo not in TipoDocs):
            raise ValueError("Tipo de documento no es válido")
        
        if es_link:
            ubicacion_archivo = document
            url_parseada = urlparse(document)
            nombre_archivo = url_parseada.hostname if url_parseada.hostname is not None else url_parseada.netloc # puede tomar por ej: drive.google.com o drive.google.com:port
            nombre_archivo = "Archivo de \"" + nombre_archivo + "\"" # ej: Archivo de "drive.google.com"
            
        else:
            last_file = cliente.archivos.order_by(ClientDocuments.id.desc()).first()
            last_id = 1
            
            if last_file:
                last_id = last_file.id + 1
                
            ubicacion_archivo = cliente.dni + '_' + last_id + '_' + document.filename # ej: 44130359_4_fotocopiadni.pdf
            nombre_archivo = document.filename
            
            try:
                storage.client.put_object("grupo23",ubicacion_archivo,document.stream,length=-1)
            except:
                raise ValueError("Hubo un problema al cargar el/los archivos, intenta nuevamente")
        
        new_file = ClientDocuments(
            titulo=nombre_archivo, 
            tipo=tipo, 
            ubicacion=ubicacion_archivo, 
            es_link=es_link)

        db.session.add(new_file)
        db.session.commit()
        
        return new_file
    
    @staticmethod
    def get_documents(client_id: int | str, filtro: dict = None, page: int = 1, per_page: int = 25, order_by: str = None, ascending: bool = True, include_deleted: bool = False):
        """Obtiene por pagina y filtro los documentos de un cliente especifico

        Args:
            client_id (int | str): ID del cliente cuyos documentos son requeridos
            filtro (dict, optional): Diccionario de filtros para los archivos. Defaults to None.
            page (int, optional): Nro de página requerida. Defaults to 1.
            per_page (int, optional): Cantidad de archivos por página. Defaults to 25.
            order_by (str, optional): Campo de orden para los elementos. Defaults to None.
            ascending (bool, optional): Flag de datos ascendentes o descendentes. Defaults to True.
            include_deleted (bool, optional): Flag de inclusión de archivos con borrado lógico. Defaults to False.
        """
        query = ClientDocuments.query.filter_by(deleted=include_deleted)
        if filtro:
            valid_filters = {key:value for key, value in filtro.items() if hasattr(ClientDocuments, key) and value is not None}
            query = query.filter_by(**valid_filters)

        if order_by:
            if ascending:
                query = query.order_by(getattr(ClientDocuments, order_by).asc())
            else:
                query = query.order_by(getattr(ClientDocuments, order_by).desc())
                
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.total, pagination.pages
    
    @staticmethod
    def delete_document(docs_id: int | str):
        """Eliminación lógica de un documento o link en particular

        Args:
            docs_id (int | str): ID del documento o link a dar de baja
        """
        document = ClientDocuments.query.get(docs_id)
        document.deleted = True
        db.session.commit()
    
    @staticmethod
    def create_example_clients():
        """Crea clientes de ejemplo."""
        ClientService.create_client("12345678")
        ClientService.create_client("87654321")
        ClientService.create_client("11111111")
