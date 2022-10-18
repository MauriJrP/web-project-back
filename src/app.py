"""Flask Application"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from src.blueprints.auth import auth

from config import Config

cors = CORS()
db = SQLAlchemy()
jwt = JWTManager()

class App:
    """Flask Application"""

    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)

        db.init_app(self.app)
        jwt.init_app(self.app)
        cors.init_app(self.app)

        self.app.register_blueprint(auth, url_prefix='/auth')

    def run(self):
        """Run Flask Application"""
        self.app.run()
# app = Flask(__name__)
# app.register_blueprint(auth, url_prefix='/auth')

