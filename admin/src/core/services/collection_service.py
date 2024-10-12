from src.core.database import db
from src.core.models.collection import Collection
from sqlalchemy import desc
from src.core.services.employee_service import EmployeeService
from src.core.services.client_service import ClientService
from src.web.handlers import validate_params

class CollectionService:

    @staticmethod
    @validate_params
    def create_collection(employee_id, client_id, payment_date, payment_method, amount, observations = "No observations"):
        """Crea un cobro"""
        EmployeeService.get_employee_by_id(employee_id) # Verificamos que exista el empleado
        ClientService.get_client_by_id(client_id) # Verificamos que exista el cliente
        
        new_collection = Collection(
            employee_id=employee_id,
            client_id=client_id,
            payment_date=payment_date,
            payment_method=payment_method,
            amount=amount,
            observations=observations
        )
        db.session.add(new_collection)
        db.session.commit()
        return new_collection

    @staticmethod
    def update_collection(collection_id, payment_date=None, payment_method=None, amount=None, observations=None):
        """Actualiza un cobro"""
        collection = CollectionService.get_collection_by_id(collection_id)
        
        if payment_date is not None:
            collection.payment_date = payment_date
        if payment_method is not None:
            collection.payment_method = payment_method
        if amount is not None:
            collection.amount = amount
        if observations is not None:
            collection.observations = observations

        db.session.commit()
        return collection

    @staticmethod
    @validate_params
    def delete_collection(collection_id):
        """Elimina un cobro de forma lógica"""
        collection = CollectionService.get_collection_by_id(collection_id)
        collection.deleted = True
        db.session.commit()

    @staticmethod
    @validate_params
    def get_collection_by_id(collection_id, include_deleted=False):
        """Obtiene un cobro por su ID"""
        query = Collection.query.filter_by(id=collection_id)
        if not include_deleted:
            query = query.filter_by(deleted=False)
        collection = query.first()
        if not collection:
            raise ValueError(f"No existe el collection con ID: {collection_id}")
        return collection

    @staticmethod
    @validate_params
    def get_all_collections(page=1, per_page=25, include_deleted=False):
        """Lista todos los cobros"""
        query = Collection.query
        if not include_deleted:
            query = query.filter_by(deleted=False)
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return pagination.items, pagination.total, pagination.pages

    @staticmethod
    def apply_ordering(query, order_by_date, ascending):
        """Aplica el ordenamiento a la consulta según el campo y el orden deseado."""
        if order_by_date:
            column = Collection.payment_date
        else:
            column = Collection.created_at
        
        return query.order_by(column.asc() if ascending else column.desc())

    @staticmethod
    def search_collections(start_date=None, end_date=None, payment_method=None, nombre=None, apellido=None, page=1, per_page=25, order_by_date=False, ascending=True, include_deleted=False):
        """Busca cobros con filtros"""
        query = Collection.query

        if not include_deleted:
            query = query.filter(Collection.deleted == False) 

        if start_date:
            query = query.filter(Collection.payment_date >= start_date)
        if end_date:
            query = query.filter(Collection.payment_date <= end_date)
        if payment_method:
            query = query.filter_by(payment_method=payment_method)

        if nombre:
            query = query.join(Collection.employee).filter_by(nombre=nombre)
        if apellido:
            query = query.join(Collection.employee).filter_by(apellido=apellido)
        
        query = CollectionService.apply_ordering(query, order_by_date, ascending)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination.items, pagination.total, pagination.pages
