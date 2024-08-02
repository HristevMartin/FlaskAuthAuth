from flask import jsonify

from managers.auth import auth
from werkzeug.exceptions import BadRequest, Forbidden

def permission_required(permission):
    def wrapper(func):
        def decorate_func(*args, **kwargs):
            user = auth.current_user()
            if not user['role'] == permission.value:
                return jsonify({'message': 'You do not have access to this resource'}), 403
            return func(*args,**kwargs)
        return decorate_func
    return wrapper