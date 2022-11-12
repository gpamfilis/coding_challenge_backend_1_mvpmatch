from flask import current_app
from flask_sqlalchemy.model import DefaultMeta
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import (  # TODO: check and see if can change the strength of the hash
    check_password_hash,
    generate_password_hash,
)

from app import db

BaseModel: DefaultMeta = db.Model


class User(BaseModel):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    deposit = db.Column(db.Integer(), default=0)
    role = db.Column(db.String(128), default="seller")
    products = db.relationship("Product", backref="user", lazy="dynamic")
    is_loggedin = db.Column(db.Boolean(), nullable=False, default=False)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=100000):
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({"user_id": self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data["id"])
        return user

    @hybrid_property
    def token(self):
        token = self.generate_auth_token()
        return token.decode("utf-8")


class Product(BaseModel):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(128))
    cost = db.Column(db.Float(), default=0.0)
    amount_available = db.Column(db.Integer(), default=0)
    seller_id = db.Column(db.Integer, db.ForeignKey("user.id"))
