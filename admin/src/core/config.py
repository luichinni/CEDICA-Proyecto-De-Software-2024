import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

class Config(object):
    TESTING = False
    SECRET_KEY= os.environ.get('SECRET_KEY_PASS') if os.environ.get('SECRET_KEY_PASS') is not None else 'my_precious' # "my_precious"
    SESSION_TYPE= "filesystem"
    SESSION_PERMANENT= False

class ProductionConfig(Config):
    DB_USER = os.environ.get('DATABASE_USERNAME')
    DB_PASSWORD = os.environ.get('DATABASE_PASSWORD')
    DB_HOST = os.environ.get('DATABASE_HOST')
    DB_PORT = os.environ.get('DATABASE_PORT')
    DB_NAME = os.environ.get('DATABASE_NAME')
    SQLALCHEMY_DATABASE_URI = (f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

class DevelopmentConfig(Config):
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    SQLALCHEMY_DATABASE_URI = (f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

class TestingConfig(Config):
    TESTING = True

config = {
    "development" : DevelopmentConfig,
    "production" : ProductionConfig,
    "testing" : TestingConfig
}