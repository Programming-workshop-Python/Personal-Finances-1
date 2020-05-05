from flask import abort, jsonify
from flask_login import current_user

from app import db
from rest.models.models import Category


def add_category(request):
    category_name = request.json['name'].lower()
    user_id = str(current_user.id)

    if not _check_category(user_id, category_name):
        abort(400, f'Category with name {category_name} exists')

    category = Category(
        category_name=category_name,
        user_id=user_id
    )

    db.session.add(category)
    db.session.commit()


def get_category():
    user_id = str(current_user.id)
    categories = Category.query.filter_by(
        user_id=user_id
    ).all()

    return jsonify([{
        'id': category.id,
        'name': category.category_name
    } for category in categories])


def get_category_by_id(category_id):
    user_id = str(current_user.id)
    return Category.query.filter_by(
        id=category_id,
        user_id=user_id
    ).limit(1)


def _check_category(user_id, category_name):
    category_number = Category.query.filter_by(
        category_name=category_name,
        user_id=user_id
    ).count()

    return True if category_number == 0 else False
