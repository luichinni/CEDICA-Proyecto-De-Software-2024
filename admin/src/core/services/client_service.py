from src.core.models.client import Client
from src.core.database import db

class ClientService:

    @staticmethod
    def create_client(dni):
        """Crea un nuevo cliente."""
        new_client = Client(dni=dni)

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
