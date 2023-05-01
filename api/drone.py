import base64
import jsonschema

from flask import Response, request, json
from schemas.drone_schema import register_drone_schema, add_medicine_schema
from models.drone_model import Drone
from models.medicine_model import Medication
from sqlalchemy import exc
from db_config import db
from config import drone_api


def register_drone():
    request_data = request.get_json()
    try:
        jsonschema.validate(request_data, register_drone_schema)
        new_drone = Drone(request_data['serial_number'], request_data['model'])
        new_drone.register_drone()
        response = Response(json.dumps(str(new_drone)), 201, \
            mimetype="application/json")
    except jsonschema.exceptions.ValidationError as exc:
        response = Response(str(exc.message), 400, mimetype="application/json")
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
        added = stored_drone.add_medication(request_data['medications'])
        response = Response(json.dumps(str(added)), 200, \
            mimetype="application/json")

    except jsonschema.exceptions.ValidationError as exc:
        response = Response(str(exc.message), 400, mimetype="application/json")
    return response
