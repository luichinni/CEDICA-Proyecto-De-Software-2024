from core.enums.client_enum import AsignacionFamiliar, Condicion, Pension
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


db = SQLAlchemy()

def init_app(app):
    """Inicializar la base de datos."""
    db.init_app(app)
    config(app)

    return app

def config(app):
    """Cerrar la session de la base de datos al finalizar el contexto de la app"""
    @app.teardown_appcontext
    def close_session(exception=None):
        db.session.close()
    return app

def reset():
    """Resetea la base de datos"""
    print("Eliminando la base de datos")
    db.drop_all()
    print("Creando la base de datos")
    db.create_all()
    print("Finalizacion del reset de la base de datos!")

def init(UserService, RoleService, EmployeeService, PermissionService, ClientService, EquestrianService, PublicationService):
    """Inicializa la base de datos"""
    print("Creando empleado admin")
    EmployeeService.create_admin_employee()
    print("Creando rol system admin")
    RoleService.create_admin_role()
    print("Creando user admin del sistema")
    UserService.create_admin_user()
    print("Creando permisos de ejemplo")
    PermissionService.create_initial_permissions()
    print("Creando roles de ejemplo")
    RoleService.create_example_roles()
    print("Creando empleados de ejemplo")
    EmployeeService.create_example_employees()
    print("Creando encuestre de ejemplo")
    create_example_eq(EquestrianService)
    print("Creando cliente de ejemplo")
    create_example_client(ClientService)
    print("Creando publicaciones de ejemplo")
    PublicationService.create_example_publications()

    print("Creando user pendiente")
    UserService.create_user(-1, "Esteban Quito", "Clavemagica123", role_id= RoleService.get_role_by_name("Usuario a confirmar por admin").id, employee_email="esperando@validacion.com")
    UserService.create_user(-1, "Esteban Quito 2", "Clavemagica1232", role_id= RoleService.get_role_by_name("Usuario a confirmar por admin").id, employee_email="esperando2@validacion.com")

    print("Finalizacion de la inicializacion de la base de datos!")

    
def create_example_client(ClientService):

    ClientService.create_client(
        dni='12345678',
        nombre='Juan',
        apellido='Pérez',
        fecha_nacimiento=datetime.strptime('2010-05-12', '%Y-%m-%d').date(),
        lugar_nacimiento={
            'localidad_nacimiento':'La Plata',
            'provincia_nacimiento':'Buenos Aires'    
        },
        domicilio={
            'calle':'50',
            'numero':'234',
            'departamento':None,
            'localidad':'La Palta',
            'provincia':'Buenos Aires'
        },
        telefono='123456789',
        contacto_emergencia={"nombre": "Ana Pérez", "telefono": "987654321"},
        becado=True,
        obs_beca='Beca otorgada por buenos desempeños',
        cert_discapacidad=Condicion.NO_POSEE.value,
        discapacidad='1',
        asignacion=AsignacionFamiliar.NO_PERCIBE.value,
        pension=Pension.NO_ES_BENEFICIARIO.value,
        obra_social='Obra Social Ejemplo',
        nro_afiliado='0123456789',
        curatela=False,
        observaciones='No observaciones adicionales',
        institucion_escolar=None,
        atendido_por='Dr. Smith',
        tutores_responsables=[{
            "parentesco": "Padre",
            "nombre": "Carlos Pérez",
            "apellido": "Pérez",
            "dni": "23456789",
            "domicilio": "Calle 123, Ciudad",
            "celular": "0987654321",
            "email": "padre@gmail.com",
            "escolaridad": "Universitario",
            "ocupacion": "Ingeniero"
        }],
        propuesta_trabajo=1,
        condicion=True,
        sede='CASJ',
        dias=[1],
        profesor_id=1,
        conductor_id=2,
        caballo_id=1,
        auxiliar_pista_id=3,
        deleted=False,
        deudor=False
    )

    ClientService.create_client(
        dni='87654321',
        nombre='Pepe',
        apellido='Gomez',
        fecha_nacimiento=datetime.strptime('2010-05-12', '%Y-%m-%d').date(),
        lugar_nacimiento={
            'localidad_nacimiento':'La Plata',
            'provincia_nacimiento':'Buenos Aires'    
        },
        domicilio={
            'calle':'50',
            'numero':'234',
            'departamento':None,
            'localidad':'La Palta',
            'provincia':'Buenos Aires'
        },
        telefono='123456789',
        contacto_emergencia={"nombre": "Ana Pérez", "telefono": "987654321"},
        becado=True,
        obs_beca='Beca otorgada por buenos desempeños',
        cert_discapacidad=Condicion.NO_POSEE.value,
        discapacidad='1',
        asignacion=AsignacionFamiliar.NO_PERCIBE.value,
        pension=Pension.NO_ES_BENEFICIARIO.value,
        obra_social='Obra Social Ejemplo',
        nro_afiliado='0123456789',
        curatela=False,
        observaciones='No observaciones adicionales',
        institucion_escolar=None,
        atendido_por='Dr. Smith',
        tutores_responsables=[{
            "parentesco": "Padre",
            "nombre": "Carlos Pérez",
            "apellido": "Pérez",
            "dni": "23456789",
            "domicilio": "Calle 123, Ciudad",
            "celular": "0987654321",
            "email": "padre@gmail.com",
            "escolaridad": "Universitario",
            "ocupacion": "Ingeniero"
        }],
        propuesta_trabajo=1,
        condicion=True,
        sede='CASJ',
        dias=[1],
        profesor_id=1,
        conductor_id=2,
        caballo_id=1,
        auxiliar_pista_id=3,
        deleted=False,
        deudor=True
    )
    
    
def create_example_eq(EquestrianService):
    EquestrianService.add_equestrian(
        nombre='Estrella',
        sexo='FEMENINO',
        raza='Criollo',
        pelaje='Blanco',
        compra=False,
        fecha_nacimiento="2014-05-15",
        fecha_ingreso="2014-05-15",
        sede_asignada='CASJ',
        tipo_de_jya_asignado='HIPOTERAPIA'
    )