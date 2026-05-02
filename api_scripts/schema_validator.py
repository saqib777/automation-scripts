# JSON Schema Validator for API Testing
# Validates API responses against expected schema definitions
# No external dependencies — pure Python

from typing import Any


class SchemaValidationError(Exception):
    pass


def validate_schema(data: Any, schema: dict, path: str = "root") -> list[str]:
    """
    Validate data against a schema definition.
    Returns list of validation errors (empty = valid).

    Schema format:
        {
            "type": "object" | "array" | "string" | "int" | "float" | "bool" | "any",
            "required": ["field1", "field2"],       # for objects
            "properties": { "field": schema },     # for objects
            "items": schema,                       # for arrays
            "min_length": int,                     # for strings/arrays
            "nullable": True,                      # allow None
        }
    """
    errors = []

    if data is None:
        if not schema.get("nullable", False):
            errors.append(f"{path}: expected non-null value")
        return errors

    expected_type = schema.get("type", "any")

    type_map = {
        "string":  str,
        "int":     int,
        "float":   (int, float),
        "bool":    bool,
        "object":  dict,
        "array":   list,
    }

    if expected_type != "any":
        expected = type_map.get(expected_type)
        if expected and not isinstance(data, expected):
            errors.append(f"{path}: expected {expected_type}, got {type(data).__name__}")
            return errors

    if expected_type == "object" and isinstance(data, dict):
        for req in schema.get("required", []):
            if req not in data:
                errors.append(f"{path}.{req}: required field missing")

        for field, field_schema in schema.get("properties", {}).items():
            if field in data:
                errors.extend(validate_schema(data[field], field_schema, f"{path}.{field}"))

    if expected_type == "array" and isinstance(data, list):
        min_len = schema.get("min_length", 0)
        if len(data) < min_len:
            errors.append(f"{path}: array length {len(data)} < minimum {min_len}")
        item_schema = schema.get("items")
        if item_schema:
            for i, item in enumerate(data):
                errors.extend(validate_schema(item, item_schema, f"{path}[{i}]"))

    if expected_type == "string" and isinstance(data, str):
        min_len = schema.get("min_length", 0)
        if len(data) < min_len:
            errors.append(f"{path}: string length {len(data)} < minimum {min_len}")

    return errors


def assert_schema(data: Any, schema: dict):
    """Assert data matches schema. Raises SchemaValidationError on failure."""
    errors = validate_schema(data, schema)
    if errors:
        raise SchemaValidationError("\n".join(errors))


# ── Predefined schemas ────────────────────────────────────────────────────────

REQRES_USER_SCHEMA = {
    "type": "object",
    "required": ["id", "email", "first_name", "last_name", "avatar"],
    "properties": {
        "id":         {"type": "int"},
        "email":      {"type": "string", "min_length": 5},
        "first_name": {"type": "string", "min_length": 1},
        "last_name":  {"type": "string", "min_length": 1},
        "avatar":     {"type": "string", "min_length": 5},
    }
}

REQRES_LIST_SCHEMA = {
    "type": "object",
    "required": ["page", "per_page", "total", "total_pages", "data"],
    "properties": {
        "page":        {"type": "int"},
        "per_page":    {"type": "int"},
        "total":       {"type": "int"},
        "total_pages": {"type": "int"},
        "data":        {"type": "array", "min_length": 1, "items": REQRES_USER_SCHEMA},
    }
}


if __name__ == "__main__":
    import requests

    r    = requests.get("https://reqres.in/api/users?page=1")
    data = r.json()

    errors = validate_schema(data, REQRES_LIST_SCHEMA)
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
    else:
        print("PASS: Schema valid")

    # Test with bad data
    bad_data = {"page": "one", "data": []}
    errors = validate_schema(bad_data, REQRES_LIST_SCHEMA)
    for e in errors:
        print(f"Expected error: {e}")
