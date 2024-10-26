from enum import Enum
class PermissionCategory(Enum):
    INDEX = "index"
    NEW = "new"
    UPDATE = "update"
    DESTROY = "destroy"
    SHOW = "show"
    BLOCK = "block"

class PermissionModel(Enum):
    USER = "user"
    COLLECTION = "collection"
    EMPLOYEE = "employee"
    CLIENT = "client"
    PAYMENT = "payment"
    EQUESTRIAN = "equestrian"
