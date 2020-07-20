import uuid

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from moxart import db
from moxart.models.post import Post
from moxart.models.post import PostSchema

bp = Blueprint('post', __name__, url_prefix='/api')


@bp.route('/post', methods=['POST'])
@jwt_required
def new_post():
    current_user = get_jwt_identity()

    data = request.get_json()

    user_public_id = data.get('user_public_id', None)
    title = data.get('title', None)
    content = data.get('content', None)

    if user_public_id is None or title is None or content is None:
        return jsonify({
            "msg": "some arguments missing"
        }), 400

    post = Post(user_public_id=user_public_id, title=title, content=content)

    db.session.add(post)
    db.session.commit()

    return jsonify({
        "status": "success",
        "msg": "post has been successfully published"
    }), 201
