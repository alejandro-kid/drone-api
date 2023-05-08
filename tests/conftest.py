import connexion
import os
import pytest


from config import drone_api  # noqa: F401
from db_config import db
from sqlalchemy import create_engine

from models.drone_model import Drone
from models.medicine_model import Medication


DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_NAME_TEST = os.getenv("DB_NAME_TEST", "drone-api-test")
DB_HOST = os.getenv("DB_HOST", "localhost")

drone_api_test = connexion.FlaskApp(__name__)
drone_api_test.app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://" + f"{DB_PASS}:{DB_USER}@{DB_HOST}/{DB_NAME_TEST}"
)
drone_api_test.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
drone_api_test.app.config["SECRET_KEY"] = "mysecret"
db.init_app(drone_api_test.app)
drone_api_test.add_api('../swagger/swagger.yml')

#Test data
medicaments = [
    {
        "name": "eKmT7xC-Toy8zqtRyAaU_K",
        "weight": 102.0,
        "code": "3PW0N9XO8VKN4RYF11F6Q5ZMI2N3BDFSHV33"
    },
    {
        "name": "IWYcE_9gqI",
        "weight": 200.0,
        "code": "J32NRQBL8QG02W03L1X"
    },
    {
        "name": "e4GiFm4ot-X9-1wKAoF",
        "weight": 198.0,
        "code": "PGX0W3H80FJAVYUC_SD1LG5YOTEI4Y9WGL7CJDVHU"
    },
    {
        "name": "POF3KuKdBiBnsZqs2UOgIu",
        "weight": 449.0,
        "code": "U2TRSUT5LRDQ9K"
    }, 
    
]

def fill_drones():
    drone_1 = Drone("LNVotKpL0QmcHjvwJeTz", "Lightweight")
    drone_2 = Drone("QF8bnGItdpWoVP7NPdS4crPS9LckPbuzidr0FvKuS8y", "Middleweight")
    drone_3 = Drone("HTU8L8SO2Xx3EYmkKAz4iuFBY2gAo", "Cruiserweight")
    drone_4 = Drone("Z0S24fHgbvjFpbgTscsX32JfuXcMDBZrOk", "Heavyweight")

    db.session.add(drone_1)
    db.session.add(drone_2)
    db.session.add(drone_3)
    db.session.add(drone_4)
    db.session.commit()

@pytest.fixture
def app():
    app = drone_api_test.app
    engine = create_engine(drone_api_test.app.config["SQLALCHEMY_DATABASE_URI"])
    db.Model.metadata.create_all(engine)

    #Data test
    with app.app_context():
        fill_drones()

    yield app
    db.Model.metadata.drop_all(engine)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
