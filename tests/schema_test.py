import json
import jsonschema

from schemas.drone_schema import register_drone_schema, update_drone_schema, \
    delete_drone_schema, add_medicine_schema

def test_schema_register_drone_schema():
    td_post_body = '{ "serial_number": "string", "model": "string" }'
    jsonschema.validate(json.loads(td_post_body), register_drone_schema)


def test_schema_update_drone_schema():
    td_post_body = '{ "battery": "number", "state": "string"}'
    jsonschema.validate(json.loads(td_post_body), update_drone_schema)


def test_schema_delete_drone_schema():
    td_post_body = '{ "serial_number": "string" }'
    jsonschema.validate(json.loads(td_post_body), delete_drone_schema)


def test_schema_add_medicine_schema():
    td_post_body = '{"serial_number": "string", "medicine": [{"name": "string", ' \
        '"weigth": "number", "code": "string", "image": "string"}]}'
    jsonschema.validate(json.loads(td_post_body), add_medicine_schema)
