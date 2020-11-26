import uuid

from functools import wraps
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    jwt_required, verify_jwt_in_request, get_jwt_claims, get_jwt_identity
)

from moxart import db, jwt
from moxart.models.user import User
from moxart.models.user import UserSchema

from moxart.utils.decorator import admin_required, is_confirmed

bp = Blueprint('user', __name__, url_prefix='/api')


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user = User.query.filter_by(username=identity).first()

    if user.admin == 1:
        return {'roles': 'admin'}
    else:
        return {'roles': 'guest'}


@bp.route('/users', methods=['POST'])
@admin_required
def get_users():
    current_user = get_jwt_identity()

    users = User.query.all()

    schema = UserSchema(many=True)
    result = schema.dump(users)

    return jsonify(result), 200


@bp.route('/user/<public_id>', methods=['GET'])
@jwt_required
@is_confirmed
def get_user(public_id):
    current_user = get_jwt_identity()

    user = User.query.filter_by(user_public_id=public_id).first()

    if user is None:
        return jsonify(status=404, msg="user not found")

    schema = UserSchema()
    result = schema.dump(user)

    return jsonify(status=200, logged_in_as=current_user, data=result), 200


@bp.route('/user/<public_id>', methods=['PUT'])
def edit_user(public_id):
    data = request.get_json()

    email = data.get('email', None)
    username = data.get('username', None)
    first_name = data.get('first_name', None)
    last_name = data.get('last_name', None)
    password = data.get('password', None)
    bio = data.get('bio', None)

    hashed_password = generate_password_hash(password, method='sha256')

    user = User.query.filter_by(user_public_id=public_id).first()

    if user is None:
        return jsonify(status=404, msg="user not found"), 404

    user.email = email
    user.username = username
    user.first_name = first_name
    user.last_name = last_name
    user.password = hashed_password
    user.bio = bio

    db.session.commit()

    return jsonify(status=200, msg="user has been successfully updated"), 200


@bp.route('/user/<public_id>', methods=['DELETE'])
@jwt_required
def delete_user(public_id):
    user = User.query.filter_by(user_public_id=public_id).first()

    if user is None:
        return jsonify(status=404, msg="user not found"), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify(status=200, msg="user has been successfully deleted")
