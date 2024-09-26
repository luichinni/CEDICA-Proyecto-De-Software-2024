import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')
class Config(object):
    TESTING = False

class ProductionConfig(Config):
    pass

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