import jsonschema
import pytest
from hypothesis import given
from hypothesis.strategies import from_regex, sampled_from, integers
from schemas.drone_schema import register_drone_schema


@given(serial_number=from_regex(r'^[a-zA-Z0-9]{7,100}$'), \
    modelo=sampled_from( \
        ["Lightweight", "Middleweight", "Cruiserweight", "Heavyweight"]))
def test_valid_required_arguments(serial_number, modelo):
    td_post_body = {"serial_number": serial_number, "model": modelo}
    jsonschema.validate(td_post_body, register_drone_schema)


@given(serial_number=from_regex(r'^[a-zA-Z0-9]{7,100}$'), \
    model=sampled_from( \
        ["Lightweight", "Middleweight", "Cruiserweight", "Heavyweight"]), \
        battery=integers(min_value=0, max_value=100))
def test_valid_required_arguments_and_battery(serial_number, model, battery):
    td_post_body = {"serial_number": serial_number, "model": model, "battery": battery}
    jsonschema.validate(td_post_body, register_drone_schema)


@pytest.mark.xfail
@given(serial_number=from_regex(r'^[a-zA-Z0-9]{7,100}$'), \
        battery=integers(min_value=0, max_value=100))
def test_fail_with_serial_number_and_battery(serial_number, battery):
    td_post_body = {"serial_number": serial_number, "battery": battery}
    jsonschema.validate(td_post_body, register_drone_schema)


@pytest.mark.xfail
@given(model=sampled_from( \
        ["Lightweight", "Middleweight", "Cruiserweight", "Heavyweight"]), \
        battery=integers(min_value=0, max_value=100))
def test_fail_with_model_and_battery(serial_number, model):
    td_post_body = {"serial_number": serial_number, "model": model}
    jsonschema.validate(td_post_body, register_drone_schema)


@pytest.mark.xfail
@given(battery=integers(min_value=0, max_value=100))
def test_fail_only_battery(battery):
    td_post_body = {"battery": battery}
    jsonschema.validate(td_post_body, register_drone_schema)