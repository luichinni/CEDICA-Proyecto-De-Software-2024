from core.enums.permission_enums import PermissionCategory, PermissionModel
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
    def get_all_roles(include_admin=False):
        """Obtiene todos los roles."""
        query = Role.query
        if not include_admin:
            query = query.filter(Role.name != AdminData.role_name)
        return query.all()
    
    @staticmethod
    def create_admin_role():
        """Crea el rol 'System Admin' si no existe."""
        return RoleService.create_role(AdminData.role_name)
        
    @staticmethod
    def create_example_roles():
        from core.services.permission_service import PermissionService
        permisos = dict()
        for category in PermissionCategory:
            for model in PermissionModel:
                if category == PermissionCategory.BLOCK and model != PermissionModel.USER: continue
                nombre = f"{model.value}_{category.value}"
                permisos[nombre] = PermissionService.get_permission_by_name(nombre).id
                
        RoleService.create_role("Usuario a confirmar por admin").id
        
        """Crea roles base con sus respectivos permisos."""
        tecnica = RoleService.create_role("Técnica").id
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CLIENT.value}_{PermissionCategory.INDEX.value}"],tecnica)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CLIENT.value}_{PermissionCategory.SHOW.value}"],tecnica)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CLIENT.value}_{PermissionCategory.UPDATE.value}"],tecnica)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CLIENT.value}_{PermissionCategory.NEW.value}"],tecnica)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CLIENT.value}_{PermissionCategory.DESTROY.value}"],tecnica)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.COLLECTION.value}_{PermissionCategory.INDEX.value}"],tecnica)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.COLLECTION.value}_{PermissionCategory.SHOW.value}"],tecnica)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.INDEX.value}"],tecnica)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.SHOW.value}"],tecnica)
        
        ecuestre = RoleService.create_role("Ecuestre").id
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.INDEX.value}"],ecuestre)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.SHOW.value}"],ecuestre)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.UPDATE.value}"],ecuestre)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.NEW.value}"],ecuestre)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.DESTROY.value}"],ecuestre)
        
        administracion = RoleService.create_role("Administración").id
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.INDEX.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.SHOW.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.UPDATE.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.NEW.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.EMPLOYEE.value}_{PermissionCategory.DESTROY.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.PAYMENT.value}_{PermissionCategory.INDEX.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.PAYMENT.value}_{PermissionCategory.SHOW.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.PAYMENT.value}_{PermissionCategory.UPDATE.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.PAYMENT.value}_{PermissionCategory.NEW.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.PAYMENT.value}_{PermissionCategory.DESTROY.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CLIENT.value}_{PermissionCategory.INDEX.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CLIENT.value}_{PermissionCategory.SHOW.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CLIENT.value}_{PermissionCategory.UPDATE.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CLIENT.value}_{PermissionCategory.NEW.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CLIENT.value}_{PermissionCategory.DESTROY.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.COLLECTION.value}_{PermissionCategory.INDEX.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.COLLECTION.value}_{PermissionCategory.SHOW.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.COLLECTION.value}_{PermissionCategory.UPDATE.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.COLLECTION.value}_{PermissionCategory.NEW.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.COLLECTION.value}_{PermissionCategory.DESTROY.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.INDEX.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.EQUESTRIAN.value}_{PermissionCategory.SHOW.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CONTENT.value}_{PermissionCategory.INDEX.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CONTENT.value}_{PermissionCategory.SHOW.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CONTENT.value}_{PermissionCategory.UPDATE.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CONTENT.value}_{PermissionCategory.NEW.value}"],administracion) 
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CONTENT.value}_{PermissionCategory.DESTROY.value}"],administracion)    
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CONTACT.value}_{PermissionCategory.INDEX.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CONTACT.value}_{PermissionCategory.SHOW.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CONTACT.value}_{PermissionCategory.UPDATE.value}"],administracion)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CONTACT.value}_{PermissionCategory.NEW.value}"],administracion) 
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CONTACT.value}_{PermissionCategory.DESTROY.value}"],administracion)  
    
        voluntariado = RoleService.create_role("Voluntariado").id # no tiene permisos de nada

        editor = RoleService.create_role("Editor").id
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CONTENT.value}_{PermissionCategory.INDEX.value}"],editor)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CONTENT.value}_{PermissionCategory.SHOW.value}"],editor)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CONTENT.value}_{PermissionCategory.UPDATE.value}"],editor)
        PermissionService.link_permission_to_role(permisos[f"{PermissionModel.CONTENT.value}_{PermissionCategory.NEW.value}"],editor)
        

