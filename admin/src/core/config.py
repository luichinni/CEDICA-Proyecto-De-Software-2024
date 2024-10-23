from os import environ
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

class Config(object):
    TESTING = False
    SECRET_KEY= environ.get('SECRET_KEY_PASS','my_precious') # "my_precious"
    SESSION_TYPE= "filesystem"
    SESSION_PERMANENT= False

class ProductionConfig(Config):
    MINIO_SERVER = environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET = environ.get("MINIO_SECRET")
    MINIO_SECURE = True
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 60,
        "pool_pre_ping": True,
    }

class DevelopmentConfig(Config):
    DB_USER = environ.get('DB_USER')
    DB_PASSWORD = environ.get('DB_PASSWORD')
    DB_HOST = environ.get('DB_HOST')
    DB_PORT = environ.get('DB_PORT')
    DB_NAME = environ.get('DB_NAME')
    SQLALCHEMY_DATABASE_URI = (f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    MINIO_SERVER = environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET = environ.get("MINIO_SECRET")
    MINIO_SECURE = False

class TestingConfig(Config):
    TESTING = True

config = {
    "development" : DevelopmentConfig,
    "production" : ProductionConfig,
    "testing" : TestingConfig
}