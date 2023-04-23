import base64
import jsonschema

from hypothesis import given
from hypothesis.strategies import text, from_regex, floats
from schemas.drone_schema import add_medicine_schema


@given(serial_number=from_regex(r'^[a-zA-Z0-9]{7,100}$'), \
    name=from_regex('^[a-zA-Z0-9]{1}[a-zA-Z0-9_-]{4,}$'), weight=floats(min_value=1.0, \
        max_value=500.0), code=from_regex('^[A-Z0-9][A-Z0-9_]{4,}$'), \
        image=text(min_size=1))
def test_schema_add_medicine_schema(serial_number, name, weight, code, image):
    td_post_body = {"serial_number": serial_number, "medicine": [{"name": name, \
        "weigth": weight, "code": code, \
        "image": base64.b64encode(image.encode())}]}
    print(type({"name": name, \
        "weigth": weight, "code": code, \
        "image": base64.b64encode(image.encode())}))
    jsonschema.validate(td_post_body, add_medicine_schema)
