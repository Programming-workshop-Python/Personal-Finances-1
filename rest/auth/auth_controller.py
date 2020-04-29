from flask import request, Blueprint, abort
from flask_login import login_required

from app import login_manager
from rest.auth import auth_service

auth = Blueprint('auth', __name__)


@auth.route('/logout')
@login_required
def logout():
    return auth_service.logout()


@auth.route('/me')
@login_required
def get_user():
    return auth_service.get_user()


@auth.route('/signup', methods=['POST'])
def signup():
    return auth_service.sign_up(request)


@auth.route('/login', methods=['POST'])
def login():
    return auth_service.login(request)


@login_manager.user_loader
def load_user(user_id):
    return auth_service.load_user(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return abort(403)
