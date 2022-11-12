from marshmallow import EXCLUDE, Schema, ValidationError, fields, validate


class CreateUserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int()
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    # TODO: Iterate over enum.
    deposit = fields.Int()
    role = fields.Str(required=True, validate=[validate.OneOf(["seller", "buyer"])])


class GETUserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int()
    username = fields.Str(required=True)
    # TODO: Iterate over enum.
    deposit = fields.Int()
    role = fields.Str(required=True, validate=[validate.OneOf(["seller", "buyer"])])


class GetUserTokenSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    username = fields.Str(required=True)
    password = fields.Str(required=True)


class UserTokenSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int()
    token = fields.Str(required=True)


def validate_cost(cost):
    if cost % 5 == 0:
        return cost
    raise ValidationError("Cost must be a multiple of 5.")


class ProductSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int()
    product_name = fields.Str(required=True)
    cost = fields.Float(required=True, validate=[validate_cost])
    amount_available = fields.Int()


class EditProductSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    product_name = fields.Str(allow_none=False)
    cost = fields.Float(required=False, allow_none=False, validate=[validate_cost])
    amount_available = fields.Int()


class DepositSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    deposit = fields.Int(required=True, validate=[validate.OneOf([5, 10, 20, 50, 100])])


class BuyProductSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(required=True)
    quantity = fields.Int(required=True)
