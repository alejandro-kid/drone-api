import json

from tests.conftest import helper
from tests.conftest import medicaments


def test_add_a_medication(client):

    td_drone_serial_number = "LNVotKpL0QmcHjvwJeTz"
    td_medicaments = [
        medicaments[0]
    ]

    response = client.post("/load_drone", data=json.dumps(dict(
        serial_number=td_drone_serial_number,
        medications=td_medicaments,
    )), mimetype='application/json')

    json_info = helper(response.response)

    assert response.status_code == 202

    assert len(json_info["data"]["stored"]) == 1
    assert len(json_info["data"]["not_stored"]) == 0
    assert json_info["data"]["stored"][0]["name"] == medicaments[0]["name"]
    assert json_info["data"]["stored"][0]["weight"] == medicaments[0]["weight"]
    assert json_info["data"]["stored"][0]["code"] == medicaments[0]["code"]


def test_add_two_medications(client):

    td_drone_serial_number = "QF8bnGItdpWoVP7NPdS4crPS9LckPbuzidr0FvKuS8y"
    td_medicaments = medicaments

    response = client.post("/load_drone", data=json.dumps(dict(
        serial_number=td_drone_serial_number,
        medications=td_medicaments,
    )), mimetype='application/json')


    json_info = helper(response.response)

    assert response.status_code == 202
    assert len(json_info["data"]["stored"]) == 2
    assert len(json_info["data"]["not_stored"]) == 1

    assert json_info["data"]["stored"][0]["name"] == medicaments[0]["name"]
    assert json_info["data"]["stored"][0]["weight"] == medicaments[0]["weight"]
    assert json_info["data"]["stored"][0]["code"] == medicaments[0]["code"]

    assert json_info["data"]["stored"][1]["name"] == medicaments[2]["name"]
    assert json_info["data"]["stored"][1]["weight"] == medicaments[2]["weight"]
    assert json_info["data"]["stored"][1]["code"] == medicaments[2]["code"]

    assert json_info["data"]["not_stored"][0]["name"] == medicaments[1]["name"]
    assert json_info["data"]["not_stored"][0]["weight"] == medicaments[1]["weight"]
    assert json_info["data"]["not_stored"][0]["code"] == medicaments[1]["code"]


def test_add_cero_medications(client):

    td_drone_serial_number = "HTU8L8SO2Xx3EYmkKAz4iuFBY2gAo"
    td_medicaments = [medicaments[3]]

    response = client.post("/load_drone", data=json.dumps(dict(
        serial_number=td_drone_serial_number,
        medications=td_medicaments,
    )), mimetype='application/json')

    json_info = helper(response.response)

    assert response.status_code == 202
    assert len(json_info["data"]["stored"]) == 0
    assert len(json_info["data"]["not_stored"]) == 1


    assert json_info["data"]["not_stored"][0]["name"] == medicaments[3]["name"]
    assert json_info["data"]["not_stored"][0]["weight"] == medicaments[3]["weight"]
    assert json_info["data"]["not_stored"][0]["code"] == medicaments[3]["code"]
