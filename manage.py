import os

from dotenv import load_dotenv
from flask_migrate import Migrate

from app import create_app, db

load_dotenv()

environment = os.getenv("FLASK_ENV")

app = create_app(environment)

migrate = Migrate(app, db, compare_type=True)

if __name__ == "__main__":
    app.run(port=5000)
