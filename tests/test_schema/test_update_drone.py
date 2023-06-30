import jsonschema
from hypothesis import given
from hypothesis.strategies import sampled_from, integers
from src.schemas.drone_schema import update_drone_schema


@given(battery=integers(min_value=0, max_value=100), \
    state=sampled_from(["IDLE", "LOADING", "LOADED", "DELIVERING", \
                "DELIVERED", "RETURNING"]))
def test_valid_update_drone(battery, state):
    td_post_body = { "battery": battery, "state": state}
    jsonschema.validate(td_post_body, update_drone_schema)


@given(battery=integers(min_value=0, max_value=100))
def test_valid_update_drone_only_battery(battery):
    td_post_body = { "battery": battery}
    jsonschema.validate(td_post_body, update_drone_schema)


@given(state=sampled_from(["IDLE", "LOADING", "LOADED", "DELIVERING", \
                "DELIVERED", "RETURNING"]))
def test_valid_update_drone_only_state(state):
    td_post_body = {"state": state}
    jsonschema.validate(td_post_body, update_drone_schema)

