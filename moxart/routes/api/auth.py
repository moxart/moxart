import uuid

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

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
    if request.method == 'POST':
        data = request.get_json()

        hashed_password = generate_password_hash(data['password'], method='sha256')

        new_user = User(username=data['username'],
                        email=data['email'], password=hashed_password, admin=False)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "user has been successfully created!"})


@bp.route('/user/<id>', methods=['PUT'])
def edit_user(id):
    return 'Edit User'


@bp.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    return 'del_user'
