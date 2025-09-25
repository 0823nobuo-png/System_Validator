"""
core_auth_manager.py

讖溯・・・- OIDC Discovery / JWKS 蜿門ｾ励→繧ｭ繝｣繝・す繝･
- JWT(ID/Access) 讀懆ｨｼ・・ss/aud/exp/nbf/iAT縲∥lg縲∫ｽｲ蜷搾ｼ・- 繧ｹ繧ｳ繝ｼ繝・繝ｭ繝ｼ繝ｫ縺ｫ蝓ｺ縺･縺乗ｨｩ髯仙宛蠕｡
- 逶｣譟ｻ繝ｭ繧ｰ・・ostgreSQL諠ｳ螳夲ｼ画嶌縺崎ｾｼ縺ｿ繝輔ャ繧ｯ
- OpenTelemetry・井ｻｻ諢擾ｼ峨〒縺ｮ險域ｸｬ
- 險ｭ螳壹・ config/auth_oidc_settings.yaml 縺九ｉ隱ｭ縺ｿ霎ｼ縺ｿ

豁｣蠑上ヱ繧ｹ・・root/System_Validator/APP_DIR/theaterverse_final/core/core_auth_manager.py
萓晏ｭ假ｼ井ｾ具ｼ会ｼ啀yJWT, cryptography, psycopg2-binary, pyyaml
"""
from __future__ import annotations

import base64
import json
import time
import logging
import threading
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import urllib.request
import urllib.error
import urllib.parse

import yaml  # type: ignore

try:  # PyJWT
    import jwt  # type: ignore
    from jwt import algorithms  # type: ignore
except Exception as e:  # pragma: no cover
    raise RuntimeError(
        "PyJWT 縺瑚ｦ九▽縺九ｊ縺ｾ縺帙ｓ縲Ｓequirements縺ｫ 'PyJWT' 繧定ｿｽ蜉縺励※縺上□縺輔＞"
    ) from e

try:
    from opentelemetry import trace  # type: ignore
    _TRACER = trace.get_tracer("theaterverse_final.core.auth")
except Exception:  # pragma: no cover
    class _DummySpan:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def set_attribute(self, *args, **kwargs):
            pass
    class _DummyTracer:
        def start_as_current_span(self, *_args, **_kwargs):
            return _DummySpan()
    _TRACER = _DummyTracer()

logger = logging.getLogger(__name__)


@dataclass
class OIDCConfig:
    issuer: str
    discovery_endpoint: str
    jwks_uri_override: Optional[str]
    allowed_audiences: List[str]
    clock_skew_seconds: int
    algorithms: List[str]
    authorization_scopes: Dict[str, List[str]]  # scope -> roles
    audit_enabled: bool
    audit_sink: str
    audit_table: str
    include_request_id: bool


class JWKSCache:
    def __init__(self) -> None:
        self._keys: Dict[str, Any] = {}
        self._exp: float = 0.0
        self._lock = threading.Lock()

    def get(self) -> Optional[Dict[str, Any]]:
        with self._lock:
            if time.time() < self._exp:
                return self._keys
            return None

    def set(self, keys: Dict[str, Any], ttl: int = 3600) -> None:
        with self._lock:
            self._keys = keys
            self._exp = time.time() + max(60, ttl)


