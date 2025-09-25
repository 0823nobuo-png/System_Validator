"""
System Validator / Theaterverse Final
Tool: JSON Loader (Python)

Loads and validates JSON files with schema support.
"""

import json
import os
from jsonschema import validate, ValidationError
from typing import Any, Dict


class JSONLoader:
    def __init__(self, schema: Dict[str, Any] = None):
        self.schema = schema

    def load(self, path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"JSON file not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if self.schema:
            try:
                validate(instance=data, schema=self.schema)
            except ValidationError as e:
                raise ValueError(f"JSON validation error: {e.message}") from e
        return data


if __name__ == "__main__":
    loader = JSONLoader()
    sample_path = "/root/System_Validator/APP_DIR/theaterverse_final/plugins/plugin_llm_qwen25_7b/plugin_llm_qwen25_7b_manifest.json"
    print(loader.load(sample_path))

# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/tools/tool_json_loader_python.py
# /root/System_Validator/APP_DIR/theaterverse_final/tools/tool_json_loader_python.py
# --- END OF STRUCTURE ---
