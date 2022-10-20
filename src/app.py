"""Flask Application"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from config import Config

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
ma = Marshmallow()

# Import routes
from src.blueprints.auth import auth
from src.models import User, InvalidToken

class App:
    """Flask Application"""

    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)

        db.init_app(self.app)
        jwt.init_app(self.app)
        cors.init_app(self.app)
        migrate.init_app(self.app, db)

        self.app.register_blueprint(auth, url_prefix='/api/auth')

    def run(self):
        """Run Flask Application"""
        self.app.run(debug=True)
# app = Flask(__name__)
# app.register_blueprint(auth, url_prefix='/auth')


