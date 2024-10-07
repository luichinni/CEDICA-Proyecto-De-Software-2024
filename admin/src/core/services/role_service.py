from src.core.models.user.role import Role
from src.core.database import db
from src.core.admin_data import AdminData

class RoleService:

    @staticmethod
    def create_role(name):
        """Crea un nuevo rol con el nombre proporcionado, a menos que ya exista."""
        try:
            existing_role = RoleService.get_role_by_name(name)
        except ValueError as e:  
            role = Role(name=name)
            db.session.add(role)
            db.session.commit()
            return role

        raise ValueError(f"El rol '{name}' ya existe.")
    
    @staticmethod
    def get_role_by_id(role_id):
        """Obtiene un rol por su ID y lanza un error si no existe."""
        existing_role = Role.query.get(role_id)
        if existing_role is None:
            raise ValueError(f"No existe rol con el ID ingresado: '{role_id}'")
        return existing_role

    @staticmethod
    def get_role_by_name(name):
        """Obtiene un rol por su nombre y lanza un error si no existe."""
        existing_role = Role.query.filter_by(name=name).first()
        if existing_role is None:
            raise ValueError(f"No existe rol con el nombre ingresado: '{name}'")
        return existing_role
    
    @staticmethod
    def get_all_roles():
        """Obtiene todos los roles."""
        return Role.query.all()

    @staticmethod
    def create_admin_role():
        """Crea el rol 'System Admin' si no existe."""
        return RoleService.create_role(AdminData.role_name)
        
    @staticmethod
    def create_example_roles():
        """Crea roles de ejemplo."""
        RoleService.create_role("Técnica")
        RoleService.create_role("Ecuestre")
        RoleService.create_role("Voluntariado")
        RoleService.create_role("Administración")