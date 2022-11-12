from flask import request

from app import csrf, db
from app.decorators import all_scope, buyer_scope, seller_scope
from app.models import Product, User
from app.operations import delete_model_operation, update_data_operation
from app.responses import no_content, not_found
from app.schemas import BuyProductSchema, EditProductSchema, ProductSchema
from app.utils import coin_change

from . import api


@api.route("/product", methods=["GET"])
@all_scope
@csrf.exempt
def list_products(user_id):
    products = Product.query.all()
    return ProductSchema().dump(products, many=True)


@api.route("/product/<int:id>", methods=["GET"])
@all_scope
@csrf.exempt
def get_product(user_id, id):
    product = Product.query.get(id)
    return ProductSchema().dump(product)


@api.route("/product", methods=["POST"])
@seller_scope
@csrf.exempt
def create_product(user_id):
    data = ProductSchema().load(request.get_json())
    data["seller_id"] = user_id
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    return ProductSchema().dump(product)


@api.route("/product/<int:id>", methods=["PUT"])
@seller_scope
@csrf.exempt
def edit_product(user_id, id):
    data = EditProductSchema().load(request.get_json())
    product = update_data_operation(
        Product, query={"id": id, "seller_id": user_id}, data=data, session=db.session
    )
    return ProductSchema().dump(product)


@api.route("/product/<int:id>", methods=["DELETE"])
@seller_scope
@csrf.exempt
def delete_product(user_id, id):
    delete_model_operation(
        Product, query={"id": id, "seller_id": user_id}, session=db.session
    )
    return no_content()


@api.route("/buy", methods=["POST"])
@buyer_scope
@csrf.exempt
def buy_product(user_id):
    data = BuyProductSchema().load(request.get_json())
    user = User.query.get(user_id)
    product = Product.query.get(data["id"])
    if not product:
        return not_found(msg=f"No product exists with ID: {data['id']}")
    user_budget = user.deposit
    total_cost = product.cost * data["quantity"]
    over_budget = total_cost > user_budget
    quantity_available = product.amount_available
    low_inventory = quantity_available < data["quantity"]
    if over_budget:
        money_needed = int(total_cost - user_budget)
        return f"Please deposit {money_needed} to make this purchase."
    if low_inventory:
        return f" Not enough products. Current inventory is: {quantity_available}."

    amount_change = int(user_budget - total_cost)
    product.amount_available = quantity_available - data["quantity"]
    user.deposit = 0
    db.session.commit()

    # Convert to list of coins.
    change = coin_change(amount_change)

    return {
        "change": change,
        "total_cost": total_cost,
        "product_id": product.id,
        "product_name": product.product_name,
    }
