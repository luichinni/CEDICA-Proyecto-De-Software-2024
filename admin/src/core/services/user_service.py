from src.core.database import db
from src.core.services.role_service import RoleService
from src.core.services.employee_service import EmployeeService
from src.core.models.user import User
from src.core.models.employee import Employee
from src.core.models.user.role_permission import RolePermission
from src.core.admin_data import AdminData
from src.web.handlers import validate_params
import re
from src.core.bcrypy_and_session import bcrypt

class UserService:
    
    @staticmethod
    def check_user(email,password) -> int:
        """Este método comprueba que un mail y contraseña sean validos para posteriormente iniciar una sesión.

        Args:
            email (str): representa el mail ingresado en login
            password (str): represena la clave sin encriptar ingresada en login

        Returns:
            int: valor que representa la ID del usuario si es que existe, sino None.
        """
        user = UserService.search_users(email=email,activo=True, include_deleted=False, include_blocked=False)[0]
        id_return = None
        if not user:
            return id_return
        
        encrypted_pass = bcrypt.check_password_hash(user[0].password, password)
        
        if encrypted_pass:
            id_return = user[0].id
            
        return id_return
    
    @staticmethod
    def validate_password(password):
        """Verifica que la contraseña cumpla con los requisitos."""
        if len(password) < 8 or len(password) > 20:
            raise ValueError("La contraseña debe tener entre 8 y 20 caracteres.")
        if not re.search(r"[a-z]", password):
            raise ValueError("La contraseña debe contener al menos una letra minúscula.")
        if not re.search(r"[A-Z]", password):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r"[0-9]", password):
            raise ValueError("La contraseña debe contener al menos un número.")

    @staticmethod
    def validate_role_id(role_id):
        """Verifica que el rol no sea admin, a menos que este no exista."""
        role_name = RoleService.get_role_by_id(role_id=role_id).name
        if role_name != AdminData.role_name: 
            return
    
        try:
            existing_admin = UserService.get_user_by_alias(alias=AdminData.alias, include_deleted=True, include_blocked=True)
        except ValueError as e: 
            return
        raise ValueError("No se permite interactuar con el usuario System Admin ni con sus datos.")

    @staticmethod
    def validate_employee_id(employee_id):
        """Verifica que el employee exista"""
        employee = EmployeeService.get_employee_by_id(employee_id)

    @staticmethod
    @validate_params
    def create_user(employee_id, alias, password, role_id = None, activo=True):
        """Crea un nuevo usuario."""
        if role_id is None:
            role_id = RoleService.get_role_by_name("Usuario a confirmar por admin").id
        UserService.validate_password(password)
        hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        password = hash.decode("utf-8")# encripta
        UserService.validate_role_id(role_id)
        UserService.validate_employee_id(employee_id)
        user = User(
            employee_id=employee_id,
            alias=alias,
            password=password,
            activo=activo,
            role_id=role_id
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update_user(user_id, alias=None, password=None, activo=None, role_id=None):
        """Actualiza un usuario existente."""
        user = UserService.get_user_by_id(user_id, include_blocked=True)
        if user.role.name == AdminData.role_name: 
            raise ValueError("No se permite interactuar con el usuario System Admin ni con sus datos.")

        if alias is not None:
            user.alias = alias
        if password is not None and password is not '':
            UserService.validate_password(password)
            hash = bcrypt.generate_password_hash(password.encode("utf-8"))
            user.password = hash.decode("utf-8")# encripta
        if activo is not None:
            user.activo = activo
        if role_id is not None:
            UserService.validate_role_id(role_id)
            user.role_id = role_id 
        db.session.commit()

        return user
    
    @staticmethod
    @validate_params
    def delete_user(user_id):
        """Elimina un usuario por su ID de forma lógica."""
        user = UserService.get_user_by_id(user_id, include_blocked=True)
        
        UserService.validate_role_id(user.role_id)
        
        user.deleted = True
        db.session.commit()
    
    @staticmethod
    @validate_params
    def block_user(user_id):
        """Bloquea un usuario por su ID."""
        user = UserService.get_user_by_id(user_id, include_blocked=True)
        
        UserService.validate_role_id(user.role_id)
        
        user.blocked = not user.blocked
        db.session.commit()
    
    @staticmethod
    @validate_params
    def get_user_by_id(user_id, include_deleted=False, include_blocked=False):
        """Obtiene un usuario por su ID."""
        query = User.query.filter_by(id=user_id)
        
        if not include_deleted:
            query = query.filter_by(deleted=False)
        
        if not include_blocked:
            query = query.filter_by(blocked=False)
        
        existing_user = query.first()
        if existing_user is None:
            raise ValueError(f"No existe un usuario con el ID ingresado: '{user_id}'")
        
        return existing_user
    
    @staticmethod
    @validate_params
    def get_user_by_alias(alias, include_deleted=False, include_blocked=False):
        """Obtiene un usuario por su alias."""
        query = User.query.filter_by(alias=alias)
        
        if not include_deleted:
            query = query.filter_by(deleted=False)
        
        if not include_blocked:
            query = query.filter_by(blocked=False)
        
        existing_user = query.first()
        if existing_user is None:
            raise ValueError(f"No existe un usuario con el alias ingresado: '{alias}'")
        
        return existing_user

    @staticmethod
    @validate_params
    def get_all_users(page=1, per_page=25, include_deleted=False, include_blocked=True):
        """Obtiene todos los usuarios."""
        query = User.query
        
        if not include_deleted:
            query = query.filter_by(deleted=False)
        
        if not include_blocked:
            query = query.filter_by(blocked=False)
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return pagination.items, pagination.total, pagination.pages
    
    @staticmethod
    def apply_ordering(query, order_by, ascending):
        """Aplica el ordenamiento a la consulta según el campo y el orden deseado."""
        if order_by == 'email':
            query = query.join(User.employee)
            column = Employee.email
        elif order_by == 'created_at':
            column = User.created_at
        else:
            raise ValueError("El campo de ordenamiento debe ser 'email' o 'created_at'.")

        return query.order_by(column.asc() if ascending else column.desc())

    @staticmethod
    def search_users(email=None, activo=None, role_id=None, page=1, per_page=25, order_by='created_at', ascending=True, include_deleted=False, include_blocked=True):
        """Busca usuarios por email, activo, y rol con paginación y ordenamiento."""
        query = User.query

        if not include_deleted:
            query = query.filter_by(deleted=False)
        
        if not include_blocked:
            query = query.filter_by(blocked=False)

        if email:
            query = query.join(User.employee).filter(Employee.email.ilike(f'%{email}%'))

        if activo is not None:
            query = query.filter(User.activo == activo)

        if role_id:
            query = query.filter(User.role_id == role_id)

        if order_by not in ['email', 'created_at']:
            raise ValueError("El campo de ordenamiento debe ser 'email' o 'created_at'.")

        query = UserService.apply_ordering(query, order_by, ascending)

        pagination = query.paginate(page=page, per_page=per_page, error_out=True)
        
        return pagination.items, pagination.total, pagination.pages


    @staticmethod
    @validate_params
    def user_has_permission(required_permission, user_id):
        """Verifica si un usuario tiene un permiso específico."""
        permissions = UserService.get_permissions_of(user_id)
        return required_permission in permissions

    @staticmethod
    def get_permissions_of(user_id):
        """Obtiene los permisos de un usuario."""
        user = UserService.get_user_by_id(user_id, include_deleted=True, include_blocked=True)
        user_permissions = RolePermission.query.filter_by(role_id=user.role_id).all()
        permissions = [up.permission.name for up in user_permissions]
        return permissions
    
    @staticmethod
    def create_admin_user():
        """Crea un usuario admin con rol de 'System Admin' si no existe."""
        admin_alias = AdminData.alias
        admin_password = AdminData.password
        admin_role_id = RoleService.get_role_by_name(name=AdminData.role_name).id
        employee_admin_id = EmployeeService.get_employee_by_email(email=AdminData.email).id
    
        admin_user = UserService.create_user(
            employee_id=employee_admin_id,
            alias=admin_alias,
            password=admin_password, 
            activo=True,
            role_id=admin_role_id
        )
        return admin_user


