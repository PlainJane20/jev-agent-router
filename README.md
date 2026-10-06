<img src="docs/jev-agent-router-banner.svg" alt="Jev Agent Router — keyword vs LLM vs Jev routing" width="100%" />

# Jev Agent Router

### *Keyword vs LLM vs Jev: accuracy and latency, measured*

<div align="center">

[![Python 3.11+](https://img.shields.io/badge/Python_3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pydantic AI](https://img.shields.io/badge/Pydantic_AI-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://ai.pydantic.dev/)
[![TypeSafe Jev](https://img.shields.io/badge/TypeSafe-Jev-8b5cf6?style=for-the-badge)](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
[![Tests](https://img.shields.io/badge/Unit_tests-2_passing-2a78d6?style=for-the-badge)](tests/)

</div>

Routes customer messages to the right team (`billing`, `bug`, `account`,
`sales`) three ways and compares them on the same labeled set: a keyword
baseline, an LLM (Claude Haiku), and TypeSafe's Jev. All three return the same
typed `Route`, so the comparison is about accuracy and latency, not output format.

**Why this exists:** Jev is a new kind of model. It does not generate text; it
returns a typed decision with confidence in one pass. Routing is the clearest
place to test the claim that this is faster and cheaper than an LLM without
losing accuracy. I wanted that comparison measured before building anything on top of it.

> **Why this repo exists:** to learn how a decision-only model behaves next to
> an LLM and a plain baseline, and to build the harness first so that when
> API access is available the numbers are reproducible, not anecdotes.

> **Related work in this portfolio:** this is the benchmark behind
> [edge-sentinel](https://github.com/PlainJane20/edge-sentinel), whose decision
> cascade trusts Jev when confident and escalates otherwise. The routing shape
> comes from [switchboard](https://github.com/PlainJane20/switchboard); a Jev
> backend there is a planned next step.

## At a glance

| | |
|---|---|
| **Problem** | Does a decision-only model route as accurately as an LLM, and how much faster is it? |
| **Approach** | Three routers behind one typed interface, one labeled dataset, p50 and p95 latency |
| **Proof so far** | Keyword baseline 81%; Jev 100% on 16 examples across 3 runs; the LLM router is wired but **not yet run** |
| **Output** | An accuracy and latency table per router |

## Competencies demonstrated

| Competency | Observable evidence |
|---|---|
| Evaluation design | One dataset and one typed output across all routers; limits written down in [METHODOLOGY](docs/METHODOLOGY.md) |
| Measurement discipline | Results stay "not run" until they are run; dataset size is stated next to every number |
| Technical judgment | A deterministic baseline first, so model results have something honest to beat |

## Results

Run on 2026-10-05 from an Apple M4 Pro, three consecutive runs per router. Jev was
called through `typesafe:jev-latest` over the public internet, one request at a time,
so its latency includes the network round trip.

| Router | Accuracy | p50 | p95 | Status |
|---|---|---|---|---|
| keywords | 81% (13 of 16) | under 0.1 ms | under 0.1 ms | measured |
| jev | **100% (16 of 16), all 3 runs** | 109 to 113 ms | 172 to 254 ms | measured |
| llm-haiku | n/a | n/a | n/a | not run (needs `ANTHROPIC_API_KEY`) |

**How much this says:** not much about the comparison that matters. The dataset has
16 messages, written by the same person who wrote the keyword rules, and they are
fairly easy. A 100% score on 16 easy examples does not show Jev would match an LLM on
messy real tickets. The LLM row is empty, so there is no Jev-vs-LLM comparison yet.
Do not quote one until the dataset reaches 100 or more examples and the LLM has been run.

What the runs do show: Jev follows a plain-language routing instruction, returned the
correct typed route on every message the baseline missed, and was stable across three runs.

Jev also returns calibrated probabilities. For "I was charged twice for my subscription
this month" it returned `billing` with probability 1.0 and `confidence: {"response": 1.0}`.

## Real findings from building this

1. **The baseline's misses all fell through to the default route.** Three of
   the 16 messages matched no keyword and were sent to `bug`: "Need to change
   the email address on my profile" (account), "Why does my bill say $99 when the
   page says $79?" (billing) and "How do I add a second admin to our workspace?"
   (account). A silent default hides failures; a router that can say "no match" is
   better, which is the idea behind confidence-based escalation.
2. **Output format is controlled so accuracy is comparable.** Every router
   returns the same `Route` enum, so a wrong answer is a wrong team and not a parsing failure.

## Architecture

```mermaid
flowchart LR
    DS[("dataset.py<br/>16 labeled messages")] --> BM["benchmark.py"]
    BM --> KW["keyword_router"]
    BM --> JV["Jev<br/>typesafe:jev-latest"]
    BM --> LL["LLM<br/>claude-haiku"]
    JV -.->|needs TYPESAFE_API_KEY| T[("typed Route")]
    LL -.->|needs ANTHROPIC_API_KEY| T
    KW --> T
    T --> OUT[("accuracy + p50/p95 table")]
```

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest
```

## Usage

```bash
python -m router.benchmark                  # keyword baseline only

pip install "pydantic-ai-slim[typesafe,anthropic]"
export TYPESAFE_API_KEY=...                 # enables the Jev router
export ANTHROPIC_API_KEY=...                # enables the LLM router
python -m router.benchmark
```

## What I'd add next

- [ ] Grow the dataset to 100 or more, including messages the baseline wasn't tuned on
- [x] Run Jev several times (done: 3 runs)
- [ ] Run the LLM router several times and record model versions
- [ ] Add a cost column from published per-token prices
- [x] Verify how Jev returns confidence (a dict like `{"response": 1.0}` plus per-class probabilities)
- [ ] Test escalating low-confidence messages to the LLM
- [ ] Contribute a Jev backend to `switchboard`

## Repository map

```
jev-agent-router/
├── router/       routers, dataset, benchmark
├── tests/        baseline tests
└── docs/         methodology and limits
```

## Contact

<div align="center">

### **Navi Sohi**
*Technical Program Manager & Automation Engineer*

<br>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/navisohi/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/PlainJane20)
[![Email](https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](https://mail.google.com/mail/?view=cm&fs=1&to=nks.ai.dev@gmail.com)

<br>

</div>

## License

MIT
