import json

from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

from app.errors import (
    AuthenticationError,
    ResourceDoesNotExistError,
    ResourceExistsError,
    ResourceNotFoundError,
    TokenError,
    UnknownException,
)
from config import config

db = SQLAlchemy()

cors = CORS(resources={r"/api/*": {"origins": "*"}})

csrf = CSRFProtect()


def create_app(config_name):
    print("Config Name:", config_name)
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    cors.init_app(app)

    from app.api import api as api_blueprint

    app.register_blueprint(api_blueprint, url_prefix="/api")

    @app.errorhandler(ValidationError)
    def register_validation_error(error):
        app.logger.info(error)
        rv = dict(
            {
                "message": error.messages,
                "error": True,
                "redirect_url": None,
                "app_message": "",
            }
        )
        db.session.rollback()
        return rv, 422

    @app.errorhandler(ResourceExistsError)
    def dbresource_exists_error(error):
        msg = "obj exists"
        if str(error):
            msg = str(error)
        rv = dict(
            {
                "message": msg,
                "error": True,
                "redirect_url": None,
                "app_message": "",
            }
        )
        db.session.rollback()
        return rv, 409

    @app.errorhandler(ResourceDoesNotExistError)
    def dbresource_does_not_exist_error(error):
        msg = "Not found"
        if str(error):
            msg = str(error)
        rv = dict(
            {"message": msg, "error": True, "redirect_url": None, "app_message": ""}
        )
        db.session.rollback()
        return rv, 404

    @app.errorhandler(ResourceNotFoundError)
    def dbresource_does_not_found_error(error):
        msg = "Not found"
        if error:
            msg = str(error)
        rv = dict(
            {"message": msg, "error": True, "redirect_url": None, "app_message": ""}
        )
        db.session.rollback()
        return rv, 404

    @app.errorhandler(UnknownException)
    def unknown_exception(error):
        rv = dict(
            {
                "message": str(error),
                "error": True,
                "redirect_url": None,
                "app_message": "",
            }
        )
        db.session.rollback()
        return rv, 404

    @app.errorhandler(TokenError)
    def token_error(error):
        msg = "Error."
        if str(error):
            msg = str(error)

        rv = dict(
            {
                "message": msg,
                "error": True,
                "redirect_url": None,
                "app_message": "",
            }
        )
        db.session.rollback()
        return rv, 500

    @app.errorhandler(AuthenticationError)
    def authentication_error(error):
        rv = dict(
            {
                "message": str(error),
                "error": True,
                "redirect_url": None,
                "app_message": "",
            }
        )
        db.session.rollback()
        return rv, 401

    @app.errorhandler(500)
    def system_error(error):
        rv = dict(
            {
                "message": str(error),
                "error": True,
                "redirect_url": None,
                "app_message": "",
            }
        )
        db.session.rollback()
        return rv, 500

    @app.errorhandler(IntegrityError)
    def system_error(error):
        rv = dict(
            {
                "message": str(error),
                "error": True,
                "redirect_url": None,
                "app_message": "",
            }
        )
        db.session.rollback()
        return rv, 500

    return app
