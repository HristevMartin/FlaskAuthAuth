from flask import jsonify

from managers.auth import auth
from werkzeug.exceptions import BadRequest, Forbidden

# def permission_required(*permissions):
#     def wrapper(func):
#         def decorated_function(*args, **kwargs):
#             user = auth.current_user()
#             # Check if the user's role is among the permitted roles
#             if user['role'] not in [permission.value for permission in permissions]:
#                 return {'message': 'You do not have access to this resource'}, 403
#             return func(*args, **kwargs)
#         return decorated_function
#     return wrapper


def permission_required(*permissions):
    def wrapper(func):
        def decorated_function(*args, **kwargs):
            user = auth.current_user()
            required_permissions = {permission.value for permission in permissions}

            user_roles = set(user['role']) if isinstance(user['role'], list) else {user['role']}

            if not required_permissions.issubset(user_roles):
                return {'message': 'You do not have access to this resource'}, 403
            return func(*args, **kwargs)

        return decorated_function

    return wrapper

