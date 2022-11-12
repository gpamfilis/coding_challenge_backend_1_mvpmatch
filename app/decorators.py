import os
from functools import partial, wraps

from flask import request
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.errors import AuthenticationError, TokenError
from app.models import User


def verify_auth_token_return_id(token):
    s = Serializer(os.getenv("SECRET_KEY"))
    try:
        data = s.loads(token)
        if "user_id" in data:
            model = User.query.get(data["user_id"])
            return model.role, model.id
            raise AuthenticationError("Invalid Token.")
    except SignatureExpired:
        raise AuthenticationError("Your token has expired. Please try again.")
    except BadSignature:
        raise AuthenticationError("Invalid Token.")


def token_required(f, scopes=[]):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.args.get("token", None, str)
        role, id = verify_auth_token_return_id(token)
        if role in scopes:
            kwargs["user_id"] = id
        if role not in scopes:
            raise TokenError("Not allowed.")
        return f(*args, **kwargs)

    return decorator


seller_scope = partial(token_required, scopes=["seller"])
buyer_scope = partial(token_required, scopes=["buyer"])
all_scope = partial(token_required, scopes=["seller", "buyer"])
