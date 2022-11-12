def setup_seller(client, seller):
    _ = client.post("/api/user", json=seller)
    seller_token = client.post("/api/user/token", json=seller).json["token"]
    return seller_token, seller


def test_create_product(test_client, seller, buyer, product, init_database):

    seller_token, seller = setup_seller(test_client, seller)

    product_response = test_client.post(
        f"/api/product?token={seller_token}", json=product
    )
    data = product_response.json
    data.pop("id")
    assert data == product


def test_get_product(test_client, seller, buyer, product, init_database):

    seller_token, seller = setup_seller(test_client, seller)

    create_product_respose = test_client.post(
        f"/api/product?token={seller_token}", json=product
    )
    data = create_product_respose.json
    product_id = data["id"]
    get_product_response = test_client.get(
        f"/api/product/{product_id}?token={seller_token}", json=product
    )
    assert get_product_response.json == create_product_respose.json


def test_edit_product(test_client, seller, buyer, product, init_database):

    seller_token, seller = setup_seller(test_client, seller)

    create_product_respose = test_client.post(
        f"/api/product?token={seller_token}", json=product
    )
    data = create_product_respose.json
    product_id = data["id"]
    put_product_response = test_client.put(
        f"/api/product/{product_id}?token={seller_token}",
        json={"amount_available": 50000},
    )

    assert put_product_response.json["amount_available"] == 50000


def test_edit_product_bad_inputs(test_client, seller, buyer, product, init_database):

    seller_token, seller = setup_seller(test_client, seller)

    create_product_respose = test_client.post(
        f"/api/product?token={seller_token}", json=product
    )
    data = create_product_respose.json
    product_id = data["id"]
    put_product_response = test_client.put(
        f"/api/product/{product_id}?token={seller_token}",
        json={"amount_available": "dsfsdfs"},
    )
    assert put_product_response.status_code == 422


def test_delete_product(test_client, seller, buyer, product, init_database):

    seller_token, seller = setup_seller(test_client, seller)

    create_product_respose = test_client.post(
        f"/api/product?token={seller_token}", json=product
    )
    data = create_product_respose.json
    product_id = data["id"]

    delete_product_response = test_client.delete(
        f"/api/product/{product_id}?token={seller_token}"
    )

    assert delete_product_response.status_code == 204
