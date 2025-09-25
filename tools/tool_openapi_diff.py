"""
System Validator / Theaterverse Final
Tool: OpenAPI Diff

Compares two OpenAPI specifications and reports differences.
"""

import yaml
import sys
from deepdiff import DeepDiff


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def diff_openapi(file1, file2):
    spec1 = load_yaml(file1)
    spec2 = load_yaml(file2)
    diff = DeepDiff(spec1, spec2, ignore_order=True)
    return diff


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: tool_openapi_diff.py <file1.yaml> <file2.yaml>")
        sys.exit(1)
    f1, f2 = sys.argv[1:]
    d = diff_openapi(f1, f2)
    print(d)

# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/tools/tool_openapi_diff.py
# /root/System_Validator/APP_DIR/theaterverse_final/tools/tool_openapi_diff.py
# --- END OF STRUCTURE ---
