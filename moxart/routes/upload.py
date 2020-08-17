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
    current_date = datetime.datetime.now().strftime('%Y/%m/')
    current_img = request.files['file']

    valid_extension = [
        tuple(current_app.config['UPLOAD_VALID_IMAGE']),
        tuple(current_app.config['UPLOAD_VALID_FILE'])
    ]

    if not current_img.filename.lower().endswith((valid_extension[0] + valid_extension[1])):
        return 'file is not valid type'

    target_path = os.path.join(os.path.join(
        current_app.config['UPLOAD_BASE_PATH'],
        current_app.config['UPLOAD_CLIENT_PATH']),
        current_user + '/photos/' + str(current_date)
    )

    if not os.path.exists(target_path):
        os.makedirs(os.path.join(target_path))

    f = request.files['file']
    f.save(target_path + secure_filename(f.filename))

    return 'file uploaded successfully'
