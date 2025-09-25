/**
 * System Validator / Theaterverse Final
 * Tests: Config Loader (TypeScript)
 *
 * Validates that the TS JSON/YAML loader loads env and YAML properly.
 */

import fs from "fs";
import path from "path";
import assert from "assert";
import { loadConfig } from "../tools/tool_json_loader_typescript";

const BASE_DIR = "/root/System_Validator/APP_DIR/theaterverse_final";

(async () => {
  const tmpDir = fs.mkdtempSync("/tmp/config_test_");

  const envFile = path.join(tmpDir, "config_env_template.env");
  fs.writeFileSync(envFile, "SYSTEM_VALIDATOR_DSN=postgresql://u:p@localhost:5432/db\n");

  const yamlFile = path.join(tmpDir, "config_app_defaults.yaml");
  fs.writeFileSync(yamlFile, "API_BIND_PORT: 1234\n");

  const cfg = await loadConfig(tmpDir);

  assert(cfg["SYSTEM_VALIDATOR_DSN"].startsWith("postgresql"));
  assert.strictEqual(cfg["API_BIND_PORT"], 1234);

  console.log("[TS Test] Config loader test passed");
})();

// --- END OF STRUCTURE ---
// /root/System_Validator/APP_DIR/theaterverse_final/tests/tests_config_loader_typescript.ts
// /root/System_Validator/APP_DIR/theaterverse_final/tests/tests_config_loader_typescript.ts
// --- END OF STRUCTURE ---
