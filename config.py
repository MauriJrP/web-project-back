import os
from dotenv import load_dotenv

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(ROOT_DIR, '.env'))

class Config(object):
    """ Retain all config variables """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(ROOT_DIR, 'app.db'))
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or "super-secret-key"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    
class ProdConfig(Config):
    """ Product config variables """
    DEBUG = False
    TESTING = False
    FLASK_ENV = 'production'

class DevConfig(Config):
    """ Development config variables """
    DEBUG = True
    TESTING = True
    FLASK_ENV = 'development'