import connexion
import json
import os
import pytest

from config import drone_api
from db_config import db
from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import from_regex, sampled_from


drone_test_api = connexion.FlaskApp(__name__)
drone_test_api.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                    os.path.join(drone_api.root_path, 'database/drone__test_db.db') 
drone_test_api.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(drone_test_api.app)
drone_test_api.add_api('../../swagger/swagger.yml')


@pytest.fixture(autouse=True)
def client():
    with drone_test_api.app.test_client() as c:
        yield c


@given(td_serial_number=from_regex(r'^[a-zA-Z0-9]{7,100}$'), \
    td_modelo=sampled_from( \
        ["Lightweight", "Middleweight", "Cruiserweight", "Heavyweight"]))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_register_drone(client, td_serial_number, td_modelo):

    register_response = client.get("/register_drone", data=json.dumps(dict(
        serial_number=td_serial_number,
        model=td_modelo
    )), mimetype='application/json')

    # get_response = client.get("/get_drone/" + register_response, mimetype='application/json')

    # assert(register_response["data"] == get_response["data"])