class CoreAuthManager:
    def __init__(self, cfg_path: str = "/root/System_Validator/APP_DIR/theaterverse_final/config/auth_oidc_settings.yaml") -> None:
        self.cfg = self._load_config(cfg_path)
        self.jwks_cache = JWKSCache()

    # ---------------------------- Public API ---------------------------- #
    def verify_access_token(self, token: str) -> Dict[str, Any]:
        with _TRACER.start_as_current_span("auth.verify_token") as span:
            span.set_attribute("auth.alg.allow", ",".join(self.cfg.algorithms))
            header = self._peek_header(token)
            kid = header.get("kid")
            alg = header.get("alg")
            if alg not in self.cfg.algorithms:
                raise PermissionError(f"algorithm not allowed: {alg}")

            jwks = self._ensure_jwks()
            key = self._find_jwk(jwks, kid)
            if not key:
                raise PermissionError("matching JWK not found")

            public_key = algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
            claims = jwt.decode(
                token,
                key=public_key,
                algorithms=self.cfg.algorithms,
                audience=self.cfg.allowed_audiences,
                options={
                    "require": ["exp", "iat", "nbf", "iss"],
                    "verify_signature": True,
                    "verify_aud": True,
                    "verify_iss": True,
                },
                issuer=self.cfg.issuer,
                leeway=self.cfg.clock_skew_seconds,
            )
            span.set_attribute("auth.issuer", claims.get("iss", ""))
            span.set_attribute("auth.sub", claims.get("sub", ""))
            return claims

    def check_scope_role(self, claims: Dict[str, Any], required_scopes: List[str], required_roles: Optional[List[str]] = None) -> bool:
        scopes = self._extract_scopes(claims)
        roles = set(claims.get("roles", []) or claims.get("role", []) or [])
        # 繧ｹ繧ｳ繝ｼ繝・        if not set(required_scopes).issubset(scopes):
            return False
        # 蠖ｹ蜑ｲ・井ｻｻ諢擾ｼ・        if required_roles:
            for s in required_scopes:
                allowed = set(self.cfg.authorization_scopes.get(s, []))
                if not roles & allowed:
                    return False
        return True

    def audit(self, event: str, detail: Dict[str, Any]) -> None:
        if not self.cfg.audit_enabled:
            return
        if self.cfg.audit_sink == "postgres":
            self._audit_pg(event, detail)
        else:
            logger.info("AUDIT %s %s", event, detail)

    # ------------------------- Internal Helpers ------------------------- #
    def _load_config(self, path: str) -> OIDCConfig:
        with open(path, "r", encoding="utf-8") as f:
            doc = yaml.safe_load(f)
        auth_scopes = {s["name"]: s.get("roles", []) for s in doc.get("authorization", {}).get("scopes", [])}
        val = doc.get("validation", {})
        aud = list(val.get("allowed_audiences", []) or [])
        algs = list(val.get("algorithms", []) or [])
        return OIDCConfig(
            issuer=doc.get("issuer"),
            discovery_endpoint=doc.get("discovery_endpoint", ".well-known/openid-configuration"),
            jwks_uri_override=doc.get("jwks_uri_override"),
            allowed_audiences=aud,
            clock_skew_seconds=int(val.get("clock_skew_seconds", 60)),
            algorithms=algs if algs else ["RS256"],
            authorization_scopes=auth_scopes,
            audit_enabled=bool(doc.get("audit", {}).get("enabled", True)),
            audit_sink=str(doc.get("audit", {}).get("sink", "postgres")),
            audit_table=str(doc.get("audit", {}).get("table", "auth_audit_logs")),
            include_request_id=bool(doc.get("audit", {}).get("include_request_id", True)),
        )

    def _discover(self) -> Dict[str, Any]:
        if self.cfg.jwks_uri_override:
            return {"jwks_uri": self.cfg.jwks_uri_override}
        url = self.cfg.issuer.rstrip("/") + "/" + self.cfg.discovery_endpoint.lstrip("/")
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode("utf-8"))

    def _ensure_jwks(self) -> Dict[str, Any]:
        cached = self.jwks_cache.get()
        if cached:
            return cached
        meta = self._discover()
        jwks_uri = meta.get("jwks_uri")
        if not jwks_uri:
            raise RuntimeError("jwks_uri not found in discovery metadata")
        req = urllib.request.Request(jwks_uri, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            jwks = json.loads(r.read().decode("utf-8"))
        self.jwks_cache.set(jwks, ttl=3600)
        return jwks

    @staticmethod
    def _find_jwk(jwks: Dict[str, Any], kid: Optional[str]) -> Optional[Dict[str, Any]]:
        for k in jwks.get("keys", []):
            if kid is None or k.get("kid") == kid:
                return k
        return None

    @staticmethod
    def _peek_header(token: str) -> Dict[str, Any]:
        # JWT繝倥ャ繝・・ase64URL・峨□縺代ｒ蠕ｩ蜿ｷ
        seg = token.split(".")[0]
        padded = seg + "=" * (-len(seg) % 4)
        return json.loads(base64.urlsafe_b64decode(padded.encode("utf-8")).decode("utf-8"))

    @staticmethod
    def _extract_scopes(claims: Dict[str, Any]) -> set:
        scope_str = (
            claims.get("scope")
            or claims.get("scp")
            or ""
        )
        if isinstance(scope_str, list):
            return set(scope_str)
        return set(str(scope_str).split())

    # 逶｣譟ｻ・・ostgreSQL・・    def _audit_pg(self, event: str, detail: Dict[str, Any]) -> None:
        import os
        import psycopg2  # type: ignore
        dsn = os.environ.get("DATABASE_URL") or "dbname=system_validator user=postgres password=postgres host=127.0.0.1 port=5432"
        with psycopg2.connect(dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS {self.cfg.audit_table} (
                        id BIGSERIAL PRIMARY KEY,
                        ts TIMESTAMPTZ DEFAULT NOW(),
                        event TEXT NOT NULL,
                        detail JSONB NOT NULL
                    )
                    """
                )
                cur.execute(
                    f"INSERT INTO {self.cfg.audit_table} (event, detail) VALUES (%s, %s)",
                    (event, json.dumps(detail)),
                )


# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_auth_manager.py
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_auth_manager.py
# --- END OF STRUCTURE ---
