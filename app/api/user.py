from flask import jsonify, request

from app import csrf, db
from app.decorators import buyer_scope
from app.errors import (
    AuthenticationError,
    ResourceDoesNotExistError,
    ResourceExistsError,
)
from app.models import User
from app.schemas import (
    CreateUserSchema,
    DepositSchema,
    GETUserSchema,
    GetUserTokenSchema,
    UserTokenSchema,
)
from app.utils import coin_change

from . import api


def logout_user(data):
    username = data["username"]
    user = User.query.filter_by(username=username).first()
    if user is None:
        raise ResourceDoesNotExistError()
    elif user.verify_password(data["password"]):
        user.is_loggedin = False
        db.session.add(user)
        db.session.commit()
        return user


def generate_user_token(data):
    username = data["username"]
    user = User.query.filter_by(username=username).first()
    if user is None:
        raise ResourceDoesNotExistError()
    if user.is_loggedin and user.verify_password(data["password"]):
        raise AuthenticationError(
            f"User {username} is already logged in. Please logout and re issue your token."
        )
    elif user.verify_password(data["password"]):
        user.is_loggedin = True
        db.session.add(user)
        db.session.commit()
        return user


@api.route("/user", methods=["POST"])
@csrf.exempt
def create_user():
    data = CreateUserSchema().load(request.get_json())
    user = User.query.filter_by(username=data["username"]).first()
    if user:
        raise ResourceExistsError(
            f"User with username: `{data['username']}` already exists."
        )
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return GETUserSchema().dump(user), 201


@api.route("/user", methods=["GET"])
@csrf.exempt
def list_users():
    users = User.query.all()
    return GETUserSchema().dump(users, many=True)


@api.route("/user/token", methods=["POST"])
@csrf.exempt
def user_token():
    data = GetUserTokenSchema().load(request.get_json(force=True))
    user = generate_user_token(data)
    return jsonify(UserTokenSchema().dump(user))


@api.route("/deposit", methods=["PUT"])
@buyer_scope
@csrf.exempt
def user_deposit(user_id):
    data = DepositSchema().load(request.get_json(force=True))
    user = User.query.get(user_id)
    new_deposit = user.deposit + data["deposit"]
    user.deposit = new_deposit
    db.session.add(user)
    db.session.commit()
    return jsonify(GETUserSchema().dump(user))


@api.route("/reset", methods=["POST"])
@buyer_scope
@csrf.exempt
def rest_deposit(user_id):
    user = User.query.get(user_id)
    money_returned = coin_change(user.deposit)
    user.deposit = 0
    db.session.add(user)
    db.session.commit()
    return jsonify({"deposit": 0, "change": money_returned})


@api.route("user/logout/all", methods=["POST"])
@csrf.exempt
def logout_user_route():
    data = GetUserTokenSchema().load(request.get_json(force=True))
    logout_user(data)
    return "User has been logged out."
