import connexion
import os
import pytest

from config import drone_api
from db_config import db
from models.drone_model import Drone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


drone_test_api = connexion.FlaskApp(__name__)
# setting in memory database for testing
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    os.path.join(drone_api.root_path, 'database/test.db')
drone_test_api.app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
drone_test_api.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(drone_test_api.app)
drone_test_api.add_api('../../swagger/swagger.yml')


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


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(drone_test_api.app.config["SQLALCHEMY_DATABASE_URI"])
    db.Model.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    db.Model.metadata.drop_all(engine)


def fill_drones(db_session):
    drone_1 = Drone("LNVotKpL0QmcHjvwJeTz", "Lightweight")
    drone_2 = Drone("QF8bnGItdpWoVP7NPdS4crPS9LckPbuzidr0FvKuS8y", "Middleweight")
    drone_3 = Drone("HTU8L8SO2Xx3EYmkKAz4iuFBY2gAo", "Cruiserweight")
    drone_4 = Drone("Z0S24fHgbvjFpbgTscsX32JfuXcMDBZrOk", "Heavyweight")

    db_session.add(drone_1)
    db_session.add(drone_2)
    db_session.add(drone_3)
    db_session.add(drone_4)
    db_session.commit()


def test_add_a_medication(db_session):

    fill_drones(db_session)
    with drone_test_api.app.app_context():
        drone = Drone.query.filter_by(serial_number="LNVotKpL0QmcHjvwJeTz").first()
        stored_and_not_stored = drone.add_medication([medicaments[0]])
        assert len(stored_and_not_stored["stored"]) == 1
        assert len(stored_and_not_stored["not_stored"]) == 0
        assert stored_and_not_stored["stored"][0].name == medicaments[0]["name"]
        assert stored_and_not_stored["stored"][0].weight == medicaments[0]["weight"]
        assert stored_and_not_stored["stored"][0].code == medicaments[0]["code"]
        assert stored_and_not_stored["stored"][0].status == "LOADED"


def test_add_two_medications(db_session):

    fill_drones(db_session)
    with drone_test_api.app.app_context():
        drone = Drone.query.filter_by(
            serial_number="QF8bnGItdpWoVP7NPdS4crPS9LckPbuzidr0FvKuS8y")\
            .first()
        stored_and_not_stored = drone.add_medication(medicaments)

        assert len(stored_and_not_stored["stored"]) == 2
        assert len(stored_and_not_stored["not_stored"]) == 1

        assert stored_and_not_stored["stored"][0].name == medicaments[0]["name"]
        assert stored_and_not_stored["stored"][0].weight == medicaments[0]["weight"]
        assert stored_and_not_stored["stored"][0].code == medicaments[0]["code"]
        assert stored_and_not_stored["stored"][0].status == "LOADED"

        assert stored_and_not_stored["stored"][1].name == medicaments[2]["name"]
        assert stored_and_not_stored["stored"][1].weight == medicaments[2]["weight"]
        assert stored_and_not_stored["stored"][1].code == medicaments[2]["code"]
        assert stored_and_not_stored["stored"][1].status == "LOADED"

        assert stored_and_not_stored["not_stored"][0]["name"] == medicaments[1]["name"]
        assert stored_and_not_stored["not_stored"][0]["weight"] == medicaments[1]["weight"]
        assert stored_and_not_stored["not_stored"][0]["code"] == medicaments[1]["code"]

def test_add_cero_medications(db_session):

    fill_drones(db_session)
    with drone_test_api.app.app_context():
        drone = Drone.query.filter_by(
            serial_number="HTU8L8SO2Xx3EYmkKAz4iuFBY2gAo")\
            .first()
        stored_and_not_stored = drone.add_medication([medicaments[3]])

        assert len(stored_and_not_stored["stored"]) == 0
        assert len(stored_and_not_stored["not_stored"]) == 1

        assert stored_and_not_stored["not_stored"][0]["name"] == medicaments[3]["name"]
        assert stored_and_not_stored["not_stored"][0]["weight"] == medicaments[3]["weight"]
        assert stored_and_not_stored["not_stored"][0]["code"] == medicaments[3]["code"]

