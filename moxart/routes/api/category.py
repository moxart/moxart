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
        return jsonify({
            "msg": "some arguments missing"
        }), 400

    category = Category(category_name=category_name)

    db.session.add(category)
    db.session.commit()

    return jsonify({
        "status": "success",
        "msg": "the category {} has been successfully created".format(category_name)
    }), 201
