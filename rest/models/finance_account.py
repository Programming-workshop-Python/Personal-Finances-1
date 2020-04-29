from sqlalchemy.orm import relationship

from app import db


class FinanceAccount(db.Model):
    __bind_key__ = 'finances'
    __tablename__ = 'finance_account'

    id = db.Column(db.Integer,
                   primary_key=True)
    count = db.Column(db.Float,
                      nullable=False)
    operation_date = db.Column(db.Date,
                               nullable=False)
    user_id = relationship("User",
                           uselist=False,
                           back_populates="account_id")
