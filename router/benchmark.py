"""Compare routers on accuracy and latency.

    python -m router.benchmark
"""
import statistics
import time

from router.dataset import DATA
from router.routers import available_routers


def run() -> None:
    routers = available_routers()
    if len(routers) == 1:
        print("Only the keyword baseline is available. Set TYPESAFE_API_KEY and/or "
              "ANTHROPIC_API_KEY to compare Jev and an LLM.\n")

    print(f"{'router':<12}{'accuracy':>10}{'p50 ms':>10}{'p95 ms':>10}")
    for name, route in routers.items():
        correct, times = 0, []
        for text, label in DATA:
            t0 = time.perf_counter()
            pred = route(text)
            times.append((time.perf_counter() - t0) * 1000)
            correct += pred.value == label
        times.sort()
        p95 = times[min(len(times) - 1, int(len(times) * 0.95))]
        print(f"{name:<12}{correct / len(DATA):>10.0%}"
              f"{statistics.median(times):>10.1f}{p95:>10.1f}")


if __name__ == "__main__":
    run()
