from datetime import datetime

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

