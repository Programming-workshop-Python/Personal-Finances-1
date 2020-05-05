from flask import Blueprint, request
from flask_login import login_required

from rest.services import category_service

category = Blueprint('category', __name__)


@category.route('/category', methods=['POST'])
@login_required
def add_category():
    category_service.add_category(request)


@category.route('/category', methods=['GET'])
@login_required
def get_category():
    category_service.get_category()
