from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from src.config import Config
from src.auth.app import auth
from src.models import UserModel

login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(username: str) -> object:
    user_query = UserModel.query(username)
    return user_query


def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)

    app.config.from_object(Config)

    login_manager.init_app(app)

    app.register_blueprint(auth)

    return app
