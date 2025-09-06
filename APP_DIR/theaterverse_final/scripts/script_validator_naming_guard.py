"""
System Validator / Theaterverse Final
Script: Validator Naming Guard

Ensures no duplicate base filenames exist across the project (enforces global uniqueness).
"""

import os
import sys
from collections import defaultdict

BASE_DIR = os.getenv("SYSTEM_VALIDATOR_BASE_DIR", "/root/System_Validator/APP_DIR/theaterverse_final")


def scan_files(base_dir):
    names = defaultdict(list)
    for root, _, files in os.walk(base_dir):
        for f in files:
            base = os.path.splitext(f)[0]
            names[base].append(os.path.join(root, f))
    return names


def main():
    names = scan_files(BASE_DIR)
    errors = []
    for base, paths in names.items():
        if len(paths) > 1:
            errors.append((base, paths))
    if errors:
        print("[NamingGuard] Duplicate base names detected:")
        for base, paths in errors:
            print(f"  {base}: {paths}")
        sys.exit(1)
    print("[NamingGuard] All filenames are globally unique.")


if __name__ == "__main__":
    main()

--- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/script_validator_naming_guard.py
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/script_validator_naming_guard.py
# --- END OF STRUCTURE ---
