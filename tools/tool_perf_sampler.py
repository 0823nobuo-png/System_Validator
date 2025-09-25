"""
System Validator / Theaterverse Final
Tool: Performance Sampler

Samples performance metrics (response times, error rates) for observability.
"""

import time
import statistics
from typing import List, Dict


class PerfSampler:
    def __init__(self):
        self.samples: List[float] = []

    def record(self, value: float):
        self.samples.append(value)

    def summary(self) -> Dict[str, float]:
        if not self.samples:
            return {"count": 0, "avg": 0.0, "max": 0.0, "min": 0.0}
        return {
            "count": len(self.samples),
            "avg": statistics.mean(self.samples),
            "max": max(self.samples),
            "min": min(self.samples),
        }


if __name__ == "__main__":
    sampler = PerfSampler()
    for _ in range(5):
        start = time.perf_counter()
        time.sleep(0.1)
        elapsed = time.perf_counter() - start
        sampler.record(elapsed)
    print(sampler.summary())

# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/tools/tool_perf_sampler.py
# /root/System_Validator/APP_DIR/theaterverse_final/tools/tool_perf_sampler.py
# --- END OF STRUCTURE ---
