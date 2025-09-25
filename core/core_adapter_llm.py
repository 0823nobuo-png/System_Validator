"""
core_adapter_llm.py

LLM繧｢繝繝励ち譛ｬ螳溯｣・ｼ・- 繝励Ο繝舌う繝・・LLM/llama.cpp/OpenAI・峨ｒ邨ｱ荳IF縺ｧ蜻ｼ縺ｳ蜃ｺ縺・- 螟ｱ謨玲凾縺ｮ繝輔ぉ繧､繝ｫ繧ｪ繝ｼ繝撰ｼ・riority鬆・ｼ・- 繝ｪ繝医Λ繧､・域欠謨ｰ繝舌ャ繧ｯ繧ｪ繝包ｼ・- 繝ｬ繝ｼ繝医Μ繝溘ャ繝茨ｼ医ヨ繝ｼ繧ｯ繝ｳ繝舌こ繝・ヨ邁｡譏灘ｮ溯｣・ｼ・- 繧ｿ繧､繝繧｢繧ｦ繝・- OpenTelemetry(莉ｻ諢・險域ｸｬ繝輔ャ繧ｯ
- 險ｭ螳壹・ config/llm_connector_config.json 縺九ｉ隱ｭ縺ｿ霎ｼ縺ｿ

豁｣蠑上ヱ繧ｹ・・root/System_Validator/APP_DIR/theaterverse_final/core/core_adapter_llm.py
"""
from __future__ import annotations

import json
import os
import time
import threading
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import urllib.request
import urllib.error
import urllib.parse

try:
    from opentelemetry import trace  # type: ignore
    _TRACER = trace.get_tracer("theaterverse_final.core.llm")
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


# ----------------------------- Rate Limiter ------------------------------ #
class TokenBucket:
    def __init__(self, rate_per_minute: int, burst: int) -> None:
        self.capacity = max(1, burst)
        self.tokens = float(self.capacity)
        self.rate_per_sec = max(0.001, rate_per_minute / 60.0)
        self.lock = threading.Lock()
        self.timestamp = time.monotonic()

    def allow(self) -> bool:
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.timestamp
            self.timestamp = now
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate_per_sec)
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                return True
            return False


# ----------------------------- Exceptions -------------------------------- #
class ProviderError(RuntimeError):
    pass

class TimeoutError(ProviderError):
    pass


# ----------------------------- Config Model ------------------------------ #
@dataclass
class RetryConfig:
    max_attempts: int
    base_ms: int
    max_ms: int

@dataclass
class RoutingConfig:
    strategy: str
    priority: List[str]
    timeout_ms: int
    retry: RetryConfig


