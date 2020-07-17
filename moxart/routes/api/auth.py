import uuid

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from moxart import db
from moxart.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/api')


@bp.route('/users', methods=['GET'])
def get_users():
    return 'users'


@bp.route('/user/<id>', methods=['GET'])
def get_user(id):
    return 'user_id'


@bp.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()

    username = data.get('username', None)
    email = data.get('email', None)
    password = data.get('password', None)

    if username is None or email is None or password is None:
        return jsonify({"msg": "some arguments missing."}), 400

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"msg": "the username '{}' already exists.".format(username)}), 400
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"msg": "the email '{}' already exists.".format(email)}), 400

    hashed_password = generate_password_hash(password, method='sha256')

    new_user = User(public_id=uuid.uuid4(), username=username, email=email,
                    password=hashed_password, admin=False)

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=username)

    return jsonify({
        "status": "success",
        "msg": "the user '{}' has been successfully created.".format(username),
        "access_token": access_token
    }), 201


@bp.route('/user/<id>', methods=['PUT'])
def edit_user(id):
    return 'Edit User'


@bp.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    return 'del_user'
