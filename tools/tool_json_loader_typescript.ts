/**
 * System Validator / Theaterverse Final
 * Tool: JSON Loader (TypeScript)
 *
 * Loads and validates JSON files with schema support.
 */

import fs from "fs";
import path from "path";

export async function loadConfig(baseDir: string): Promise<Record<string, any>> {
  const envFile = path.join(baseDir, "config_env_template.env");
  const yamlFile = path.join(baseDir, "config_app_defaults.yaml");

  const config: Record<string, any> = {};

  // Load env file
  if (fs.existsSync(envFile)) {
    const lines = fs.readFileSync(envFile, "utf-8").split("\n");
    for (const line of lines) {
      if (!line || line.startsWith("#")) continue;
      const [k, v] = line.split("=", 2);
      config[k] = v;
    }
  }

  // Load YAML file
  if (fs.existsSync(yamlFile)) {
    const yaml = await import("js-yaml");
    const doc = yaml.load(fs.readFileSync(yamlFile, "utf-8"));
    Object.assign(config, doc);
  }

  // PostgreSQL DSN validation
  if (!config["SYSTEM_VALIDATOR_DSN"]?.startsWith("postgresql")) {
    throw new Error("SYSTEM_VALIDATOR_DSN must be a PostgreSQL DSN");
  }

  return config;
}

// --- END OF STRUCTURE ---
// /root/System_Validator/APP_DIR/theaterverse_final/tools/tool_json_loader_typescript.ts
// /root/System_Validator/APP_DIR/theaterverse_final/tools/tool_json_loader_typescript.ts
// --- END OF STRUCTURE ---
