"""Flask Application"""

from flask import Flask

from src.blueprints.auth import auth

app = Flask(__name__)

app.register_blueprint(auth)
