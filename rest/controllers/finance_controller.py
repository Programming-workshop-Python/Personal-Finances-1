from flask import Blueprint, request
from flask_login import login_required

from rest.services import finance_service

finance = Blueprint('finance', __name__)


@finance.route('/coming', methods=['POST'])
@login_required
def add_coming():
    return finance_service.add_coming(request)


@finance.route('/outgo', methods=['POST'])
@login_required
def add_outgo():
    return finance_service.add_outgo(request)


@finance.route('/balance')
@login_required
def get_balance():
    return finance_service.get_balance(request)


@finance.route('/outgo', methods=['POST'])
@login_required
def add_category():
    return finance_service.add_category(request)