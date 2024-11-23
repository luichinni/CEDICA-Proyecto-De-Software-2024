from enum import Enum
class PermissionCategory(Enum):
    INDEX = "index"
    NEW = "new"
    UPDATE = "update"
    DESTROY = "destroy"
    SHOW = "show"
    BLOCK = "block"

class PermissionModel(Enum):
    USER = "users"
    COLLECTION = "collections"
    EMPLOYEE = "employees"
    CLIENT = "clients"
    PAYMENT = "payments"
    EQUESTRIAN = "equestrians"
    CONTENT = "publications"
    CONTACT = "contact"
