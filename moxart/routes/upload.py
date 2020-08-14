from flask import current_app, Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from moxart import db

from moxart.models.user import User

bp = Blueprint('upload', __name__)


@bp.route('/upload', methods=['POST'])
def upload_file():
    f = request.files['file']
    f.save(secure_filename(f.filename))

    return 'file uploaded successfully'

