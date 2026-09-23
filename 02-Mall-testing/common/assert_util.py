# common/assert_util.py
import json
import jsonschema
import os


def validate_json_schema(response_json, schema_file_name):
    """校验响应体是否符合 JSON Schema"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    schema_path = os.path.join(base_dir, 'data', 'schema', schema_file_name)

    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = json.load(f)

    try:
        jsonschema.validate(instance=response_json, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        raise AssertionError(f"JSON Schema 校验失败: {e.message}")
