"""
System Validator / Theaterverse Final
Core Security Policy - RBAC and policy enforcement.

Provides role-based access control and centralized policy validation.
"""

import logging
from typing import Dict, List
import yaml
import os

logger = logging.getLogger(__name__)


class SecurityPolicy:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.roles_file = os.path.join(base_dir, "config", "config_rbac_roles.yaml")
        self.roles: Dict[str, List[str]] = {}
        self._load_roles()

    def _load_roles(self):
        if not os.path.exists(self.roles_file):
            logger.warning("Roles file not found: %s", self.roles_file)
            return
        with open(self.roles_file, "r", encoding="utf-8") as f:
            self.roles = yaml.safe_load(f) or {}
        logger.info("Loaded RBAC roles: %s", list(self.roles.keys()))

    def check_access(self, role: str, resource: str) -> bool:
        allowed = self.roles.get(role, [])
        if resource in allowed:
            logger.debug("Access granted for role=%s to resource=%s", role, resource)
            return True
        logger.warning("Access denied for role=%s to resource=%s", role, resource)
        return False


# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_security_policy.py
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_security_policy.py
# --- END OF STRUCTURE ---
