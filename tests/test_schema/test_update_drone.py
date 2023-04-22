import jsonschema
from hypothesis import given
from hypothesis.strategies import sampled_from, integers
from schemas.drone_schema import update_drone_schema


@given(battery=integers(min_value=0, max_value=100), \
    status=sampled_from(["IDLE", "LOADING", "LOADED", "DELIVERING", \
                "DELIVERED", "RETURNING"]))
def test_valid_update_drone(battery, status):
    td_post_body = { "battery": battery, "status": status}
    jsonschema.validate(td_post_body, update_drone_schema)


@given(battery=integers(min_value=0, max_value=100))
def test_valid_update_drone_only_battery(battery):
    td_post_body = { "battery": battery}
    jsonschema.validate(td_post_body, update_drone_schema)


@given(status=sampled_from(["IDLE", "LOADING", "LOADED", "DELIVERING", \
                "DELIVERED", "RETURNING"]))
def test_valid_update_drone_only_status(status):
    td_post_body = {"status": status}
    jsonschema.validate(td_post_body, update_drone_schema)

