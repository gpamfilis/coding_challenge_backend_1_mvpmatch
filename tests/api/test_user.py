def test_create_seller(test_client, seller, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.post("/api/user", json=seller)
    assert response.status_code == 201


def test_create_buyer(test_client, buyer, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.post("/api/user", json=buyer)
    assert response.status_code == 201
