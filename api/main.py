from flask import Response
from db_config import db


def welcome():
    response_text = '{ "message": "Hello, welcome to Drone-api" }'
    response = Response(response_text, 200, mimetype='application/json')
    return response


def health():
    response_text = '{ "status": "OK" }'
    response = Response(response_text, 200, mimetype='application/json')
    return response

def create_db():
    db.drop_all()
    db.create_all()
    response_text = '{ "message": "Database created." }'
    response = Response(response_text, 200, mimetype='application/json')
    return response