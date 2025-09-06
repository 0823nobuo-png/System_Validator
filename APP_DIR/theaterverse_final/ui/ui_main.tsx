"""
System Validator / Theaterverse Final
UI Main - Entry point for React-based UI
"""

import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import UIRouter from "./ui_router";
import "./ui_theme_tokens";

function App() {
  return (
    <BrowserRouter>
      <UIRouter />
    </BrowserRouter>
  );
}

const container = document.getElementById("root");
if (container) {
  const root = createRoot(container);
  root.render(<App />);
}

--- END OF STRUCTURE ---
// /root/System_Validator/APP_DIR/theaterverse_final/ui/ui_main.tsx
// /root/System_Validator/APP_DIR/theaterverse_final/ui/ui_main.tsx
// --- END OF STRUCTURE ---
