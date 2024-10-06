from src.core.database import db
from src.core.models.user.role import Role
from src.core.models.user.permission import Permission
from src.core.models.user.role_permission import RolePermission
from src.core.admin_data import AdminData

class PermissionService:

    @staticmethod
    def create_permission(name):
        """Crea un permiso y lo enlaza automáticamente con el rol del Admin."""
        existing_permission = Permission.query.filter_by(name=name).first()
        if existing_permission:
            raise ValueError(f"El permiso '{name}' ya existe.")
        
        permission = Permission(name=name)
        db.session.add(permission)
        db.session.commit()

        admin_role = Role.query.filter_by(name=AdminData.role_name).first()
        if admin_role:
            PermissionService.link_permission_to_role(permission.id, admin_role.id)
        else:
            raise ValueError(f"El rol '{AdminData.role_name}' no existe para enlazar el permiso.")
        
        return permission

    @staticmethod
    def get_permission_by_id(permission_id):
        """Obtiene un permiso por su ID."""
        return Permission.query.get(permission_id)

    @staticmethod
    def get_permission_by_name(name):
        """Obtiene un permiso por su nombre."""
        return Permission.query.filter_by(name=name).first()

    @staticmethod
    def link_permission_to_role(permission_id, role_id):
        """Enlaza un permiso con un rol."""
        # Verificar que el permiso y el rol existan
        permission = Permission.query.get(permission_id)
        role = Role.query.get(role_id)
        if not permission:
            raise ValueError(f"El permiso con ID {permission_id} no existe.")
        if not role:
            raise ValueError(f"El rol con ID {role_id} no existe.")
        
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
    def create_example_permissions():
        """Crea permisos de ejemplo y los enlaza automáticamente al rol de AdminData."""
        PermissionService.create_permission("user_index")
        PermissionService.create_permission("user_show")
        PermissionService.create_permission("user_new")
        PermissionService.create_permission("user_update")
        PermissionService.create_permission("user_destroy")
