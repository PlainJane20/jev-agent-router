from collections import Counter

from router.benchmark import evaluate, summarize
from router.dataset import AMBIGUOUS_IDS, DATA, DATA_V1, KINDS, TEAMS
from router.routers import KEYWORDS, keyword_router


def _kw_teams(text):
    low = text.lower()
    return {r.value for r, ws in KEYWORDS.items() if any(w in low for w in ws)}


def test_size_and_unique_ids():
    assert len(DATA) == 120
    assert len({e.id for e in DATA}) == len(DATA)
    assert len({e.text for e in DATA}) == len(DATA)


def test_classes_balanced():
    assert Counter(e.label for e in DATA) == {t: 30 for t in TEAMS}


def test_labels_and_kinds_valid():
    assert all(e.label in TEAMS for e in DATA)
    assert all(e.kind in KINDS for e in DATA)
    assert {e.kind for e in DATA} == set(KINDS)  # every kind is used


def test_ambiguous_ids_exist_and_are_few():
    ids = {e.id for e in DATA}
    assert set(AMBIGUOUS_IDS) <= ids
    assert len(AMBIGUOUS_IDS) == len(set(AMBIGUOUS_IDS))
    assert 0 < len(AMBIGUOUS_IDS) <= 15


def test_v1_preserved_exactly():
    expected = [
        ("I was charged twice for my subscription this month", "billing"),
        ("Can I get a refund for the annual plan?", "billing"),
        ("My invoice shows the wrong company name", "billing"),
        ("The app crashes every time I open settings", "bug"),
        ("Timeline on my Android phone has been blank since yesterday", "bug"),
        ("Export to CSV throws an error 500", "bug"),
        ("I forgot my password and the reset email never arrives", "account"),
        ("Need to change the email address on my profile", "account"),
        ("My account got locked after too many attempts", "account"),
        ("Do you offer enterprise pricing for 500 seats?", "sales"),
        ("Can we schedule a demo for our team?", "sales"),
        ("What does the upgrade to Pro include?", "sales"),
        ("Why does my bill say $99 when the page says $79?", "billing"),
        ("Dashboard widgets overlap on small screens", "bug"),
        ("How do I add a second admin to our workspace?", "account"),
        ("Looking for a quote on a multi-year contract", "sales"),
    ]
    assert [(e.text, e.label) for e in DATA_V1] == expected
    assert DATA[: len(DATA_V1)] == DATA_V1
    assert not set(AMBIGUOUS_IDS) & {e.id for e in DATA_V1}


def test_kind_tags_match_keyword_content():
    """no-keyword examples match no baseline keyword; misleading ones match a wrong team's."""
    for e in DATA:
        teams = _kw_teams(e.text)
        if e.kind == "no-keyword":
            assert not teams, e.id
        if e.kind == "misleading-keyword":
            assert teams - {e.label}, e.id
        if e.kind == "easy":
            assert e.label in teams, e.id


def test_baseline_runs_and_v1_score_is_unchanged():
    s = summarize(evaluate(keyword_router, DATA))
    assert s["full"][1] == 120
    assert s["headline"][1] == 120 - len(AMBIGUOUS_IDS)
    v1 = summarize(evaluate(keyword_router, DATA_V1))
    assert v1["full"] == (13, 16)  # README: keywords 81% (13 of 16)


def test_repeat_multiplies_samples():
    s = summarize(evaluate(keyword_router, DATA_V1, repeat=3))
    assert s["full"][1] == 48 and len(s["per_run"]) == 3
