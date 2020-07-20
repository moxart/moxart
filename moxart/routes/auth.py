import uuid

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)

from moxart import db, jwt
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

    if username is None or email is None or password is None:
        return jsonify({
            "msg": "some arguments missing"
        }), 400

    if db.session.query(User).filter(or_(
            User.username == username, User.email == email
    )).first():
        return jsonify({
            "msg": "the user already exists, "
                   "please choose an another username or email address".format(username)
        }), 400

    hashed_password = generate_password_hash(password, method='sha256')

    new_user = User(public_id=uuid.uuid4(), username=username, email=email,
                    password=hashed_password, admin=False)

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=username, expires_delta=False)
    refresh_token = create_refresh_token(identity=username)

    return jsonify({
        "status": "success",
        "msg": "the user {} has been successfully created".format(username),
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 201


@bp.route('/login', methods=['POST'])
def login_user():
    if not request.is_json:
        return jsonify({"msg": "request is not json"}), 400

    data = request.get_json()

    username = data.get('username', None)
    password = data.get('password', None)

    if username is None or password is None:
        return jsonify({"msg": "some arguments missing"}), 400

    user = User.query.filter_by(username=username).first()

    if user is None or not check_password_hash(user.password, password):
        return jsonify({"msg": "bad username or password"}), 400

    access_token = create_access_token(identity=username, expires_delta=False)
    refresh_token = create_refresh_token(identity=username)

    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


@bp.route('/token/refresh', methods=['POST'])
@jwt_refresh_token_required
def token_refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    return jsonify({
        "status": "success",
        "refresh": True,
        "access_token": access_token,
        "msg": "the refresh token has been successfully refreshed"
    })


@bp.route('/logout', methods=['DELETE'])
@jwt_required
def logout_user():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)

    return jsonify({
        "status": "success",
        "logout": True,
        "msg": "successfully logged out"
    }), 200
