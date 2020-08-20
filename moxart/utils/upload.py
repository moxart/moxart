import os
from sqlalchemy.exc import IntegrityError
from flask import current_app, jsonify


# initializing user upload directory
def init_client_upload_dir(base_dir, user):
    try:
        os.makedirs(os.path.join(base_dir, user))

    except FileExistsError:
        print("you can not execute modifying operation on existing files")
