from functools import wraps
from flask import abort
from flask_jwt import current_identity
from .models import Permission
import logging


def permission_required(perm):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            logging.debug(current_identity.role.permissions)
            if not current_identity.can(perm):
                abort(401)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
