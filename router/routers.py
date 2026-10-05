"""Three interchangeable routers that map a support message to a team."""
from __future__ import annotations

import os
from enum import Enum


class Route(str, Enum):
    billing = "billing"
    bug = "bug"
    account = "account"
    sales = "sales"


KEYWORDS = {
    Route.billing: ("charge", "invoice", "refund", "payment", "billed"),
    Route.bug: ("crash", "error", "broken", "blank", "not working", "freezes"),
    Route.account: ("password", "login", "log in", "email change", "locked"),
    Route.sales: ("pricing", "quote", "enterprise", "demo", "upgrade"),
}

INSTRUCTIONS = (
    "Route this customer message to the right team: billing, bug, account, or sales."
)


def keyword_router(text: str) -> Route:
    """Baseline: no model, first keyword match wins."""
    low = text.lower()
    for route, words in KEYWORDS.items():
        if any(w in low for w in words):
            return route
    return Route.bug


def pydantic_ai_router(model: str):
    """Build a router backed by any Pydantic AI model string.

    'typesafe:jev-latest' -> Jev (needs TYPESAFE_API_KEY)
    'anthropic:claude-haiku-4-5-20251001' -> LLM baseline (needs ANTHROPIC_API_KEY)
    """
    from pydantic_ai import Agent

    agent = Agent(model, output_type=Route, instructions=INSTRUCTIONS)

    def route(text: str) -> Route:
        return agent.run_sync(text).output

    return route


def available_routers() -> dict:
    routers = {"keywords": keyword_router}
    if os.getenv("TYPESAFE_API_KEY"):
        routers["jev"] = pydantic_ai_router("typesafe:jev-latest")
    if os.getenv("ANTHROPIC_API_KEY"):
        routers["llm-haiku"] = pydantic_ai_router("anthropic:claude-haiku-4-5-20251001")
    return routers
