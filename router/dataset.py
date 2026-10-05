"""Small labeled set. Extend this before drawing conclusions from benchmark numbers."""
DATA = [
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
