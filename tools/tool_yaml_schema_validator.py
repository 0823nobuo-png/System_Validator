"""
System Validator / Theaterverse Final
Tool: YAML Schema Validator

Validates YAML files against provided JSON schema.
"""

import yaml
import jsonschema
import os
from typing import Dict, Any


class YAMLValidator:
    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema

    def validate_file(self, path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"YAML file not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        jsonschema.validate(instance=data, schema=self.schema)
        return data


if __name__ == "__main__":
    schema = {"type": "object"}
    validator = YAMLValidator(schema)
    sample_path = "/root/System_Validator/APP_DIR/theaterverse_final/config/config_app_defaults.yaml"
    print(validator.validate_file(sample_path))

--- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/tools/tool_yaml_schema_validator.py
# /root/System_Validator/APP_DIR/theaterverse_final/tools/tool_yaml_schema_validator.py
# --- END OF STRUCTURE ---
