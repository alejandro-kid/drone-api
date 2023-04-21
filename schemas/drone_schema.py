register_drone_schema = {
    "type": "object",
    "properties": {
        "serial_number": {
            "type": "string",
            "maximum": 100,
            "pattern": "^[a-zA-Z0-9_-]*$"
        },
        "model": {
            "type": "string",
            "enum": ["Lightweight", "Middleweight", "Cruiserweight", "Heavyweight"]
            },
        "battery": {"type": "integer", "minimum": 0, "maximum": 100}
    },
    "requiered": ["serial_number", "model"]
}

