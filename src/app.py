"""Flask Application"""

import logging
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os
from config import DevConfig, ProdConfig

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
ma = Marshmallow()

# Import routes
from src.blueprints.auth import auth


class App:
    """Flask Application"""

    def __init__(self):
        self.app = Flask(__name__)

        env = os.getenv('ENVIRONMENT', 'dev')
        if env == 'dev':
            self.app.config.from_object(DevConfig)
        else:
            self.app.config.from_object(ProdConfig)

        db.init_app(self.app)
        jwt.init_app(self.app)
        cors.init_app(self.app, resources={r"/api/*": {"origins": "*"}},)
        migrate.init_app(self.app, db)
        logging.getLogger('flask_cors').level = logging.DEBUG

        self.app.register_blueprint(auth, url_prefix='/api/auth')

    def run(self):
        """Run Flask Application"""
        self.app.run(debug=True)


