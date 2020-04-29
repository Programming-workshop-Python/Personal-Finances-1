from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret key'

app.config['SQLALCHEMY_BINDS'] = {'finances': 'sqlite:///:memory:'}

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
