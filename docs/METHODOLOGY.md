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
`router/dataset.py` has two sets.

- **`DATA_V1`**: the original 16 messages, unchanged. The published Jev results (3 runs, 2026-10-05) used exactly this set. `python -m router.benchmark --v1` reruns it.
- **`DATA`**: 120 messages, `DATA_V1` plus 104 newer ones, 30 per team (billing, bug, account, sales).

Each example has a stable `id` (`v1-01`, `bil-007`, ...), a `label` and a `kind`:

| Kind | Meaning |
|---|---|
| easy | Contains an obvious keyword for its own team |
| no-keyword | Matches none of the baseline's keywords; the team follows from the meaning |
| misleading-keyword | Contains a keyword for a different team (e.g. mentions "password" but is a billing dispute) |
| multi-intent | Several sentences or topics; the label follows the actual ask |
| terse | A few words |
| noisy | Typos, informal or non-native phrasing |

Tests check that `no-keyword` messages really match no baseline keyword and that
`misleading-keyword` messages really contain another team's keyword.

### How the data was written
All 120 messages were written by hand by the repo author. None are copied from real
customer data. The 104 newer messages were written to be varied and hard: roughly half
carry no obvious trigger word, many have several sentences, and some mention one topic
while needing another team.

### Authorship caveat
The same person wrote the keyword baseline and the data. The newer messages were
deliberately written to defeat keyword matching, so the baseline's low score on them is
partly by design and says little about real traffic. The labels are one person's
judgment, with no second annotator. The `easy` messages (28 of 120, including the V1
ones) are the ones the baseline was effectively written against. The kind mix is not a
sample of any real ticket distribution.

### Ambiguity
Nine examples (`AMBIGUOUS_IDS`) are ones where reasonable people could disagree, such as
a trial-expired lockout (sales, billing or account) or enabling SSO (account or sales).
They keep a label, but the benchmark reports **headline accuracy excluding them**, and
reports the full-set and ambiguous-only numbers on separate lines. The list was chosen by
the author before any model was run on the new messages. Other messages may also be
arguable; the list is not a guarantee of clean labels.

### Reading the output
`python -m router.benchmark` prints, per router: headline accuracy, full-set accuracy,
ambiguous-only accuracy, p50/p95 latency, accuracy per kind (headline set), and a
confusion matrix (all runs). `--repeat N` runs each router N times and pools the samples;
per-run headline accuracy is also printed.

## Before quoting results
1. ~~Grow the dataset to 100 or more~~ (done: 120). Still to do: run Jev and the LLM on it; so far they have only been run on `DATA_V1`.
2. Run each model router several times; model output can vary between runs.
3. Report the run date and model versions with the table.
4. Check how Jev returns confidence before using it to escalate to an LLM.
