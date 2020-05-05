from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(UserMixin, db.Model):
    __bind_key__ = 'finances'
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True)
    email = db.Column(db.String(40),
                      unique=True,
                      nullable=False)
    password = db.Column(db.String(200),
                         unique=False,
                         nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class FinanceAccount(db.Model):
    __bind_key__ = 'finances'
    __tablename__ = 'finance_account'

    id = db.Column(db.Integer,
                   primary_key=True)
    count = db.Column(db.Float,
                      nullable=False)
    operation_date = db.Column(db.TIMESTAMP,
                               nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


class Category(db.Model):
    __bind_key__ = 'finances'
    __tablename__ = 'category'

    id = db.Column(db.Integer,
                   primary_key=True)
    category_name = db.Column(db.String(40),
                              nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
