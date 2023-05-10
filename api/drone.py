import jsonschema

from flask import Response, request, json
from schemas.drone_schema import register_drone_schema, add_medicine_schema, \
    update_drone_schema
from models.drone_model import Drone
from models.medicine_model import Medication
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
                "success": True,
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
                "success": False,
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
            stored_and_not_stored = \
                stored_drone.add_medication(request_data['medications'])
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


def get_drone(serial_number):
    try:
        stored_drone = Drone.query.filter_by(serial_number=serial_number).first()
        if stored_drone:
            medicines = \
                Medication.query.filter_by(drone_id=stored_drone.serial_number).all()
            data = {
                "success": True,
                "data": {
                    "drone": {
                        "serial_number": stored_drone.serial_number,
                        "model": stored_drone.model,
                        "battery": "{}%".format(stored_drone.battery_capacity),
                        "weight_limit": "{}g".format(stored_drone.weight_limit),
                        "state": stored_drone.state
                    },
                    "medicines": [{
                        "name": medicine.name,
                        "weight": "{}g".format(medicine.weight),
                        "code": medicine.code,
                        "state": medicine.state
                    } for medicine in medicines]
                }
            }
            response = Response(json.dumps(data), 200, mimetype="application/json")
        else:
            data = {
                "success": False,
                "message": "Drone not found"
            }
            response = Response(json.dumps(data), 404, mimetype="application/json")

    except jsonschema.exceptions.ValidationError as exc:
        response = Response(str(exc.message), 400, mimetype="application/json")
    return response


def update_drone(serial_number):
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, update_drone_schema)
        stored_drone = Drone.query.filter_by(serial_number=serial_number).first()
        if stored_drone:
            if 'state' in request_data:
                match request_data['state']:
                    case 'IDLE':
                        if stored_drone.state == 'RETURNING':
                            stored_drone.update_state('IDLE')
                            success = True
                            message = "Drone state changed successfully"
                        else:
                            success = False
                            message = "You only change from RETURNING to IDLE state"

                    case 'LOADING':
                            success = False
                            message = \
                                "The only way to change to LOADING"\
                                " is adding medications"

                    case 'LOADED':
                            if stored_drone.state == 'LOADING':
                                stored_drone.update_state('LOADED')
                                success = True
                                message = "Drone state changed successfully"
                            else:
                                success = False
                                message = "You only change from LOADING to LOADED state"

                    case 'DELIVERING':
                            if stored_drone.state in ['LOADED', 'LOADING']:
                                stored_drone.update_state(state='DELIVERING')
                                success = True
                                message = "Drone state changed successfully"
                            else:
                                success = False
                                message = \
                                    "You only change from LOADED or LOADING" \
                                    " to DELIVERING state"

                    case "DELIVERED":
                            if stored_drone.state == 'DELIVERING':
                                stored_drone.update_state('DELIVERED')
                                Medication.update_all_state(\
                                        stored_drone.serial_number, "DELIVERED"\
                                )
                                success = True
                                message = "Drone state changed successfully"
                            else:
                                success = False
                                message = \
                                    "You only change from DELIVERING to DELIVERED state"

                    case "RETURNING":
                            if stored_drone.state in ['DELIVERED', 'DELIVERING']:
                                if stored_drone.state == 'DELIVERING':
                                    stored_drone.update_state('DELIVERING')
                                    Medication.update_all_state(\
                                        stored_drone.serial_number, "LOADED"\
                                    )
                                    success = True
                                    message = "Drone state changed successfully"
                            else:
                                success = False
                                message = \
                                    "You only change from DELIVERED or DELIVERING" \
                                    " to RETURNING state"
                    case _:
                        success = False
                        message = "Invalid state"

                data = {
                    "success": success,
                    "message": message
                }
                response = Response(json.dumps(data), 200, mimetype="application/json")
            if 'battery' in request_data:
                stored_drone.update_battery(request_data['battery'])
                data = {
                    "success": True,
                    "message": "Drone battery changed successfully"
                }
                response = Response(json.dumps(data), 200, mimetype="application/json")
            print(type(request_data))
        else:
            data = {
                "success": False,
                "message": "Drone not found"
            }
            response = Response(json.dumps(data), 404, mimetype="application/json")

    except jsonschema.exceptions.ValidationError as exc:
        response = Response(str(exc.message), 400, mimetype="application/json")
    return response