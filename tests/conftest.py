import pytest

from app import create_app, db


@pytest.fixture()
def seller():
    return {
        "username": "seller1",
        "password": "12345",
        "role": "seller",
    }


@pytest.fixture()
def buyer():
    return {
        "username": "buyer1",
        "password": "123456",
        "deposit": 100,
        "role": "buyer",
    }


@pytest.fixture()
def product():
    return {"product_name": "product 1", "cost": 30, "amount_available": 10}


@pytest.fixture(scope="module")
def test_client():
    # Create a Flask app configured for testing
    flask_app = create_app("testing")

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(autouse=True)
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    # user1 = User(email='patkennedy79@gmail.com', password_plaintext='FlaskIsAwesome')
    # user2 = User(email='kennedyfamilyrecipes@gmail.com', password_plaintext='PaSsWoRd')
    # db.session.add(user1)
    # db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()

    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join('/tmp', "test.db")
    # os.remove(os.path.join('/tmp', "test.db"))


@pytest.fixture(scope="module")
def cli_test_client():
    flask_app = create_app()
    flask_app.config.from_object("config.TestingConfig")

    runner = flask_app.test_cli_runner()

    yield runner  # this is where the testing happens!
