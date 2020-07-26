from functools import wraps
from flask import current_app, jsonify
from flask_jwt_extended import (
    get_jwt_identity, verify_jwt_in_request, get_jwt_claims
)

from moxart.models.user import User


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        verify_jwt_in_request()

        claims = get_jwt_claims()

        if claims['roles'] != 'admin':
            return jsonify(msg="you don't have permission to access this endpoint"), 403
        else:
            return fn(*args, **kwargs)

    return wrapper


def is_confirmed(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()

        user = User.query.filter_by(username=current_user).first()

        if user and user.confirmed is False:
            return jsonify(status=401, msg="please confirm your account")

        return fn(*args, **kwargs)

    return wrapper
