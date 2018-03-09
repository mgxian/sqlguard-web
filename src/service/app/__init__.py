from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt import JWT
from flask_mail import Mail
from config import config

db = SQLAlchemy()
ma = Marshmallow()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)

    from app.token.jwt import authenticate, identify
    JWT(app, authenticate, identify)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
