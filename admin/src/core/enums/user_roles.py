from enum import Enum

class UserRoles(Enum):
    TECNICA = 'Técnica'
    ECUSTRE = 'Ecuestre'
    VOLUNTARIADO = 'Voluntariado'
    ADMINISTRACION = 'Administración'
    SYSTEM_ADMIN = 'System Admin'

    @classmethod
    def choices(cls):
        return [(role.name, role.value) for role in cls]

    @classmethod
    def values(cls):
        return [role.value for role in cls]
