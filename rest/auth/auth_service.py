from app import db
from flask import jsonify, abort
from flask_login import current_user, login_user, logout_user

from rest.models.users import User


def logout():
    logout_user()
    return jsonify(success=True)


def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


def get_user():
    return jsonify(id=current_user.id, email=current_user.email)


def sign_up(request):
    email = request.json.get('email')
    password = request.json.get('password')
    existing_user = User.query.filter_by(email=email).first()
    if existing_user is None:
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return jsonify(success=True)
    return abort(400, 'message=A user already exists with that email address.')


def login(request):
    if current_user.is_authenticated:
        return jsonify(id=current_user.id, email=current_user.email)

    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password=password):
        login_user(user)
        return jsonify(id=current_user.id, email=current_user.email)
    return abort(401, 'message=Invalid username/password combination')
