from app import app
from rest.auth.auth_controller import auth

from rest.controllers.finance_controller import finance

if __name__ == '__main__':
    app.register_blueprint(auth)
    app.register_blueprint(finance)
    app.run(host='0.0.0.0', port=8080, debug=True)
