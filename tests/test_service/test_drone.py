import json

from hypothesis import given, HealthCheck, settings
from hypothesis.strategies import sampled_from
from tests.conftest import helper


def test_welcome(client):
    response = client.get("/")
    assert response.status_code == 200


def test_register_drone(client):

    td_serial_number = "1234567"
    td_model = "Lightweight"

    response = client.post("/drone/register", data=json.dumps(dict(
        serial_number=td_serial_number,
        model=td_model
    )), mimetype='application/json')

    json_info = helper(response.response)

    assert response.status_code == 201
    assert response.content_type == 'application/json'
    assert json_info["success"] is True
    assert json_info["message"] == "Drone registered successfully"
    assert json_info["data"]["serial_number"] == td_serial_number
    assert json_info["data"]["model"] == td_model
    assert json_info["data"]["weight_limit"] == 200.0
    assert json_info["data"]["battery"] == 100


def test_register_existed_drone(client):

    td_serial_number = "HTU8L8SO2Xx3EYmkKAz4iuFBY2gAo"
    td_model = "Cruiserweight"

    response = client.post("/drone/register", data=json.dumps(dict(
        serial_number=td_serial_number,
        model=td_model
    )), mimetype='application/json')

    json_info = helper(response.response)

    assert response.status_code == 202
    assert response.content_type == 'application/json'
    assert json_info["success"] is False
    assert json_info["message"] == "Drone already registered"


@given(td_state=sampled_from(["IDLE", "LOADING", "LOADED", "DELIVERING", \
                "DELIVERED", "RETURNING"]))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_update_drone_state_from_idle(client, td_state):

    td_serial_number = "LNVotKpL0QmcHjvwJeTz"
    response = client.put("/drone/" + td_serial_number, data=json.dumps(dict(
        state=td_state
    )), mimetype='application/json')

    json_info = helper(response.response)

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert json_info["success"] is False

    match td_state:
        case "LOADING":
            assert json_info["message"] == \
                "The only way to change to LOADING is adding medications"
        case 'IDLE':
            assert json_info["message"] == \
                "You only change from RETURNING to IDLE state"
        case 'LOADED':
            assert json_info["message"] == \
                "You only change from LOADING to LOADED state"
        case "DELIVERED":
            assert json_info["message"] == \
                "You only change from DELIVERING to DELIVERED state"
        case "RETURNING":
             assert json_info["message"] == \
                "You only change from DELIVERED or DELIVERING to RETURNING state"
        case "DELIVERING":
            assert json_info["message"] == \
                "You only change from LOADED or LOADING to DELIVERING state"


@given(td_state=sampled_from(["IDLE", "LOADING", \
                "DELIVERED", "RETURNING"]))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_update_drone_state_from_loading_rejected(client, td_state):

    td_serial_number = "tbGTqKCXYFb"
    response = client.put("/drone/" + td_serial_number, data=json.dumps(dict(
        state=td_state
    )), mimetype='application/json')

    json_info = helper(response.response)

    assert response.status_code == 200
    assert response.content_type == 'application/json'

    match td_state:
        case "LOADING":
            assert json_info["success"] is False
            assert json_info["message"] == \
                "The only way to change to LOADING is adding medications"

        case 'IDLE':
            assert json_info["success"] is False
            assert json_info["message"] == \
                "You only change from RETURNING to IDLE state"

        case "DELIVERED":
            assert json_info["success"] is False
            assert json_info["message"] == \
                "You only change from DELIVERING to DELIVERED state"

        case "RETURNING":
             assert json_info["success"] is False
             assert json_info["message"] == \
                "You only change from DELIVERED or DELIVERING to RETURNING state"


"""The test in this case was splitted in two because the hypothesis library
    genereate a lot of test cases without clean the database, so the test
    failed because the drone was already in LOADED state or DELIVERING state"""

@given(td_state=sampled_from(["LOADED", "DELIVERING"]))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_update_drone_state_from_loading_acepted(client, td_state):

    td_serial_number = "tbGTqKCXYFb"
    response = client.put("/drone/" + td_serial_number, data=json.dumps(dict(
        state=td_state
    )), mimetype='application/json')

    json_info = helper(response.response)

    assert response.status_code == 200
    assert response.content_type == 'application/json'

    match td_state:
        case 'LOADED':
            assert json_info["success"] is True
            assert json_info["message"] == \
                "Drone state changed successfully"

        case "DELIVERING":
            assert json_info["success"] is True
            assert json_info["message"] == \
                "Drone state changed successfully"


