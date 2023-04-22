import json
import jsonschema

from hypothesis import given
from hypothesis.strategies import from_regex, sampled_from, integers
from schemas.drone_schema import register_drone_schema, update_drone_schema, \
    delete_drone_schema, add_medicine_schema


@given(battery=integers(min_value=0, max_value=100), \
    status=sampled_from(["IDLE", "LOADING", "LOADED", "DELIVERING", \
                "DELIVERED", "RETURNING"]))
def test_schema_update_drone_schema(battery, status):
    td_post_body = { "battery": battery, "status": status}
    jsonschema.validate(td_post_body, update_drone_schema)


def test_schema_delete_drone_schema():
    td_post_body = '{ "serial_number": "string" }'
    jsonschema.validate(json.loads(td_post_body), delete_drone_schema)


def test_schema_add_medicine_schema():
    td_post_body = '{"serial_number": "string", "medicine": [{"name": "string", ' \
        '"weigth": "number", "code": "string", "image": "string"}]}'
    jsonschema.validate(json.loads(td_post_body), add_medicine_schema)
