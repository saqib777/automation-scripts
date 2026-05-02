import pytest
from schema_validator import validate_schema, assert_schema, SchemaValidationError


def test_valid_string():
    assert validate_schema("hello", {"type": "string"}) == []

def test_invalid_string_type():
    errors = validate_schema(123, {"type": "string"})
    assert len(errors) == 1
    assert "string" in errors[0]

def test_valid_int():
    assert validate_schema(42, {"type": "int"}) == []

def test_valid_object_required_fields():
    schema = {"type":"object","required":["name","age"]}
    assert validate_schema({"name":"Saqib","age":25}, schema) == []

def test_missing_required_field():
    schema = {"type":"object","required":["name","age"]}
    errors = validate_schema({"name":"Saqib"}, schema)
    assert any("age" in e for e in errors)

def test_nested_object():
    schema = {
        "type": "object",
        "properties": {
            "user": {
                "type":     "object",
                "required": ["id","email"],
                "properties": {
                    "id":    {"type":"int"},
                    "email": {"type":"string"},
                }
            }
        }
    }
    assert validate_schema({"user":{"id":1,"email":"a@b.com"}}, schema) == []

def test_nested_missing_field():
    schema = {"type":"object","properties":{"user":{"type":"object","required":["id"]}}}
    errors = validate_schema({"user":{}}, schema)
    assert any("id" in e for e in errors)

def test_array_min_length():
    schema = {"type":"array","min_length":2}
    errors = validate_schema([1], schema)
    assert len(errors) == 1

def test_array_items_schema():
    schema = {"type":"array","items":{"type":"string"}}
    assert validate_schema(["a","b","c"], schema) == []
    errors = validate_schema(["a",2,"c"], schema)
    assert len(errors) == 1

def test_nullable_allows_none():
    assert validate_schema(None, {"type":"string","nullable":True}) == []

def test_non_nullable_rejects_none():
    errors = validate_schema(None, {"type":"string"})
    assert len(errors) == 1

def test_assert_schema_passes():
    assert_schema({"id":1,"name":"test"}, {"type":"object","required":["id","name"]})

def test_assert_schema_raises():
    with pytest.raises(SchemaValidationError):
        assert_schema({}, {"type":"object","required":["id"]})

def test_any_type_accepts_all():
    for val in [1, "str", [], {}, True, None]:
        assert validate_schema(val, {"type":"any"}) == []
