from core.enums.user_roles import UserRoles
from src.core.models.user import User
from src.core.models.user.user_permission import UserPermission
from src.core.database import db
from enum import Enum
import re

class UserOrderBy(Enum):
    CREATED_AT = 'created_at'
    EMAIL = 'email'

class UserService:
    
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
    def validate_role(role):
        """Verifica que el rol no sea admin, a menos que este no exista."""
        if role != UserRoles.SYSTEM_ADMIN: 
            return
    
        admin_alias = "admin" 
        existing_admin = UserService.get_user_by_alias(alias=admin_alias, include_deleted=True)
        if existing_admin:
            raise ValueError("No se puede crear un usuario con el rol 'SYSTEM_ADMIN' porque ya existe el usuario ADMIN.")

    @staticmethod
    def create_user(empleado_id, alias, password, role, activo=True):
        """Crea un nuevo usuario."""
        UserService.validate_password(password)
        UserService.validate_role(role)

        user = User(
            empleado_id=empleado_id,
            alias=alias,
            password=password,
            activo=activo,
            roles=role
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update_user(user_id, alias=None, password=None, activo=None, role=None):
        """Actualiza un usuario existente."""
        user = UserService.get_user_by_id(user_id)
        if user:
            if alias is not None:
                user.alias = alias
            if password is not None:
                UserService.validate_password(password)
                user.password = password
            if activo is not None:
                user.activo = activo
            if role is not None:
                UserService.validate_role(role)
                user.roles = role 
            db.session.commit()
        return user
    
    @staticmethod
    def delete_user(user_id):
        """Elimina un usuario por su ID de forma lógica."""
        user = UserService.get_user_by_id(user_id)
        if user:
            user.deleted = True
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_user_by_id(user_id, include_deleted=False):
        """Obtiene un usuario por su ID."""
        if include_deleted:
            return User.query.get(user_id)
        return User.query.filter_by(id=user_id, deleted=False).first()

    @staticmethod
    def get_user_by_alias(alias, include_deleted=False):
        """Obtiene un usuario por su alias."""
        if include_deleted:
            return User.query.filter_by(alias=alias).first()
        return User.query.filter_by(alias=alias, deleted=False).first()

    @staticmethod
    def get_all_users(include_deleted=False):
        """Obtiene todos los usuarios."""
        if include_deleted:
            return User.query.all()
        return User.query.filter_by(deleted=False).all()
    
    from flask_sqlalchemy import Pagination

    @staticmethod
    def search_users(email=None, activo=None, rol=None, page=1, per_page=25, order_by='created_at', ascending=True):
        """Busca usuarios por email, activo, y rol con paginación y ordenamiento."""
        query = User.query.filter(User.deleted == False) 

        if email:
            query = query.filter(User.empleado.has(email=email)) 

        if activo is not None:
            query = query.filter(User.activo == activo)

        if rol:
            query = query.filter(User.roles == rol)

        if order_by not in ['email', 'created_at']:
            raise ValueError("El campo de ordenamiento debe ser 'email' o 'created_at'.")

        if ascending:
            query = query.order_by(getattr(User, order_by).asc())
        else:
            query = query.order_by(getattr(User, order_by).desc())

        pagination = query.paginate(page, per_page, error_out=True)
        
        return pagination.items, pagination.total, pagination.pages


    @staticmethod
    def user_has_permission(required_permission, user_id):
        """Verifica si un usuario tiene un permiso específico."""
        permissions = UserService.get_permissions_of(user_id)
        return required_permission in permissions

    @staticmethod
    def get_permissions_of(user_id):
        """Obtiene los permisos de un usuario."""
        user_permissions = UserPermission.query.filter_by(user_id=user_id).all()
        permissions = [up.permission.name for up in user_permissions]
        return permissions
    
    @staticmethod
    def create_admin_user():
        """Crea un usuario admin con rol de 'System Admin' si no existe."""
        admin_alias = 'admin'
        admin_password = 'DEFAULT_password1234' # TODO: Cambiar esto a una contraseña segura
        existing_admin = UserService.get_user_by_alias(alias=admin_alias)
        

        if existing_admin is None:
            #TODO: Crear empleado para user_admin create_admin_employee

            admin_user = UserService.create_user(
                empleado_id=0,  # TODO: Revisar esto mas adelante
                alias=admin_alias,
                password=admin_password, 
                activo=True,
                role=UserRoles.SYSTEM_ADMIN
            )
            return admin_user
        return existing_admin


