import uuid

from flask import current_app, Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import or_
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)
from flask_mail import Message

from moxart import db, jwt, mail
from moxart.models.user import User

bp = Blueprint('auth', __name__)

blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@bp.route('/register', methods=['POST'])
def signup_user():
    data = request.get_json()

    username = data.get('username', None)
    email = data.get('email', None)
    password = data.get('password', None)

    if not username or not email or not password or \
            not User.query.filter(or_(User.username == username, User.email == email)):
        return jsonify(status=400, msg="some arguments missing"), 400

    user = User(username=username, email=email, password=password, admin=False)

    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=username, expires_delta=False)
    refresh_token = create_refresh_token(identity=username)

    return jsonify(status=201, message="the user has been successfully created",
                   access_token=access_token, refresh_token=refresh_token), 201


@bp.route('/login', methods=['POST'])
def login_user():
    current_user = get_jwt_identity()
    if not request.is_json:
        return jsonify(msg="request is not json"), 400

    data = request.get_json()

    username = data.get('username', None)
    password = data.get('password', None)

    user = User.query.filter_by(username=username).first()

    if not username or not password or not user or not check_password_hash(user.password, password):
        return jsonify(status=400, msg="user authentication invalid"), 400

    access_token = create_access_token(identity=username, expires_delta=False)
    refresh_token = create_refresh_token(identity=username)

    return jsonify(status=200, msg="user has been authenticated successfully",
                   access_token=access_token, refresh_token=refresh_token, current_user=current_user), 200


@bp.route('/token/refresh', methods=['POST'])
@jwt_refresh_token_required
def token_refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    return jsonify(status=200, refresh=True, access_token=access_token,
                   msg="the refresh token has been successfully refreshed"), 200


@bp.route('/logout', methods=['DELETE'])
@jwt_required
def logout_user():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)

    return jsonify(status=200, logout=True, msg="user has been successfully logged out"), 200
