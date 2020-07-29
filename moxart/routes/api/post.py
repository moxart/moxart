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
    data = request.get_json()

    user_public_id = data.get('user_public_id', None)
    category_public_id = data.get('category_public_id', None)
    title = data.get('title', None)
    content = data.get('content', None)

    if user_public_id is None or category_public_id is None or title is None or content is None:
        return jsonify(status=400, msg="some arguments missing")

    post = Post(user_public_id=user_public_id, category_public_id=category_public_id,
                title=title, content=content)

    db.session.add(post)
    db.session.commit()

    return jsonify(status=201, msg="post has been successfully published"), 201


@bp.route('/post/<uuid:post_public_id>')
def get_post(post_public_id):
    post = Post.query.filter_by(post_public_id=post_public_id).first()

    if not post:
        return jsonify(status=404, msg="post not found"), 404

    schema = PostSchema()
    result = schema.dump(post)

    return jsonify(status=200, data=result), 200


@bp.route('/posts', methods=['GET'])
def get_all_posts():
    posts = Post.query.all()

    schema = PostSchema(many=True)
    result = schema.dump(posts)

    return jsonify(status=200, data=result), 200
