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


def load_drone():
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, add_medicine_schema)
        serial_number = request_data['serial_number']
        stored_drone = Drone.query.filter_by(serial_number=serial_number).first()
        if stored_drone.battery_capacity >= 25:
            stored_and_not_stored = stored_drone.add_medication(request_data['medications'])
            data = {
                "success": True,
                "data": {
                    "medication": stored_and_not_stored,
                    "drone": {
                        "serial_number": stored_drone.serial_number,
                        "state": stored_drone.state
                    }
                }
            }
            response = Response(json.dumps(data), 202, \
                mimetype="application/json")
        else:
            data = {
                "success": False,
                "message": "Drone under permitted limit to carry medicine",
                "data": {
                    "serial_number": stored_drone.serial_number,
                    "battery": "{}%".format(stored_drone.battery_capacity)
                }
            }
            response = Response(json.dumps(data), 202, \
                mimetype="application/json")

    except jsonschema.exceptions.ValidationError as exc:
        response = Response(str(exc.message), 400, mimetype="application/json")
    return response
