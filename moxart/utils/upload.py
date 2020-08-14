import os

from flask import current_app, jsonify


# initializing user upload directory
def init_client_upload_dir(base_dir, client_dir, sub_dirs, which_user=None):
    if os.path.exists(os.path.join(base_dir, client_dir)) and \
            os.path.isdir(os.path.join(base_dir, client_dir)):
        for dir_name in sub_dirs:
            os.makedirs(os.path.join(base_dir + '/' + client_dir + '/' + which_user, dir_name))
