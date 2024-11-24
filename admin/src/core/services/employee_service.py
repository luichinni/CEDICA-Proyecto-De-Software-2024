from os import path
from urllib.parse import urlparse

from core.models.employee.employee import Employee
from core.models.employee.employee_documents import EmployeeDocuments
from src.core.storage import storage
from src.core.models.user import User
from src.core.database import db
from src.core.admin_data import AdminData
from core.models.employee.employee import ProfesionEnum
from core.models.employee.employee import CondicionEnum
from core.models.employee.employee import PuestoLaboralEnum
from core.models.employee.employee import TipoDoc
from core.models.employee.employee import ExtensionesPermitidas
from core.enums.employee_enum.CondicionEnum import Enum
from datetime import date, timedelta


class EmployeeService:

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
    def get_model_fields():
        return [column.name for column in Employee.__table__.columns]

    @staticmethod
    def add_employee(**kwargs):
        """Crea un empleado"""
        employee = Employee(**kwargs)
        db.session.add(employee)
        db.session.commit()
        return employee
    
    @staticmethod
    def add_default_data_employee(email):
        """Crea un empleado con un email y el resto de los datos con valores por defecto"""
        new_employee_default_data = {"email" : email, "has_default_data":True ,"nombre" : "PENDIENTE A INGRESAR", "apellido" : "PENDIENTE A INGRESAR", "dni" : "1000000", "domicilio" : "PENDIENTE A INGRESAR", "localidad" : "PENDIENTE A INGRESAR", "telefono" : "9999999999", "profesion" : ProfesionEnum.OTRO, "puesto_laboral" : PuestoLaboralEnum.OTRO, "fecha_inicio" : date(5555, 10, 1), "fecha_cese" : date(5555, 10, 1), "contacto_emergencia_nombre" : "PENDIENTE A INGRESAR", "contacto_emergencia_telefono" : "9999999999", "obra_social" : "PENDIENTE A INGRESAR", "nro_afiliado" : "0", "condicion" : CondicionEnum.VOLUNTARIO, "activo" : False}
        default_employee = EmployeeService.add_employee(**new_employee_default_data)
        default_employee.dni = str( int(default_employee.dni)+default_employee.id )
        db.session.commit()

        return default_employee.id
            
    
    @staticmethod
    def delete_employee(employee_id):
        """Elimina un empleado de manera logica"""
        employee = EmployeeService.get_employee_by_id(employee_id)
        if not employee:
            raise ValueError(f"No existe el empleado con id {employee_id} empleado")
        employee.deleted = True
        db.session.commit()
        return employee

    
    @staticmethod
    def get_all_employees(include_admin=False, include_deleted=False):
        """Obtiene todos los roles."""
        query = Employee.query
        if not include_admin:
            query = query.filter(Employee.email != AdminData.email)
        if not include_deleted:
            query = query.filter_by(deleted = False)
        return query.all()

    @staticmethod
    def get_employees(filtro=None, order_by=None, ascending=True, include_deleted=False, page=1, per_page=5):
        """Obtiene todos los empleados"""
        employees_query = Employee.query.filter_by(deleted = include_deleted)
        if filtro:
            valid_filters = {key:value for key, value in filtro.items() if hasattr(Employee, key) and value is not None}
            for key, value in valid_filters.items():
                if key == 'puesto_laboral':
                    employees_query = employees_query.filter(Employee.puesto_laboral == value)
                else:
                    employees_query = employees_query.filter(getattr(Employee, key).ilike(f"%{str(value).lower()}%"))



        if order_by:
            if ascending:
                employees_query = employees_query.order_by(getattr(Employee, order_by).asc())
            else:
                employees_query = employees_query.order_by(getattr(Employee, order_by).desc())

        pagination = employees_query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.total, pagination.pages
    
    @staticmethod
    def get_employees_without_user():
        """Obtiene todos los empleados que no tienen un usuario asociado o cuyos usuarios están eliminados."""
        
        # Subconsulta: obtener empleados que tienen usuarios no eliminados
        subquery = Employee.query.join(User).filter(User.deleted == False).with_entities(Employee.id)
        
        # Consulta principal: empleados que no tienen usuario o cuyos usuarios están eliminados
        query = Employee.query.outerjoin(User).filter(
            (Employee.user == None) | (User.deleted == True)
        ).filter(
            Employee.id.notin_(subquery)  # Excluir empleados con usuarios no eliminados
        )
        
        return query.all()

    @staticmethod
    def update_employee(employee, **kwargs):
        """Actualiza los datos de un empleado"""

        for key, value in kwargs.items():
            if value is not None and getattr(employee, key) != value:
                setattr(employee, key, value)
        employee.has_default_data = False
        db.session.commit()
        return employee

    @staticmethod
    def get_employee_by_id(employee_id, include_deleted=False):
        """Busca un empleado por su email"""
        if not Employee.query.get(employee_id):
            raise ValueError(f"No se encontro el empleado con id {employee_id}")

        query = Employee.query.filter_by(id = employee_id)
        if not include_deleted:
            query = query.filter_by(deleted = include_deleted)
        if not query:
            raise ValueError(f"No se encontro el empleado con id {employee_id}")
        return query.first()

    @staticmethod
    def get_employee_by_email(email, include_deleted=False):
        """Busca un empleado por email y lanza un error si no existe."""
        existing_employee = Employee.query.filter_by(email = email)
        if not include_deleted:
            existing_employee = existing_employee.filter_by(deleted=False)
        if existing_employee is None:
            raise ValueError(f"No existe empleado con el email ingresado: '{email}'")
        return existing_employee.first()

    @staticmethod
    def add_document(employee_id: int | str, titulo: str, document, tipo: TipoDoc, es_link: bool) -> EmployeeDocuments:
        """Permite cargarle un documento o link a un empleado

        Args:
            employee_id (int | str): ID del empleado al que se le añadirá el document
            document (Any): Documento o link a agregar
            tipo (TipoDoc): Tipo del documento
            es_link (bool): Flag de confirmación si es link

        Returns:
            EmployeeDocuments: Retorna el objeto con la información del archivo guardado
        """
        employee = EmployeeService.get_employee_by_id(employee_id)

        ubicacion_archivo = ""
        nombre_archivo = ""

        if (int(tipo) not in TipoDoc):
            raise ValueError("Tipo de documento no es válido")

        if es_link:
            ubicacion_archivo = document  # si es link, seria la url
            url_parseada = urlparse(document)
            nombre_archivo = url_parseada.hostname if url_parseada.hostname is not None else url_parseada.netloc
            nombre_archivo = "Archivo de \"" + nombre_archivo + "\"" if not titulo else titulo

        else:
            last_file = employee.archivos
            last_id = 1

            if last_file:
                ultimo_documento = (
                    db.session.query(EmployeeDocuments)
                    .filter(EmployeeDocuments.employee_id == employee.id)
                    .order_by(EmployeeDocuments.id.desc())
                    .first()
                )
                last_id = ultimo_documento.id + 1

            nombre_archivo = employee.dni + '_' + str(last_id) + '_' + (
                document.filename if not titulo else titulo.replace(' ', '_') + path.splitext(document.filename)[
                    1])  # 44130359_4_fotocopiadni.pdf o con titulo 44130359_4_titulo_agregado.pdf
            ubicacion_archivo = 'employee_files/' + nombre_archivo  # ej: client_files/44130359_4_fotocopiadni.pdf o 44130359_4_titulo_agregado.pdf

            try:
                result = storage.client.put_object("grupo23", ubicacion_archivo, document.stream, length=-1, part_size=5 * 1024 * 1024)
            except Exception as e:
                raise ValueError(f"Hubo un problema al cargar el archivo, intenta nuevamente: {e}")

        new_file = EmployeeDocuments(
            titulo=nombre_archivo,
            tipo=EmployeeService.obtener_clave_por_valor(TipoDoc, int(tipo)),
            ubicacion=ubicacion_archivo,
            es_link=es_link,
            employee_id=employee_id
        )

        db.session.add(new_file)
        db.session.commit()

        return new_file

    @staticmethod
    def update_document(document_id: int | str, titulo: str, tipo: TipoDoc, url: str,
                        es_link: bool) -> EmployeeDocuments:
        """Permite actualizar un documento o link a un cliente

        Args:
            document_id (int | str): ID del documento al que se actualizará
            titulo (Any): titulo nuevo para documento
            tipo (TipoDocs): Tipo del documento
            url (str): url actualizada
            es_link (bool): Flag de confirmación si es link

        Returns:
            ClientDocuments: Retorna el objeto con la información del archivo guardado
        """
        archivo = EmployeeService.get_document_by_id(document_id)

        ubicacion_archivo = url
        nombre_archivo = titulo

        if (int(tipo) not in TipoDoc):
            raise ValueError("Tipo de documento no es válido")

        if es_link:
            url_parseada = urlparse(ubicacion_archivo)
            nombre_archivo = url_parseada.hostname if url_parseada.hostname is not None else url_parseada.netloc  # puede tomar por ej: drive.google.com o drive.google.com:port
            nombre_archivo = "Archivo de \"" + nombre_archivo + "\"" if not titulo else titulo  # ej: Archivo de "drive.google.com"
            archivo.ubicacion = ubicacion_archivo

        else:
            partes = str(archivo.titulo).split('_')
            nombre_archivo = partes[0] + '_' + partes[1] + '_' + titulo  # 44130359_4_titulo_agregado

        archivo.titulo = nombre_archivo

        db.session.commit()

        return archivo

    @staticmethod
    def get_document(id: int):
        archivo = EmployeeDocuments.query.get(id)

        if not archivo:
            raise ValueError(f'No existe el archivo de id {id}')

        if archivo.es_link:
            url = archivo.ubicacion
        else:
            formatos = {ext.name: ext.value for ext in ExtensionesPermitidas}
            headers = {"response-content-type": formatos[path.splitext(archivo.ubicacion)[1][1:].upper()]}
            url = storage.client.presigned_get_object('grupo23', archivo.ubicacion, expires=timedelta(hours=1),
                                                      response_headers=headers)

        return url

    @staticmethod
    def get_document_by_id(id: int) -> EmployeeDocuments:
        doc = EmployeeDocuments.query.get(id)

        if not doc:
            raise ValueError(f'No existe el archivo de id {id}')

        return doc

    @staticmethod
    def get_documents(employee_id: int | str, filtro: dict = None, extension: str = None, page: int = 1,
                      per_page: int = 5, order_by: str = None, ascending: bool = True, include_deleted: bool = False,
                      like: bool = False):
        """
        Obtiene por página y filtro los documentos de un empleado específico.

        Args:
            client_id (int | str): ID del empleado cuyos documentos son requeridos.
            filtro (dict, optional): Diccionario de filtros para los archivos. Defaults to None.
            page (int, optional): Número de página requerida. Defaults to 1.
            per_page (int, optional): Cantidad de archivos por página. Defaults to 5.
            order_by (str, optional): Campo de orden para los elementos. Defaults to None.
            ascending (bool, optional): Flag de datos ascendentes o descendentes. Defaults to True.
            include_deleted (bool, optional): Flag de inclusión de archivos con borrado lógico. Defaults to False.
            like (bool, optional): Flag de búsqueda parcial en strings. Defaults to False.
        """
        if isinstance(employee_id, str):
            client_id = int(employee_id)

        query = EmployeeDocuments.query.filter(EmployeeDocuments.employee_id == employee_id)

        if not include_deleted:
            query = query.filter(EmployeeDocuments.deleted == include_deleted)

        if filtro:
            for key, value in filtro.items():
                if hasattr(EmployeeDocuments, key) and value is not None:
                    if isinstance(value, str) and not issubclass(getattr(EmployeeDocuments, key).type.python_type,
                                                                 Enum) and like:
                        query = query.filter(getattr(EmployeeDocuments, key).like(f'%{value}%'))
                    else:
                        query = query.filter(getattr(EmployeeDocuments, key) == value)

        if extension:
            extension = extension.lower()
            if extension != 'link':
                query = query.filter(EmployeeDocuments.ubicacion.like(f'%.{extension}'))
            elif extension == 'link':
                query = query.filter_by(es_link=True)

        if order_by and hasattr(EmployeeDocuments, order_by):
            if ascending:
                query = query.order_by(getattr(EmployeeDocuments, order_by).asc())
            else:
                query = query.order_by(getattr(EmployeeDocuments, order_by).desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return pagination.items, pagination.total, pagination.pages

    @staticmethod
    def delete_document(docs_id: int | str):
        """Eliminación lógica de un documento o link en particular

        Args:
            docs_id (int | str): ID del documento o link a dar de baja
        """
        document = EmployeeDocuments.query.get(docs_id)

        if not document:
            raise ValueError('No existe el archivo que se intenta eliminar')

        document.deleted = True
        db.session.commit()

    @staticmethod
    def create_admin_employee():
        """Crea un empleado admin con email del admin si no existe."""
        admin_email = AdminData.email
        EmployeeService.add_employee(nombre="admin", email=admin_email, apellido="a", dni="00000000",
        domicilio="a", localidad="a",telefono="1234",profesion=ProfesionEnum.MEDICO,puesto_laboral=PuestoLaboralEnum.DOMADOR,
        fecha_inicio=date(2023, 10, 8),
        fecha_cese =date(2023, 10, 8),
        contacto_emergencia_nombre ="a",
        contacto_emergencia_telefono = "123",
        obra_social="a",
        nro_afiliado ="0",
        condicion=CondicionEnum.VOLUNTARIO,
        activo=True)

    @staticmethod
    def create_example_employees():
        """Crea un empleados de ejemplo."""

        example_employees = [
            {"nombre" : "nombre 1", "email" : "exa1@example.com", "apellido" : "apellido 1", "dni" : "00000004", "domicilio" : "a", "localidad" : "a", "telefono" : "1234", "profesion" : ProfesionEnum.MEDICO, "puesto_laboral" : PuestoLaboralEnum.DOMADOR, "fecha_inicio" : date(2023, 10, 8), "fecha_cese" : date(2023, 10, 8), "contacto_emergencia_nombre" : "a", "contacto_emergencia_telefono" : "1234", "obra_social" : "a", "nro_afiliado" : "0", "condicion" : CondicionEnum.VOLUNTARIO, "activo" : True},
            {"nombre" : "nombre 2", "email" : "exa2@example.com", "apellido" : "apellido 2", "dni" : "00000001", "domicilio" : "a", "localidad" : "a", "telefono" : "1234", "profesion" : ProfesionEnum.MEDICO, "puesto_laboral" : PuestoLaboralEnum.DOMADOR, "fecha_inicio" : date(2023, 10, 8), "fecha_cese" : date(2023, 10, 8), "contacto_emergencia_nombre" : "a", "contacto_emergencia_telefono" : "1234", "obra_social" : "a", "nro_afiliado" : "0", "condicion" : CondicionEnum.VOLUNTARIO, "activo" : True},
            {"nombre" : "nombre 3", "email" : "exa3@example.com", "apellido" : "apellido 3", "dni" : "00000002", "domicilio" : "a", "localidad" : "a", "telefono" : "1234", "profesion" : ProfesionEnum.MEDICO, "puesto_laboral" : PuestoLaboralEnum.DOMADOR, "fecha_inicio" : date(2023, 10, 8), "fecha_cese" : date(2023, 10, 8), "contacto_emergencia_nombre" : "a", "contacto_emergencia_telefono" : "1234", "obra_social" : "a", "nro_afiliado" : "0", "condicion" : CondicionEnum.VOLUNTARIO, "activo" : True}
        ]
        for employee_data in example_employees:
            EmployeeService.add_employee(**employee_data)



