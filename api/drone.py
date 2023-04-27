import jsonschema

from flask import Response, request, json
from schemas.drone_schema import register_drone_schema
from models.drone_model import Drone


def register_drone():
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, register_drone_schema)
        new_drone = Drone(request_data['serial_number'], request_data['model'])
        new_drone.register_drone()
        response = Response(json.dumps(str(new_drone)), 201, mimetype="application/json")
        json_info = ""
        for info in response.response:
            first_row = info.decode("utf-8")
            json_info = str(json.loads(first_row))
        print(json_info)
        stored_drone = Drone.query.filter_by(serial_number=request_data['serial_number']).first()
        print(stored_drone)
    except jsonschema.exceptions.ValidationError as exc:
        response = Response("error_message_helper(exc.message)", 400, mimetype="application/json")
    return response


def get_drone(id):
    try:
        stored_drone = Drone.get_drone.filter_by(id=id).first()
        response = Response(json.dumps(str(stored_drone)), 201, mimetype="application/json")
    except jsonschema.exceptions.ValidationError as exc:
        response = Response("error_message_helper(exc.message)", 400, mimetype="application/json")
    return response