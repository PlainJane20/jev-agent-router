# jev-agent-router

Routes customer messages to the right team and benchmarks three approaches
head to head: a keyword baseline, an LLM (Claude Haiku), and TypeSafe's Jev
decision model.

Jev returns a typed choice instead of generated text, so the interesting
questions are whether it matches an LLM on accuracy and how much latency and
cost it saves.

## Run

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest                  # unit tests, no keys needed
python -m router.benchmark        # keyword baseline only

pip install "pydantic-ai-slim[typesafe,anthropic]"
export TYPESAFE_API_KEY=...       # enables the Jev router
export ANTHROPIC_API_KEY=...      # enables the LLM router
python -m router.benchmark
```

## Results

_Not run yet. Paste the benchmark table here once you have API keys, and note
the dataset size (16 examples is a smoke test, not evidence). Grow
`router/dataset.py` to 100+ examples before quoting numbers._

## Ideas to extend

- Use Jev's confidence output to escalate low-confidence messages to an LLM.
- Add a cost column using published per-token prices.
- Wire the router into a LangChain or Pydantic AI multi-agent graph.
