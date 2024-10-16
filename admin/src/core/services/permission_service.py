from src.core.database import db
from src.core.services.role_service import RoleService
from src.core.models.user.permission import Permission
from src.core.models.user.role_permission import RolePermission
from src.core.admin_data import AdminData
from src.core.enums.permission_enums import PermissionCategory, PermissionModel

class PermissionService:

    @staticmethod
    def create_permission(name):
        """Crea un permiso y lo enlaza automáticamente con el rol del Admin, a menos que ya exista."""
        try:
            existing_permission = PermissionService.get_permission_by_name(name)
        except ValueError as e:  
            permission = Permission(name=name)
            db.session.add(permission)
            db.session.commit()

            admin_role = RoleService.get_role_by_name(AdminData.role_name)
            PermissionService.link_permission_to_role(permission.id, admin_role.id)
            
            return permission

        raise ValueError(f"El permiso '{name}' ya existe.")
    
    @staticmethod
    def get_permission_by_id(permission_id):
        """Obtiene un permiso por su ID y lanza un error si no existe."""
        existing_permission = Permission.query.get(permission_id)
        if existing_permission is None:
            raise ValueError(f"No existe permiso con el ID ingresado: '{permission_id}'")
        return existing_permission

    @staticmethod
    def get_permission_by_name(name):
        """Obtiene un permiso por su nombre y lanza un error si no existe."""
        existing_permission = Permission.query.filter_by(name=name).first()
        if existing_permission is None:
            raise ValueError(f"No existe permiso con el nombre ingresado: '{name}'")
        return existing_permission

    @staticmethod
    def link_permission_to_role(permission_id, role_id):
        """Enlaza un permiso con un rol."""
        # Verificar que el permiso y el rol existan
        permission = PermissionService.get_permission_by_id(permission_id)
        role = RoleService.get_role_by_id(role_id)
        
        # Verificar si la relación ya existe
        existing_relation = RolePermission.query.filter_by(permission_id=permission_id, role_id=role_id).first()
        if existing_relation:
            raise ValueError(f"El permiso '{permission.name}' ya está enlazado con el rol '{role.name}'.")

        # Crear la relación
        role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
        db.session.add(role_permission)
        db.session.commit()
        
        return role_permission

    @staticmethod
    def create_initial_permissions():
        """Crea los permisos iniciales y los enlaza automáticamente al rol de AdminData."""
        for category in PermissionCategory:
            for model in PermissionModel:
                permission_name = f"{model.value}_{category.value}"
                PermissionService.create_permission(permission_name)