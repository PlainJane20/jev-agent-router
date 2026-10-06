"""Compare routers on accuracy and latency.

    python -m router.benchmark              # full 120-example set, keyword baseline only
    python -m router.benchmark --v1         # only the original 16 messages (DATA_V1)
    python -m router.benchmark --repeat 3   # run every router 3 times

Headline accuracy excludes AMBIGUOUS_IDS; those are reported on their own line.
Model routers (Jev, LLM) are only included when their API key is set.
"""
import argparse
import statistics
import time
from collections import Counter

from router.dataset import AMBIGUOUS_IDS, DATA, DATA_V1, KINDS, TEAMS
from router.routers import available_routers


def evaluate(route, data, repeat: int = 1) -> list:
    """Run a router over data `repeat` times. Returns (example, prediction, ms, run) tuples."""
    results = []
    for run in range(repeat):
        for ex in data:
            t0 = time.perf_counter()
            pred = route(ex.text).value
            results.append((ex, pred, (time.perf_counter() - t0) * 1000, run))
    return results


def _acc(rows) -> tuple:
    correct = sum(ex.label == pred for ex, pred, _, _ in rows)
    return correct, len(rows)


def _fmt(correct: int, total: int) -> str:
    return f"{correct / total:.0%} ({correct}/{total})" if total else "n/a"


def summarize(results: list) -> dict:
    """Pure aggregation, kept separate from printing so it can be tested."""
    firm = [r for r in results if r[0].id not in AMBIGUOUS_IDS]
    amb = [r for r in results if r[0].id in AMBIGUOUS_IDS]
    per_kind = {k: _acc([r for r in firm if r[0].kind == k]) for k in KINDS}
    confusion = Counter((ex.label, pred) for ex, pred, _, _ in results)
    runs = sorted({r[3] for r in results})
    per_run = [_acc([r for r in firm if r[3] == n]) for n in runs]
    times = sorted(r[2] for r in results)
    return {
        "full": _acc(results), "headline": _acc(firm), "ambiguous": _acc(amb),
        "per_kind": {k: v for k, v in per_kind.items() if v[1]},
        "confusion": confusion, "per_run": per_run,
        "p50": statistics.median(times),
        "p95": times[min(len(times) - 1, int(len(times) * 0.95))],
    }


def print_report(name: str, s: dict) -> None:
    print(f"== {name} ==")
    print(f"  headline (excl. ambiguous): {_fmt(*s['headline'])}")
    print(f"  full set (incl. ambiguous): {_fmt(*s['full'])}")
    print(f"  ambiguous only:             {_fmt(*s['ambiguous'])}")
    if len(s["per_run"]) > 1:
        print("  headline per run:           " + ", ".join(_fmt(*r) for r in s["per_run"]))
    print(f"  latency p50 {s['p50']:.1f} ms, p95 {s['p95']:.1f} ms")
    print("  per kind (headline set):")
    for k, v in s["per_kind"].items():
        print(f"    {k:<20}{_fmt(*v)}")
    print("  confusion (rows = true team, columns = predicted; all runs, incl. ambiguous):")
    print("    " + f"{'true \\ pred':<12}" + "".join(f"{t:>9}" for t in TEAMS))
    for true in TEAMS:
        print("    " + f"{true:<12}" + "".join(f"{s['confusion'][(true, p)]:>9}" for p in TEAMS))
    print()


def run(v1: bool = False, repeat: int = 1) -> None:
    data = DATA_V1 if v1 else DATA
    routers = available_routers()
    if len(routers) == 1:
        print("Only the keyword baseline is available. Set TYPESAFE_API_KEY and/or "
              "ANTHROPIC_API_KEY to compare Jev and an LLM.\n")
    n_amb = sum(ex.id in AMBIGUOUS_IDS for ex in data)
    print(f"dataset: {'DATA_V1' if v1 else 'DATA'}, {len(data)} messages "
          f"({n_amb} ambiguous), {repeat} run(s) per router\n")
    for name, route in routers.items():
        print_report(name, summarize(evaluate(route, data, repeat)))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--v1", action="store_true", help="run only the original 16 messages")
    p.add_argument("--repeat", type=int, default=1, metavar="N", help="runs per router")
    args = p.parse_args()
    if args.repeat < 1:
        p.error("--repeat must be >= 1")
    run(v1=args.v1, repeat=args.repeat)


if __name__ == "__main__":
    main()
