from enum import Enum
from os import environ

class AdminData(): # TODO: Cambiar esto para que sea seguro
    role_name = environ.get('SYSADMIN_ROLE_NAME') if environ.get('SYSADMIN_ROLE_NAME') is not None else 'System Admin'
    alias = environ.get('SYSADMIN_ADMIN') if environ.get('SYSADMIN_ADMIN') is not None else 'admin'
    password = environ.get('SYSADMIN_PASSWORD') if environ.get('SYSADMIN_PASSWORD') is not None else 'DEFAULT_password1234' 
    email = environ.get('SYSADMIN_EMAIL') if environ.get('SYSADMIN_EMAIL') is not None else 'admin@gmail.com' 
