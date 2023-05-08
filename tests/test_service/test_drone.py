import json


def helper(json_info)->any:
    for info in json_info:
        first_row = info.decode("utf-8")
        return json.loads(first_row)


def test_welcome(client):
    response = client.get("/")
    assert response.status_code == 200


def test_register_drone(client):

    td_serial_number = "1234567"
    td_model = "Lightweight"

    response = client.post("/register_drone", data=json.dumps(dict(
        serial_number=td_serial_number,
        model=td_model
    )), mimetype='application/json')

    json_info = helper(response.response)

    assert response.status_code == 201
    assert response.content_type == 'application/json'
    assert json_info["sucess"] is True
    assert json_info["message"] == "Drone registered successfully"
    assert json_info["data"]["serial_number"] == td_serial_number
    assert json_info["data"]["model"] == td_model
    assert json_info["data"]["weight_limit"] == 200.0
    assert json_info["data"]["battery"] == 100


def test_register_existed_drone(client):

    td_serial_number = "HTU8L8SO2Xx3EYmkKAz4iuFBY2gAo"
    td_model = "Cruiserweight"

    response = client.post("/register_drone", data=json.dumps(dict(
        serial_number=td_serial_number,
        model=td_model
    )), mimetype='application/json')

    json_info = helper(response.response)

    assert response.status_code == 202
    assert response.content_type == 'application/json'
    assert json_info["sucess"] is False
    assert json_info["message"] == "Drone already registered"

