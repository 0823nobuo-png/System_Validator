"""
ci_sbom_generator.py

讖溯・・・- CI/CD 繝代う繝励Λ繧､繝ｳ蠑ｷ蛹厄ｼ亥ｼｷ蛹問造・峨・荳迺ｰ
- Python, Node.js 萓晏ｭ倬未菫ゅ・SBOM・・oftware Bill of Materials・峨ｒJSON蠖｢蠑上〒蜃ｺ蜉・- CycloneDX 1.5 貅匁侠縺ｮ譛蟆乗ｧ矩繧堤函謌・- SPDX繝ｩ繧､繧ｻ繝ｳ繧ｹ陦ｨ險倥ｂ莉倅ｸ主庄閭ｽ
- CI蜀・〒螳溯｡後＠縲∵・譫懃黄繧・artifacts 縺ｨ縺励※菫晏ｭ・
豁｣蠑上ヱ繧ｹ・・root/System_Validator/APP_DIR/theaterverse_final/scripts/ci_sbom_generator.py
萓晏ｭ假ｼ嗔ip freeze / npm ls --json
"""
import json
import subprocess
import sys
import time
from typing import Any, Dict, List


def collect_python_packages() -> List[Dict[str, Any]]:
    try:
        output = subprocess.check_output([sys.executable, "-m", "pip", "freeze"], text=True)
    except Exception:
        return []
    comps = []
    for line in output.splitlines():
        if "==" in line:
            name, ver = line.split("==", 1)
            comps.append({
                "type": "library",
                "name": name,
                "version": ver,
                "purl": f"pkg:pypi/{name}@{ver}",
            })
    return comps


def collect_node_packages() -> List[Dict[str, Any]]:
    try:
        output = subprocess.check_output(["npm", "ls", "--json", "--all"], text=True)
        data = json.loads(output)
    except Exception:
        return []
    comps = []
    def walk(deps: Dict[str, Any]):
        for name, meta in (deps or {}).items():
            ver = meta.get("version", "0.0.0")
            comps.append({
                "type": "library",
                "name": name,
                "version": ver,
                "purl": f"pkg:npm/{name}@{ver}",
            })
            walk(meta.get("dependencies", {}))
    walk(data.get("dependencies", {}))
    return comps


def generate_sbom() -> Dict[str, Any]:
    components = []
    components.extend(collect_python_packages())
    components.extend(collect_node_packages())
    bom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "version": 1,
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "tools": [{"vendor": "SystemValidator", "name": "ci_sbom_generator", "version": "1.0.0"}],
        },
        "components": components,
    }
    return bom


def main() -> None:
    sbom = generate_sbom()
    with open("sbom.json", "w", encoding="utf-8") as f:
        json.dump(sbom, f, indent=2, ensure_ascii=False)
    print("SBOM generated: sbom.json")


if __name__ == "__main__":
    main()

# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/ci_sbom_generator.py
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/ci_sbom_generator.py
# --- END OF STRUCTURE ---
