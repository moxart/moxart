import os
import datetime
import imghdr

from flask import current_app, Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity

from moxart import db

from moxart.models.user import User

bp = Blueprint('upload', __name__)


@bp.route('/upload', methods=['POST'])
@jwt_required
def upload_file():
    current_user = get_jwt_identity()
    current_base = current_app.config['UPLOAD_BASE_PATH']
    current_date = str(datetime.datetime.now().strftime('%Y/%m/'))

    for file in request.files.getlist('file'):
        filename, ext = os.path.splitext(file.filename)

        if ext.lower() not in tuple(current_app.config['UPLOAD_VALID_FILE']):
            return jsonify(status=400, msg="some uploaded files has not valid type"), 400

        save_path = os.path.join(current_base + current_user, current_date)

        if not os.path.exists(save_path):
            os.makedirs(os.path.join(save_path))

        file.save(save_path + secure_filename(file.filename))

    return jsonify(status=200, msg="file has been uploaded successfully"), 200
