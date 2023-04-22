import jsonschema

from hypothesis import given
from hypothesis.strategies import from_regex
from schemas.drone_schema import delete_drone_schema


@given(serial_number=from_regex(r'^[a-zA-Z0-9]{7,100}$'))
def test_schema_delete_drone_schema(serial_number):
    td_post_body = { "serial_number": serial_number}
    jsonschema.validate(td_post_body, delete_drone_schema)

