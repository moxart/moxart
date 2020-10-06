import os

HOST = 'localhost'
PORT = 5000

SECRET_KEY = 'this-is-secret-key'
SECURITY_PASSWORD_SALT = 'this-is-security-password-salt'

JWT_SECRET_KEY = 'this-is-jwt-secret-key'
JWT_BLACKLIST_ENABLED = False
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
JWT_TOKEN_LOCATION = ['cookies']
JWT_COOKIE_CSRF_PROTECT = False

JSON_SORT_KEYS = False

ADMIN_USERNAME = 'moxart'
ADMIN_PASSWORD = 'password'
ADMIN_EMAIL = 'your gmail address'

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'your gmail address'
MAIL_PASSWORD = 'app password generated'
MAIL_DEFAULT_SENDER = 'your gmail address'
MAIL_USE_TLS = True
MAIL_USE_SSL = False

UPLOAD_PARENT_PATH = 'uploads/'
UPLOAD_BASE_PATH = os.path.join('./', UPLOAD_PARENT_PATH)
UPLOAD_VALID_FILE = ['.jpg', '.jpeg', '.png', '.gif', '.zip', '.tar.gz', '.rar']
