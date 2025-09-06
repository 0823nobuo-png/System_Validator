"""
System Validator / Theaterverse Final
UI Component: Card
"""

import React from "react";

interface CardProps {
  children: React.ReactNode;
  className?: string;
}

export function Card({ children, className = "" }: CardProps) {
  return (
    <div className={`rounded-2xl shadow-md bg-white p-4 ${className}`}>
      {children}
    </div>
  );
}

export function CardContent({ children }: { children: React.ReactNode }) {
  return <div className="p-2">{children}</div>;
}

--- END OF STRUCTURE ---
// /root/System_Validator/APP_DIR/theaterverse_final/ui/ui_components_card.tsx
// /root/System_Validator/APP_DIR/theaterverse_final/ui/ui_components_card.tsx
// --- END OF STRUCTURE ---
