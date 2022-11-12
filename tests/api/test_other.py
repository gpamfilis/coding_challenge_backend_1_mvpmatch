import pytest

deposits = [5, 10, 20, 50, 100]
bad_deposits = [1, 4, 499, 2, 3]


def test_buy_endpoint(test_client, seller, buyer, product, init_database):

    _ = test_client.post("/api/user", json=seller)
    seller_token = test_client.post("/api/user/token", json=seller).json["token"]
    product_response = test_client.post(
        f"/api/product?token={seller_token}", json=product
    )
    product_id = product_response.json["id"]

    _ = test_client.post("/api/user", json=buyer)
    buyer_token = test_client.post("/api/user/token", json=buyer).json["token"]

    buy_response = test_client.post(
        f"/api/buy?token={buyer_token}", json={"id": product_id, "quantity": 3}
    )
    data = buy_response.json
    assert data["product_id"] == product_id
    assert data["total_cost"] == 90
    assert isinstance(data["change"], list)
    assert 10 in data["change"]


@pytest.mark.parametrize("deposit", deposits)
def test_deposit_endpoint(test_client, buyer, init_database, deposit):
    _ = test_client.post("/api/user", json=buyer)
    token_response = test_client.post("/api/user/token", json=buyer)
    token = token_response.json["token"]
    response_deposit = test_client.put(
        f"/api/deposit?token={token}", json={"deposit": deposit}
    )
    assert response_deposit.json["deposit"] == buyer["deposit"] + deposit


@pytest.mark.parametrize("deposit", bad_deposits)
def test_bad_deposit_endpoint(test_client, buyer, init_database, deposit):
    _ = test_client.post("/api/user", json=buyer)
    token_response = test_client.post("/api/user/token", json=buyer)
    token = token_response.json["token"]
    response_deposit = test_client.put(
        f"/api/deposit?token={token}", json={"deposit": deposit}
    )
    assert response_deposit.status_code == 422
