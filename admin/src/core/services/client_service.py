from src.core.models.client import Client
from src.core.database import db

class ClientService:
    @staticmethod
    def validate_data(**kwargs):
        copy = dict(kwargs)
        for campo in copy.keys():
            if (campo == 'dni'):
                pass
            elif (campo == 'fecha_nacimiento'):
                pass
            elif (campo == 'lugar_nacimiento'):
                pass
            elif (campo == 'domicilio'):
                pass
            elif (campo == 'telefono'):
                pass
            elif (campo == 'contacto_emergencia'):
                pass
            elif (campo == 'becado'):
                pass
            elif (campo == 'obs_beca'):
                pass
            elif (campo == 'cert_discapacidad'):
                pass
            elif (campo == 'discapacidad'):
                pass
            elif (campo == 'asignacion'):
                pass
            elif (campo == 'pension'):
                pass
            elif (campo == 'obra_social'):
                pass
            elif (campo == 'nro_afiliado'):
                pass
            elif (campo == 'curatela'):
                pass
            elif (campo == 'observaciones'):
                pass
            elif (campo == 'institucion_escolar'):
                pass
            elif (campo == 'atendido_por'):
                pass
            elif (campo == 'tutores_responsables'):
                pass
            elif (campo == 'propuesta_trabajo'):
                pass
            elif (campo == 'condicion'):
                pass
            elif (campo == 'sede'):
                pass
            elif (campo == 'dias'):
                pass
            elif (campo == 'profesor_id'):
                pass
            elif (campo == 'conductor_id'):
                pass
            elif (campo == 'caballo_id'):
                pass
            elif (campo == 'auxiliar_pista_id'):
                pass
            else:
                pass

    @staticmethod
    def create_client(**kwargs):
        """Crea un nuevo cliente."""
        ClientService.validate_data(**kwargs)

        """ new_client = Client(dni=dni) """

        # TODO: CHEQUEAR QUE EL DNI SEA UNICO CUANDO SE IMPLEMENTE 

        db.session.add(new_client)
        db.session.commit()

        return new_client

    @staticmethod
    def get_client_by_id(client_id):
        """Busca un cliente por id y lanza un error si no existe."""
        existing_client = Client.query.get(client_id)
        if existing_client is None:
            raise ValueError(f"No existe cliente con el id ingresado: '{client_id}'")
        return existing_client
    
    @staticmethod
    def get_client_by_dni(dni):
        """Busca un cliente por dni y lanza un error si no existe."""
        existing_client = Client.query.filter_by(dni=dni).first()
        if existing_client is None:
            raise ValueError(f"No existe cliente con el dni ingresado: '{dni}'")
        return existing_client
    
    @staticmethod
    def get_clients(filtro=None, order_by=None, ascending=True, include_deleted=False):
        """Obtiene todos los empleados"""
        employees_query = Client.query.filter_by(deleted=include_deleted)
        if filtro:
            valid_filters = {key:value for key, value in filtro.items() if hasattr(Client, key) and value is not None}
            employees_query = employees_query.filter_by(**valid_filters)

        if order_by:
            if ascending:
                employees_query = employees_query.order_by(getattr(Client, order_by).asc())
            else:
                employees_query = employees_query.order_by(getattr(Client, order_by).desc())
        return employees_query.all()
    
    @staticmethod
    def create_example_clients():
        """Crea clientes de ejemplo."""
        ClientService.create_client("12345678")
        ClientService.create_client("87654321")
        ClientService.create_client("11111111")
