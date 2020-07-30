from flask import current_app, jsonify
from itsdangerous import URLSafeTimedSerializer


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )

    except(ValueError, KeyError, TypeError) as error:
        return jsonify(error=error)

    return email


def encrypt_email_address(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def decrypt_email_address(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    return serializer.loads(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
