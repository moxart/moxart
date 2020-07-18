import uuid

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

from moxart import db
from moxart.models.user import User
from moxart.models.user import UserSchema

bp = Blueprint('user', __name__, url_prefix='/api')


@bp.route('/users', methods=['POST'])
@jwt_required
def get_users():
    current_user = get_jwt_identity()

    all_users = User.query.all()

    schema = UserSchema(many=True)
    result = schema.dump(all_users)
    return jsonify({
        "status": "success",
        "logged_in_as": current_user,
        "data": result
    }), 200


@bp.route('/user/<public_id>', methods=['GET'])
@jwt_required
def get_user(public_id):
    current_user = get_jwt_identity()

    user_by_public_id = User.query.filter_by(public_id=public_id).first()

    if user_by_public_id is None:
        return jsonify({
            "status": "not found",
            "msg": "user not found"
        })

    schema = UserSchema()
    result = schema.dump(user_by_public_id)
    return jsonify({
        "status": "success",
        "logged_in_as": current_user,
        "data": result
    }), 200


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

    user_by_public_id = User.query.filter_by(public_id=public_id).first()

    if user_by_public_id is None:
        return jsonify({
            "status": "not found",
            "msg": "user not found"
        })

    user_by_public_id.email = email
    user_by_public_id.username = username
    user_by_public_id.first_name = first_name
    user_by_public_id.last_name = last_name
    user_by_public_id.password = hashed_password
    user_by_public_id.bio = bio

    db.session.commit()

    return jsonify({
        "status": "success",
        "msg": "user has been successfully updated"
    }), 200


@bp.route('/user/<public_id>', methods=['DELETE'])
@jwt_required
def delete_user(public_id):
    user_by_public_id = User.query.filter_by(public_id=public_id).first()

    if user_by_public_id is None:
        return jsonify({
            "status": "not found",
            "msg": "user not found"
        })

    db.session.delete(user_by_public_id)
    db.session.commit()

    return jsonify({
        "status": "success",
        "msg": "user has been successfully deleted"
    }), 200
