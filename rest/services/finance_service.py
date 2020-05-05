from datetime import datetime

from flask import jsonify, abort
from flask_login import current_user
from sqlalchemy import and_

from app import db
from rest.models.models import FinanceAccount
from rest.services.category_service import get_category_by_id


def create_account(user_id):
    now = datetime.now()
    account = FinanceAccount(user_id=user_id,
                             count=0,
                             operation_date=now)
    db.session.add(account)
    db.session.commit()
    return account.id


def add_coming(request):
    now = datetime.now()
    user_id = str(current_user.id)
    current_balance = get_current_balance(user_id)
    balance = current_balance + request.json['count']

    category = get_category_by_id(request.json['category_id'])
    category_id = None
    if category is not None:
        category_id = category.id

    coming = FinanceAccount(
        user_id=user_id,
        count=balance,
        operation_date=now,
        category_id=category_id
    )

    db.session.add(coming)
    db.session.commit()

    return jsonify(
        get_operation_response(coming)
    )


def add_outgo(request):
    now = datetime.now()
    user_id = str(current_user.id)
    current_balance = get_current_balance(user_id)
    balance = current_balance - request.json['count']
    if balance < 0:
        abort(400, 'Operation limit exceeded.')

    category = get_category_by_id(request.json['category_id'])
    category_id = None
    if category is not None:
        category_id = category.id

    coming = FinanceAccount(
        user_id=user_id,
        count=balance,
        operation_date=now,
        category_id=category_id
    )

    db.session.add(coming)
    db.session.commit()

    return jsonify(
        get_operation_response(coming)
    )


def get_balance():
    user_id = str(current_user.id)
    balance = get_current_balance(user_id)

    return jsonify({'balance': balance})


def get_operation_list(request):
    user_id = str(current_user.id)
    from_time = request.args.get('from_time')
    to_time = request.args.get('to_time')

    operations = FinanceAccount.query.filter(and_(
        FinanceAccount.operation_date.between(from_time, to_time)), (FinanceAccount.user_id == user_id)
    ).order_by(
        FinanceAccount.operation_date.desc()
    ).all()

    return jsonify([
        get_operation_response(operation) for operation in operations
    ])


def get_current_balance(user_id):
    balance = FinanceAccount.query.filter_by(
        user_id=user_id
    ).order_by(
        FinanceAccount.operation_date.desc()
    ).first()

    return balance.count


def get_operation_response(operation):
    return {
        'id': operation.id,
        'date': operation.operation_date
    }
