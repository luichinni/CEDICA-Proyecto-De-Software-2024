from src.core.models.user.role import Role
from src.core.database import db
from src.core.admin_data import AdminData

class RoleService:

    @staticmethod
    def create_role(name):
        existing_role = Role.query.filter_by(name=name).first()
        if existing_role:
            raise ValueError(f"El rol '{name}' ya existe.")
        
        role = Role(name=name)
        db.session.add(role)
        db.session.commit()
        return role

    @staticmethod
    def get_role_by_id(role_id):
        return Role.query.get(role_id)

    @staticmethod
    def get_role_by_name(name):
        return Role.query.filter_by(name=name).first()

    @staticmethod
    def create_admin_role():
        """Crea el rol 'System Admin' si no existe."""
        return RoleService.create_role(AdminData.role_name)
        