import jsonschema

from flask import Response, request, json
from schemas.drone_schema import register_drone_schema, add_medicine_schema
from models.drone_model import Drone
from sqlalchemy import exc


def register_drone():
    request_data = request.get_json()
    try:
        if not \
            Drone.query.filter_by(serial_number=request_data['serial_number']).first():

            jsonschema.validate(request_data, register_drone_schema)
            new_drone = Drone(request_data['serial_number'], request_data['model'])
            new_drone.register_drone()
            data = {
                "sucess": True,
                "message": "Drone registered successfully",
                "data": {
                    "serial_number": new_drone.serial_number,
                    "model": new_drone.model,
                    "battery": new_drone.battery_capacity,
                    "weight_limit": new_drone.weight_limit
                }
            }
            response = Response(json.dumps(data), 201, \
                mimetype="application/json")
        else:
            data = {
                "sucess": False,
                "message": "Drone already registered"
            }
            response = Response(json.dumps(data), 202, mimetype="application/json")

    except jsonschema.exceptions.ValidationError as exc:
        response = Response(str(exc.message), 400, mimetype="application/json")

    except exc.SQLAlchemyError as error:
        response = Response(str(error), 400, mimetype="application/json")

    return response


def get_drone(id):
    try:
        stored_drone = Drone.query.filter_by(id=id).first()
        response = Response(json.dumps(str(stored_drone)), 201, \
            mimetype="application/json")
    except exc.SQLAlchemyError as error:
        response = Response(str(error), 400, mimetype="application/json")
    return response

def load_drone():
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, add_medicine_schema)
        drone_id = request_data['drone_id']
        stored_drone = Drone.query.filter_by(id=drone_id).first()
        stored_drone.add_medication(request_data['medications'])
        response = Response(json.dumps(str(stored_drone)), 201, \
            mimetype="application/json")

    except jsonschema.exceptions.ValidationError as exc:
        response = Response(str(exc.message), 400, mimetype="application/json")
    return response
