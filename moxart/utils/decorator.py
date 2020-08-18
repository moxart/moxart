import os

from functools import wraps
from flask import current_app, request, jsonify
from flask_jwt_extended import (
    get_jwt_identity, verify_jwt_in_request, get_jwt_claims
)

from moxart.models.user import User


# def check_file_extension(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         filename, ext = os.path.splitext(request.files['file'].filename)
#         exts = current_app.config['UPLOAD_VALID_IMAGE']
#
#         if ext not in exts:
#             return jsonify(status=403, msg="file type is not valid")
#
#         return fn(*args, **kwargs)
#
#     return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        verify_jwt_in_request()

        claims = get_jwt_claims()

        if claims['roles'] != 'admin':
            return jsonify(msg="you don't have permission to access this endpoint"), 403

        return fn(*args, **kwargs)

    return wrapper


def is_confirmed(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()

        user = User.query.filter_by(username=current_user).first()

        if user and user.confirmed is False:
            return jsonify(status=401, msg="please confirm your account"), 401

        return fn(*args, **kwargs)

    return wrapper
