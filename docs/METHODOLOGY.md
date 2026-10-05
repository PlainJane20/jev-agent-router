# Methodology and limits

## What is measured
- **Accuracy:** exact match of the predicted team against the label, per message.
- **Latency:** wall-clock time of one routing call, reported as p50 and p95 over the dataset. For model routers this includes the network round trip.

## Routers
| Router | Needs | Notes |
|---|---|---|
| `keywords` | nothing | First keyword match wins; unmatched messages default to `bug` |
| `jev` | `TYPESAFE_API_KEY` | `typesafe:jev-latest` through Pydantic AI, typed `Route` output |
| `llm-haiku` | `ANTHROPIC_API_KEY` | `anthropic:claude-haiku-4-5-20251001` through Pydantic AI, same typed output |

## Dataset
16 hand-written messages across four teams (`router/dataset.py`), written by the author while building the keyword baseline. That makes the baseline's score optimistic, and 16 examples is too few to separate routers that differ by a few points.

## Before quoting results
1. Grow the dataset to 100 or more, including messages the keyword baseline was not tuned on.
2. Run each model router several times; model output can vary between runs.
3. Report the run date and model versions with the table.
4. Check how Jev returns confidence before using it to escalate to an LLM.
