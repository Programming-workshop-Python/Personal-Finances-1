from datetime import datetime

from flask import jsonify, abort
from flask_login import current_user

from rest.models.models import FinanceAccount
from app import db


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

    coming = FinanceAccount(
        user_id=user_id,
        count=balance,
        operation_date=now
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

    coming = FinanceAccount(
        user_id=user_id,
        count=balance,
        operation_date=now
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


def get_operation_list():
    user_id = str(current_user.id)

    operations = FinanceAccount.query.filter_by(
        user_id=user_id
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
