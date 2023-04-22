import json
import jsonschema

from hypothesis import given
from hypothesis.strategies import sampled_from, integers
from schemas.drone_schema import update_drone_schema, \
    delete_drone_schema, add_medicine_schema

def test_schema_delete_drone_schema():
    td_post_body = '{ "serial_number": "string" }'
    jsonschema.validate(json.loads(td_post_body), delete_drone_schema)


def test_schema_add_medicine_schema():
    td_post_body = '{"serial_number": "string", "medicine": [{"name": "string", ' \
        '"weigth": "number", "code": "string", "image": "string"}]}'
    jsonschema.validate(json.loads(td_post_body), add_medicine_schema)
