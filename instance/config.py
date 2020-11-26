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

# For MAIL_PASSWORD Go to the settings for your Google Account in the application or device you are trying to set up.
# Replace your password with the 16-character password shown above.
MAIL_PASSWORD = 'app password'
MAIL_DEFAULT_SENDER = 'sender gmail address'
MAIL_USE_TLS = True
MAIL_USE_SSL = False

UPLOAD_PARENT_PATH = 'uploads/'
UPLOAD_BASE_PATH = os.path.join('./', UPLOAD_PARENT_PATH)
UPLOAD_VALID_FILE = ['.jpg', '.jpeg', '.png', '.gif', '.zip', '.tar.gz', '.rar']