# @given(td_state=sampled_from(["IDLE", "LOADING", "LOADED", "DELIVERING", \
#                 "DELIVERED", "RETURNING"]))
# @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
# def test_update_drone_state_from_loaded(client, td_state):

#     td_serial_number = "kcPyGHjfrhU3TbOp"
#     response = client.put("/drone/" + td_serial_number, data=json.dumps(dict(
#         state=td_state
#     )), mimetype='application/json')

#     json_info = helper(response.response)

#     assert response.status_code == 200
#     assert response.content_type == 'application/json'

#     match td_state:
#         case "LOADING":
#             assert json_info["success"] is False
#             assert json_info["message"] == \
#                 "The only way to change to LOADING is adding medications"

#         case 'IDLE':
#             assert json_info["success"] is False
#             assert json_info["message"] == \
#                 "You only change from RETURNING to IDLE state"

#         case "DELIVERED":
#             assert json_info["success"] is False
#             assert json_info["message"] == \
#                 "You only change from DELIVERING to DELIVERED state"

#         case "RETURNING":
#              assert json_info["success"] is False
#              assert json_info["message"] == \
#                 "You only change from DELIVERED or DELIVERING to RETURNING state"

#         case 'LOADED':
#              assert json_info["success"] is False
#              assert json_info["message"] == \
#                 "You only change from LOADING to LOADED state"

#         case "DELIVERING":
#             assert json_info["success"] is True
#             assert json_info["message"] == \
#                 "Drone state changed successfully"


# @given(td_state=sampled_from(["IDLE", "LOADING", "LOADED", "DELIVERING", \
#                 "DELIVERED", "RETURNING"]))
# @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
# def test_update_drone_state_from_delivering(client, td_state):

#     td_serial_number = "eLGsWwiJ5Lzn"
#     response = client.put("/drone/" + td_serial_number, data=json.dumps(dict(
#         state=td_state
#     )), mimetype='application/json')

#     json_info = helper(response.response)

#     assert response.status_code == 200
#     assert response.content_type == 'application/json'

#     if td_state != "DELIVERED":
#         assert json_info["data"]["success"] is False
#         assert json_info["data"]["message"] == \
#             "You only change from DELIVERING to DELIVERED state"
#     else:
#         assert json_info["success"] is True



# @given(td_state=sampled_from(["IDLE", "LOADING", "LOADED", "DELIVERING", \
#                 "DELIVERED", "RETURNING"]))
# @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
# def test_update_drone_state_from_delivered(client, td_state):

#     td_serial_number = "jEwQeOv3LFqJee"
#     response = client.put("/drone/" + td_serial_number, data=json.dumps(dict(
#         state=td_state
#     )), mimetype='application/json')

#     json_info = helper(response.response)

#     assert response.status_code == 200
#     assert response.content_type == 'application/json'

#     if td_state != "RETURNING":
#         assert json_info["data"]["success"] is False
#         assert json_info["data"]["message"] == \
#             "You only change from DELIVERED to RETURNING state"
#     else:
#         assert json_info["data"]["success"] is True


# @given(td_state=sampled_from(["IDLE", "LOADING", "LOADED", "DELIVERING", \
#                 "DELIVERED", "RETURNING"]))
# @settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
# def test_update_drone_state_from_returning(client, td_state):

#     td_serial_number = "mOb3Kd0IX4RJdtTVAAET"
#     response = client.put("/drone/" + td_serial_number, data=json.dumps(dict(
#         state=td_state
#     )), mimetype='application/json')

#     json_info = helper(response.response)

#     assert response.status_code == 200
#     assert response.content_type == 'application/json'

#     if td_state != "IDLE":
#         assert json_info["data"]["success"] is False
#         assert json_info["data"]["message"] == \
#             "You only change from RETURNING to IDLE state"
#     else:
#         assert json_info["data"]["success"] is True
