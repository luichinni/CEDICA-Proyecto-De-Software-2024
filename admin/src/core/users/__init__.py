


def user_has_permission(required_permission, user_id):
    if (user_id == 0): return True # TODO: borrar esta linea cuando se implemente get_permissions_of

    permissions = get_permissions_of(user_id)
    return required_permission in permissions

def get_permissions_of(user_id):
    return [] # TODO: obtener de la tabla que relaciona el rol con los permisos