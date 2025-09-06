"""
System Validator / Theaterverse Final
UI Component: Button
"""

import React from "react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
}

export function Button({ children, ...props }: ButtonProps) {
  return (
    <button
      {...props}
      className={`px-4 py-2 rounded-2xl shadow bg-blue-600 text-white hover:bg-blue-700 ${props.className}`}
    >
      {children}
    </button>
  );
}

--- END OF STRUCTURE ---
// /root/System_Validator/APP_DIR/theaterverse_final/ui/ui_components_button.tsx
// /root/System_Validator/APP_DIR/theaterverse_final/ui/ui_components_button.tsx
// --- END OF STRUCTURE ---
