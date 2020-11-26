import uuid

from datetime import datetime
from flask import current_app, Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from moxart import db

from moxart.models.user import User

from moxart.utils.email import send_verification_link
from moxart.utils.token import confirm_token

bp = Blueprint('confirm', __name__)


@bp.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    try:
        email = confirm_token(token)

    except(ValueError, KeyError, TypeError) as error:
        return jsonify(status=401, msg='the confirmation link is invalid or has expired', error=error), 401

    user = User.query.filter_by(email=email).first()

    if user.confirmed:
        return jsonify(status=200, msg="account already confirmed. Please login"), 200

    user.confirmed = True
    user.confirmed_at = datetime.utcnow()

    db.session.commit()

    return jsonify(status=200, msg="you have confirmed your account"), 200


@bp.route('/unconfirmed')
@jwt_required
def unconfirmed():
    current_user = get_jwt_identity()

    user = User.query.filter_by(username=current_user).first()

    if user and user.confirmed == 1:
        return jsonify(status=200, msg="you are logged in"), 200

    return jsonify(status=401, msg="please confirm your account"), 401


@bp.route('/resend/confirm', methods=['POST'])
@jwt_required
def resend_confirmation():
    current_user = get_jwt_identity()

    user = User.query.filter_by(username=current_user).first()

    if not user or user.confirmed is True:
        return jsonify(status=200, msg="account already confirmed. Please login"), 200

    if send_verification_link(user.email, "Email Confirmation", current_app.config['MAIL_DEFAULT_SENDER'],
               "layouts/email/confirm.html", user.username):
        return jsonify(status=200, msg="a new confirmation email has been sent"), 200


@bp.route('/send/token', methods=['POST'])
def send_reset_token():
    data = request.get_json()

    email = data.get('email', None)

    user = User.query.filter_by(email=email).first()

    if send_verification_link(email, "Please Reset Your Password", current_app.config['MAIL_DEFAULT_SENDER'],
               "layouts/email/send-reset-link.html", user.username):
        return jsonify(status=200, msg="If your email is valid, an email will be sent to you")
    return jsonify(status=401, msg="something is not right")


@bp.route('/reset/password/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json()

    password = data.get('password', None)

    hashed_password = generate_password_hash(password, method='sha256')

    if not token or not password:
        return jsonify(status=401, msg="some arguments missing"), 401

    try:
        email = confirm_token(token)
    except(ValueError, KeyError, TypeError) as error:
        return jsonify(status=401, msg="the token link is invalid or has expired", error=error), 401

    user = User.query.filter_by(email=email).first()

    user.password = hashed_password

    db.session.commit()

    return jsonify(status=200, msg="your password has been reset successfully")
