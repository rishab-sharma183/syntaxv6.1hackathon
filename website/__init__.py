from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .proxyfix import SaferProxyFix
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "111111111"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.wsgi_app = SaferProxyFix(app.wsgi_app)

    from .views import views

    app.register_blueprint(views, url_prefix="/")

    return app