# ----------------------------- Adapter Core ------------------------------ #
class LLMAdapter:
    def __init__(self, config_path: Optional[str] = None) -> None:
        self.config_path = (
            config_path
            or os.environ.get(
                "LLM_CONNECTOR_CONFIG",
                "/root/System_Validator/APP_DIR/theaterverse_final/config/llm_connector_config.json",
            )
        )
        self.config = self._load_config(self.config_path)
        self.routing = self._parse_routing(self.config)
        self.rate_limiters = self._build_rate_limiters(self.config)

    # ------------------------- Public API ------------------------- #
    def chat(self, messages: List[Dict[str, str]], model: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
        """繝ｦ繝九ヵ繧｡繧､繝・Chat API縲Ｎessages縺ｯOpenAI莠呈鋤蠖｢蠑上ｒ諠ｳ螳壹・        謌ｻ繧雁､繧０penAI莠呈鋤縺ｮ譛蟆丞ｽ｢縺ｧ霑斐☆縲・""
        with _TRACER.start_as_current_span("llm.chat") as span:
            span.set_attribute("llm.messages.count", len(messages))
            last_error: Optional[Exception] = None
            for provider_name in self._providers_in_order():
                if not self._allow(provider_name):
                    last_error = ProviderError(f"rate-limited: {provider_name}")
                    continue
                try:
                    resp = self._call_provider(provider_name, messages, model=model, **kwargs)
                    span.set_attribute("llm.provider", provider_name)
                    return resp
                except Exception as e:  # noqa: BLE001
                    last_error = e
            raise ProviderError(f"All providers failed: {last_error}")

    # ----------------------- Internal Methods --------------------- #
    def _providers_in_order(self) -> List[str]:
        if self.routing.strategy == "failover-priority":
            return list(self.routing.priority)
        return list(self.config["providers"].keys())

    def _allow(self, provider: str) -> bool:
        lim = self.rate_limiters.get(provider)
        return True if lim is None else lim.allow()

    def _call_provider(self, provider: str, messages: List[Dict[str, str]], model: Optional[str], **kwargs: Any) -> Dict[str, Any]:
        timeout = self.routing.timeout_ms / 1000.0
        attempts = max(1, self.routing.retry.max_attempts)
        base = max(0.001, self.routing.retry.base_ms / 1000.0)
        backoff_max = max(base, self.routing.retry.max_ms / 1000.0)
        for i in range(attempts):
            try:
                return self._invoke(provider, messages, model=model, timeout=timeout, **kwargs)
            except TimeoutError as te:
                if i == attempts - 1:
                    raise te
            except Exception as e:  # noqa: BLE001
                if i == attempts - 1:
                    raise e
            sleep = min(backoff_max, base * (2 ** i))
            time.sleep(sleep)
        raise ProviderError("unreachable")

    # ---------------------- Provider Invocations ------------------ #
    def _invoke(self, provider: str, messages: List[Dict[str, str]], *, model: Optional[str], timeout: float, **kwargs: Any) -> Dict[str, Any]:
        p = self.config["providers"].get(provider)
        if not p:
            raise ProviderError(f"unknown provider: {provider}")
        ptype = p["type"]
        if ptype == "openai":
            return self._invoke_openai(p, messages, model=model, timeout=timeout, **kwargs)
        elif ptype == "http":
            return self._invoke_http(p, messages, model=model, timeout=timeout, **kwargs)
        else:
            raise ProviderError(f"unsupported provider type: {ptype}")

    def _invoke_http(self, pconf: Dict[str, Any], messages: List[Dict[str, str]], *, model: Optional[str], timeout: float, **kwargs: Any) -> Dict[str, Any]:
        url = pconf["base_url"].rstrip("/") + "/chat/completions"
        payload = {
            "model": model or pconf.get("default_model"),
            "messages": messages,
            **({k: v for k, v in pconf.get("request", {}).items()}),
            **kwargs,
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read().decode("utf-8")
                obj = json.loads(body)
                return self._as_openai_min(obj)
        except urllib.error.URLError as e:
            if isinstance(e.reason, TimeoutError):
                raise TimeoutError(str(e))
            raise ProviderError(str(e))

    def _invoke_openai(self, pconf: Dict[str, Any], messages: List[Dict[str, str]], *, model: Optional[str], timeout: float, **kwargs: Any) -> Dict[str, Any]:
        api_key = os.environ.get(pconf.get("auth", {}).get("env", "OPENAI_API_KEY"))
        if not api_key:
            raise ProviderError("OPENAI_API_KEY not set")
        url = pconf["base_url"].rstrip("/") + "/chat/completions"
        payload = {
            "model": model or pconf.get("default_model", "gpt-4o-mini"),
            "messages": messages,
            **({k: v for k, v in pconf.get("request", {}).items()}),
            **kwargs,
        }
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        req = urllib.request.Request(url, data=data, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read().decode("utf-8")
                obj = json.loads(body)
                return self._as_openai_min(obj)
        except urllib.error.URLError as e:
            if isinstance(e.reason, TimeoutError):
                raise TimeoutError(str(e))
            raise ProviderError(str(e))

    # --------------------------- Helpers --------------------------- #
    @staticmethod
    def _load_config(path: str) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _parse_routing(cfg: Dict[str, Any]) -> RoutingConfig:
        r = cfg.get("routing", {})
        retry = r.get("retry", {})
        return RoutingConfig(
            strategy=r.get("strategy", "failover-priority"),
            priority=list(r.get("priority", [])),
            timeout_ms=int(r.get("timeout_ms", 20000)),
            retry=RetryConfig(
                max_attempts=int(retry.get("max_attempts", 3)),
                base_ms=int(retry.get("backoff", {}).get("base_ms", 300)),
                max_ms=int(retry.get("backoff", {}).get("max_ms", 4000)),
            ),
        )

    def _build_rate_limiters(self, cfg: Dict[str, Any]) -> Dict[str, TokenBucket]:
        rl = cfg.get("rate_limit", {})
        burst = int(rl.get("burst", 10))
        per = rl.get("per_provider", {})
        res: Dict[str, TokenBucket] = {}
        for name in cfg.get("providers", {}).keys():
            rpm = int(per.get(name, 60))
            res[name] = TokenBucket(rpm, burst)
        return res

    @staticmethod
    def _as_openai_min(obj: Dict[str, Any]) -> Dict[str, Any]:
        # 荳驛ｨ縺ｮ閾ｪ蜑阪し繝ｼ繝舌・OpenAI莠呈鋤繧定ｿ斐☆縺後∝ｮ牙・蛛ｴ縺ｧ譛蟆丞､画鋤
        if "choices" in obj:
            return obj
        # 譛菴朱剞縺ｮ謨ｴ蠖｢・・ontent縺ｮ諠ｳ螳壹く繝ｼ繧呈爾縺呻ｼ・        content = (
            obj.get("message")
            or obj.get("output")
            or obj.get("text")
            or obj.get("choices", [{}])[0].get("message", {}).get("content")
            or ""
        )
        return {
            "id": obj.get("id", "adp_generated"),
            "object": "chat.completion",
            "created": int(time.time()),
            "model": obj.get("model", "unknown"),
            "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
        }


# --------------- Minimal self-test (manual execution) -------------------- #
if __name__ == "__main__":
    adapter = LLMAdapter()
    msgs = [{"role": "user", "content": "Hello from System Validator"}]
    try:
        print(adapter.chat(msgs))
    except Exception as e:  # noqa: T201
        print("Error:", e)

# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_adapter_llm.py
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_adapter_llm.py
# --- END OF STRUCTURE ---
