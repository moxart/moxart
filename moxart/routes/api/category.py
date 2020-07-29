import uuid

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from moxart import db
from moxart.models.category import Category
from moxart.models.category import CategorySchema

bp = Blueprint('category', __name__, url_prefix='/api')


@bp.route('/category', methods=['POST'])
@jwt_required
def new_category():
    data = request.get_json()

    category_name = data.get('category_name', None)

    if category_name is None:
        return jsonify(status=400, msg="some arguments missing")

    category = Category(category_name=category_name)

    db.session.add(category)
    db.session.commit()

    return jsonify(status=201, msg="category has been successfully created"), 201


@bp.route('/category/<uuid:category_public_id>')
def get_post(category_public_id):
    category = Category.query.filter_by(category_public_id=category_public_id).first()

    if not category:
        return jsonify(status=404, msg="post not found"), 404

    schema = CategorySchema()
    result = schema.dump(category)

    return jsonify(status=200, data=result), 200


@bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()

    schema = CategorySchema(many=True)
    result = schema.dump(categories)

    return jsonify(status=200, data=result), 200



