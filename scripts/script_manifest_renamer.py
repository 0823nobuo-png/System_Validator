"""
System Validator / Theaterverse Final
Script: Manifest Renamer

Renames all manifest.json files to <plugin>_manifest.json to enforce uniqueness.
"""

import os
import sys

BASE_DIR = os.getenv("SYSTEM_VALIDATOR_BASE_DIR", "/root/System_Validator/APP_DIR/theaterverse_final")


def rename_manifests(base_dir):
    for root, _, files in os.walk(base_dir):
        for f in files:
            if f == "manifest.json":
                plugin = os.path.basename(root)
                new_name = f"{plugin}_manifest.json"
                old_path = os.path.join(root, f)
                new_path = os.path.join(root, new_name)
                if os.path.exists(new_path):
                    print(f"[ManifestRenamer] Skipping, already exists: {new_path}")
                    continue
                os.rename(old_path, new_path)
                print(f"[ManifestRenamer] Renamed {old_path} -> {new_path}")


def main():
    rename_manifests(BASE_DIR)


if __name__ == "__main__":
    main()

# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/script_manifest_renamer.py
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/script_manifest_renamer.py
# --- END OF STRUCTURE ---
