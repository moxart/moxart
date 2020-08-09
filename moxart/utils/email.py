from flask import render_template
from flask_mail import Message

from moxart import mail

# BLOCK UTILS
from moxart.utils.token import (
    generate_confirmation_token, confirm_token,
    decrypt_me, encrypt_me
)
# END BLOCK UTILS

def send_me(user_email, title, sender, username):
    token = generate_confirmation_token(user_email)

    email = Message(title, sender=sender, recipients=[user_email])
    email.html = render_template('layouts/email/confirm.html', token=token, username=username)

    mail.send(email)

    return True
    