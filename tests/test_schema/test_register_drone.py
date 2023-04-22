import json
import jsonschema

from hypothesis import given
from hypothesis.strategies import from_regex, sampled_from
from schemas.drone_schema import register_drone_schema


@given(serial_number=from_regex(r'^[a-zA-Z0-9]{7,100}$'), \
    modelo=sampled_from( \
        ["Lightweight", "Middleweight", "Cruiserweight", "Heavyweight"]))
def test_valid_required_arguments(serial_number, modelo):
    td_post_body = {"serial_number": serial_number, "model": modelo}
    jsonschema.validate(td_post_body, register_drone_schema)
