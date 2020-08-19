from flask import render_template, jsonify
from flask_mail import Message

from sqlalchemy.exc import IntegrityError

from moxart import mail

from moxart.utils.token import (
    generate_confirmation_token, confirm_token,
    decrypt_me, encrypt_me
)


def send_verification_link(user_email, title, sender, tmpl, username):
    try:
        token = generate_confirmation_token(user_email)

        email = Message(title, sender=sender, recipients=[user_email])
        email.html = render_template(tmpl, token=token, username=username)

        mail.send(email)
    except IntegrityError:
        return jsonify(status=400, msg="registration confirmation email could not be sent"), 400
