"""
System Validator / Theaterverse Final
UI Router - Application routes configuration
"""

import React from "react";
import { Routes, Route } from "react-router-dom";
import PluginUIConsolePanel from "../plugins/plugin_ui_console/plugin_ui_console_panel";

export default function UIRouter() {
  return (
    <Routes>
      <Route path="/" element={<div>Welcome to System Validator UI</div>} />
      <Route path="/console" element={<PluginUIConsolePanel />} />
    </Routes>
  );
}

--- END OF STRUCTURE ---
// /root/System_Validator/APP_DIR/theaterverse_final/ui/ui_router.ts
// /root/System_Validator/APP_DIR/theaterverse_final/ui/ui_router.ts
// --- END OF STRUCTURE ---
