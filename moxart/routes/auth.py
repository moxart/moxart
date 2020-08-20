import uuid

from datetime import datetime
from flask import current_app, Blueprint, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt,
    set_access_cookies, set_refresh_cookies,
    unset_jwt_cookies
)
from moxart import db, jwt
from moxart.utils.email import send_verification_link
from moxart.utils.upload import init_client_upload_dir
from moxart.models.user import User

bp = Blueprint('auth', __name__)

blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']

    return jti in blacklist


@bp.route('/register', methods=['POST'])
def signup_user():
    try:
        username = request.json.get('username', None)
        email = request.json.get('email', None)
        password = request.json.get('password', None)

        if not username or not email or not password:
            return jsonify(status=400, msg="some arguments missing"), 400

        hashed_password = generate_password_hash(password, method='sha256')

        user = User(username=username, email=email, password=hashed_password, admin=False, confirmed=False)

        if not user:
            return jsonify(status=400, msg="user registration is not completed successfully"), 400

        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=username, expires_delta=False)
        refresh_token = create_refresh_token(identity=username)

        resp = jsonify(status=201, register=True, msg="user has been authenticated successfully",
                       access_token=access_token, refresh_token=refresh_token, current_email=email)

        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)

        init_client_upload_dir(current_app.config['UPLOAD_BASE_PATH'], username)
        send_verification_link(email, 'Email Confirmation', current_app.config['MAIL_DEFAULT_SENDER'],
                               'layouts/email/confirm.html', username)

        return resp, 201

    except IntegrityError:
        db.session.rollback()

        return jsonify(status=400, register=False,
                       msg="username or email address already exists please choose another")
    except AttributeError:
        return jsonify(status=400, register=False,
                       msg="request body should be json format"), 400


@bp.route('/login', methods=['POST'])
def login_user():
    try:
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username or not password:
            return jsonify(status=400, msg="some arguments missing"), 400

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify(status=400, msg="user authentication invalid"), 400

        access_token = create_access_token(identity=username, expires_delta=False)
        refresh_token = create_refresh_token(identity=username)

        resp = jsonify(status=200, login=True, msg="user has been authenticated successfully",
                       access_token=access_token, refresh_token=refresh_token)

        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)

        return resp, 200
    except IntegrityError:
        return jsonify(status=400, login=False, msg="user authentication invalid"), 400

    except AttributeError:
        return jsonify(status=400, login=False, msg="request body should be json format"), 400


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
