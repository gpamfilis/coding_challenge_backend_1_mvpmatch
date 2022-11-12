import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

ENV = os.getenv("FLASK_ENV")
print("USING ENV: ", ENV)
load_dotenv()


class Config:
    def __init__(self):
        pass

    SECRET_KEY = os.getenv("SECRET_KEY")
    CORS_ALLOW_ORIGIN = "*"
    CORS_ALLOW_METHODS = "OPTIONS, GET, POST, PUT, DELETE"
    CORS_ALLOW_HEADERS = "Content-Type, Accept, Authorization, access_token"
    CORS_EXPOSE_HEADERS = "access_token"
    SECURITY_PASSWORD_SALT = "my_precious_two"
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    INTERNAL_URL = "127.0.0.1:5000"
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "test.db")


config = {
    "testing": TestingConfig,
    "development": DevelopmentConfig,
}
