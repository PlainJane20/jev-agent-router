from router.routers import Route, keyword_router


def test_keyword_billing():
    assert keyword_router("I need a refund") == Route.billing


def test_keyword_default_is_bug():
    assert keyword_router("something odd happened") == Route.bug
