from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError

from moxart import db, jwt
from moxart.models.user import User
from moxart.models.user import UserSchema

bp = Blueprint('dashboard_user', __name__, url_prefix='/dashboard')


@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.order_by('registered_at').all()
    schema = UserSchema(many=True)
    result = schema.dump(users)

    return jsonify(data=result), 200


@bp.route('/user/<username>', methods=['DELETE'])
def remove_user(username):
    user = User.query.filter_by(username=username).first()

    db.session.delete(user)
    db.session.commit()

    return jsonify(msg="Hello")
