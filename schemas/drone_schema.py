register_drone_schema = {
    "type": "object",
    "properties": {
        "serial_number": {
            "type": "string",
            "maximum": 100,
            "pattern": "^[a-zA-Z0-9]*$"
        },
        "model": {
            "type": "string",
            "enum": ["Lightweight", "Middleweight", "Cruiserweight", "Heavyweight"]
            },
        "battery": {"type": "integer", "minimum": 0, "maximum": 100}
    },
    "requiered": ["serial_number", "model"]
}

update_drone_schema = {
    "type": "object",
    "properties": {
        "battery": {"type": "integer", "minimum": 0, "maximum": 100},
        "status": {
            "type": "string",
            "enum": ["IDLE", "LOADING", "LOADED", "DELIVERING", \
                "DELIVERED", "RETURNING"]
        }
    },
    "anyOf": [
        {
            "oneOf": [
                {
                    "required": ["battery"]
                },
                {
                    "required": ["status"]
                }
            ]
        },
        {
            "required": ["battery", "status"]
        }
    ],
}

delete_drone_schema = {
    "type": "object",
    "properties": {
        "serial_number": {
            "type": "string",
            "maximum": 100,
            "pattern": "^[a-zA-Z0-9]*$"
        },
    },
    "requiered": ["serial_number"]
}

add_medicine_schema = {
    "type": "object",
    "properties": {
        "serial_number": {
            "type": "string",
            "maximum": 100,
            "pattern": "^[a-zA-Z0-9]*$"
        },
        "medicine": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "weight": {"type": "number", "pattern": "^[a-zA-Z0-9_-]*$"},
                    "code": {"type": "string", "pattern": "^[A-Z0-9_]+$"},
                    "image": {"type": "string", "contentEncoding": "base64"}
                },
                "requiered": ["name", "weight", "code", "image"]
            },
        "battery": {"type": "number"}
        },
    "requiered": ["serial_number", "medicine"]
    }
}
