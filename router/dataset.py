"""Labeled evaluation set for the router benchmark.

DATA_V1  the original 16 messages. The published Jev results (3 runs, 2026-10-05)
         used exactly this set, in this order. Do not edit it.
DATA     120 messages: DATA_V1 plus 104 newer ones, 30 per team. Neither Jev nor the
         LLM router has been run on the 104 newer messages.

Every example has a stable id and a kind tag so results can be sliced.
AMBIGUOUS_IDS lists examples where reasonable people could pick a different team;
the benchmark reports them separately from the headline accuracy.

All messages were written by hand by the repo author (who also wrote the keyword
baseline). None come from real customer data.
"""
from typing import NamedTuple

TEAMS = ("billing", "bug", "account", "sales")
KINDS = ("easy", "no-keyword", "misleading-keyword", "multi-intent", "terse", "noisy")


class Example(NamedTuple):
    id: str
    text: str
    label: str
    kind: str


def _ex(id: str, kind: str, label: str, text: str) -> Example:
    return Example(id, text, label, kind)


DATA_V1 = [
    _ex('v1-01', 'easy', 'billing', 'I was charged twice for my subscription this month'),
    _ex('v1-02', 'easy', 'billing', 'Can I get a refund for the annual plan?'),
    _ex('v1-03', 'easy', 'billing', 'My invoice shows the wrong company name'),
    _ex('v1-04', 'easy', 'bug', 'The app crashes every time I open settings'),
    _ex('v1-05', 'easy', 'bug', 'Timeline on my Android phone has been blank since yesterday'),
    _ex('v1-06', 'easy', 'bug', 'Export to CSV throws an error 500'),
    _ex('v1-07', 'easy', 'account', 'I forgot my password and the reset email never arrives'),
    _ex('v1-08', 'no-keyword', 'account', 'Need to change the email address on my profile'),
    _ex('v1-09', 'easy', 'account', 'My account got locked after too many attempts'),
    _ex('v1-10', 'easy', 'sales', 'Do you offer enterprise pricing for 500 seats?'),
    _ex('v1-11', 'easy', 'sales', 'Can we schedule a demo for our team?'),
    _ex('v1-12', 'easy', 'sales', 'What does the upgrade to Pro include?'),
    _ex('v1-13', 'no-keyword', 'billing', 'Why does my bill say $99 when the page says $79?'),
    _ex('v1-14', 'no-keyword', 'bug', 'Dashboard widgets overlap on small screens'),
    _ex('v1-15', 'no-keyword', 'account', 'How do I add a second admin to our workspace?'),
    _ex('v1-16', 'easy', 'sales', 'Looking for a quote on a multi-year contract'),
]

_NEW = [
    _ex('bil-001', 'easy', 'billing', 'My card was billed again even though I cancelled last week'),
    _ex('bil-002', 'easy', 'billing', "Please send me a copy of last month's invoice for our accountant"),
    _ex('bil-003', 'easy', 'billing', "I'd like a refund for the add-on I never used"),
    _ex('bil-004', 'easy', 'billing', 'There is a duplicate charge on my credit card statement'),
    _ex('bil-005', 'no-keyword', 'billing', 'My credit card on file expired. Where do I put in the new one so the next renewal goes through?'),
    _ex('bil-006', 'no-keyword', 'billing', "We got taxed on our order but we're a nonprofit and exempt. Can you fix that?"),
    _ex('bil-007', 'no-keyword', 'billing', 'Where can I find the receipts for the whole year? Finance is asking.'),
    _ex('bil-008', 'no-keyword', 'billing', 'I was promised a discount on the annual deal but the total on my statement is higher.'),
    _ex('bil-009', 'no-keyword', 'billing', 'You took $240 from my bank account and I only signed up for the $20 plan.'),
    _ex('bil-010', 'no-keyword', 'billing', "Cancel my renewal and give me my money back, I haven't touched the product in months."),
    _ex('bil-011', 'no-keyword', 'billing', "My coupon code didn't apply at checkout."),
    _ex('bil-012', 'no-keyword', 'billing', "We want to move from monthly to annual to save money. How does the switch work for the amount we've already paid?"),
    _ex('bil-013', 'misleading-keyword', 'billing', 'After I changed my password the system took $30 from my bank again.'),
    _ex('bil-014', 'misleading-keyword', 'billing', 'The pricing page said free for 14 days but I was taken for money on day 3 and want it returned.'),
    _ex('bil-015', 'misleading-keyword', 'billing', 'I clicked upgrade by accident last night and was taken for $300. Please undo it and put the money back.'),
    _ex('bil-016', 'misleading-keyword', 'billing', 'The error on checkout said card declined, yet my bank shows the money left my account.'),
    _ex('bil-017', 'multi-intent', 'billing', "Hi, hope you're well. Our finance team noticed we're paying for 12 seats but only 9 people use the product. Can we get credit for the unused ones? Thanks, Priya"),
    _ex('bil-018', 'multi-intent', 'billing', 'Two things. First, the dashboard loads fine now, thanks. Second, the October total on our statement is $1,800 higher than September and nobody added seats.'),
    _ex('bil-019', 'multi-intent', 'billing', "I'm writing about my subscription. I love the product. But I was taken for the yearly price when I picked monthly, and I need that corrected today."),
    _ex('bil-020', 'multi-intent', 'billing', 'Our accountant needs a W-9 and a VAT number on all the paperwork. Also the totals on the last two statements disagree with each other.'),
    _ex('bil-021', 'terse', 'billing', 'wrong amount on my statement'),
    _ex('bil-022', 'terse', 'billing', 'money back pls'),
    _ex('bil-023', 'terse', 'billing', 'taken twice'),
    _ex('bil-024', 'noisy', 'billing', 'hi i got a bil for 79 but i only use free plan?? pls fix'),
    _ex('bil-025', 'noisy', 'billing', 'wht is this 29.99 on my bank statment from ur company'),
    _ex('bil-026', 'noisy', 'billing', 'helllo, my compnay got overcharged!! need reversal asap'),
    _ex('bug-001', 'easy', 'bug', 'The mobile app freezes when I try to upload a photo'),
    _ex('bug-002', 'easy', 'bug', 'Getting a 404 error when I click the reports tab'),
    _ex('bug-003', 'easy', 'bug', "Search is broken since this morning's update"),
    _ex('bug-004', 'easy', 'bug', 'Page crashes on Safari after I click save'),
    _ex('bug-005', 'no-keyword', 'bug', 'When I click Save nothing happens and my changes are gone after a refresh.'),
    _ex('bug-006', 'no-keyword', 'bug', 'The spinner just keeps spinning on the analytics page, it has been like that for an hour.'),
    _ex('bug-007', 'no-keyword', 'bug', 'Notifications are showing up three times for each comment.'),
    _ex('bug-008', 'no-keyword', 'bug', 'Dates in the exported file are shifted one day back.'),
    _ex('bug-009', 'no-keyword', 'bug', 'Dark mode makes the text unreadable on the settings screen.'),
    _ex('bug-010', 'no-keyword', 'bug', 'Since the latest release, drag and drop of files stopped doing anything.'),
    _ex('bug-011', 'no-keyword', 'bug', 'The API returns an empty list for projects that definitely have tasks in them.'),
    _ex('bug-012', 'no-keyword', 'bug', 'Webhook deliveries are arriving out of order and sometimes twice.'),
    _ex('bug-013', 'misleading-keyword', 'bug', 'Every time I try to log in with Google SSO the page just loops back to the sign-in screen.'),
    _ex('bug-014', 'misleading-keyword', 'bug', 'The invoice PDF download button does nothing when I click it.'),
    _ex('bug-015', 'misleading-keyword', 'bug', "The demo video on your homepage doesn't play on my iPad."),
    _ex('bug-016', 'misleading-keyword', 'bug', 'The pricing calculator on the website shows NaN when I enter 10 or more seats.'),
    _ex('bug-017', 'multi-intent', 'bug', 'Quick note: love the new layout. However the bulk edit feature applies changes to only the first 50 rows and silently ignores the rest. Seen it three times now.'),
    _ex('bug-018', 'multi-intent', 'bug', "We're evaluating you for our team of 40. During the trial the calendar sync duplicated every event on our Outlook. That's a dealbreaker unless it's fixed."),
    _ex('bug-019', 'multi-intent', 'bug', 'My teammate says it works for him. For me, uploading anything larger than 10MB hangs at 99%. Tried Chrome and Firefox, same thing.'),
    _ex('bug-020', 'multi-intent', 'bug', "Hello, after yesterday's maintenance window the scheduled reports are arriving empty. Previously they had data. Please investigate."),
    _ex('bug-021', 'terse', 'bug', "app won't open"),
    _ex('bug-022', 'terse', 'bug', 'images not loading'),
    _ex('bug-023', 'terse', 'bug', 'stuck on loading screen'),
    _ex('bug-024', 'noisy', 'bug', 'teh apps keeps closing by itself after i update'),
    _ex('bug-025', 'noisy', 'bug', 'buton doesnt do anythin on iphone'),
    _ex('bug-026', 'noisy', 'bug', 'ur site is sooo slow today, pages take like 30 sec 2 load'),
    _ex('acc-001', 'easy', 'account', "I can't log in, it says my credentials are wrong"),
    _ex('acc-002', 'easy', 'account', 'My account is locked and I need access today'),
    _ex('acc-003', 'easy', 'account', 'How do I reset my password?'),
    _ex('acc-004', 'easy', 'account', 'Requesting an email change for my user from the old work address to my new one.'),
    _ex('acc-005', 'no-keyword', 'account', 'How do I delete my account and all my data?'),
    _ex('acc-006', 'no-keyword', 'account', 'Can I merge my two accounts? I signed up once with Gmail and once with my work address.'),
    _ex('acc-007', 'no-keyword', 'account', "I need to transfer ownership of the workspace to my colleague since I'm leaving the company."),
    _ex('acc-008', 'no-keyword', 'account', 'Two-factor codes from my authenticator app stopped being accepted after I got a new phone.'),
    _ex('acc-009', 'no-keyword', 'account', "How do I remove a former employee from our team so they can't see anything anymore?"),
    _ex('acc-010', 'no-keyword', 'account', "My name is spelled wrong on my profile and I can't find where to edit it."),
    _ex('acc-011', 'no-keyword', 'account', 'Can you turn on single sign-on for our company domain?'),
    _ex('acc-012', 'no-keyword', 'account', 'I got a notification that someone signed into my profile from another country. Was that me?'),
    _ex('acc-013', 'misleading-keyword', 'account', "I was trying to find the invoice link when I noticed a device in my profile that I don't recognize."),
    _ex('acc-014', 'misleading-keyword', 'account', 'I keep getting an error saying my email is already registered, but I need to recover that profile.'),
    _ex('acc-015', 'misleading-keyword', 'account', 'Please make me an admin on the enterprise workspace; my manager approved it.'),
    _ex('acc-016', 'misleading-keyword', 'account', "I'd like to switch my seat to read-only; the upgrade my boss made gave me too many permissions."),
    _ex('acc-017', 'multi-intent', 'account', "Hey team, I recently changed jobs and my old company email is no longer valid. I can't get the verification code anymore. How do I get back into my profile with my new address?"),
    _ex('acc-018', 'multi-intent', 'account', 'Two requests. First, add Maria as a viewer on our workspace. Second, remove Tom, he left last week.'),
    _ex('acc-019', 'multi-intent', 'account', "I love the service but I've been getting a lot of marketing emails and I'd like to stop them. Also please update my display name to Dr. Okafor."),
    _ex('acc-020', 'multi-intent', 'account', "My daughter set up the profile for me and I don't know the sign-in details. I'm the one paying, so how can I take it over?"),
    _ex('acc-021', 'terse', 'account', 'cant sign in'),
    _ex('acc-022', 'terse', 'account', '2FA reset'),
    _ex('acc-023', 'noisy', 'account', 'i cant acess my acount no more, pls help'),
    _ex('acc-024', 'noisy', 'account', 'hi pls chnage my emial to the new one, old 1 is dead'),
    _ex('acc-025', 'noisy', 'account', 'forgt pasword, link expird'),
    _ex('acc-026', 'no-keyword', 'account', "I can't see the billing tab in settings anymore."),
    _ex('sal-001', 'easy', 'sales', "What's the pricing for a team of 25?"),
    _ex('sal-002', 'easy', 'sales', "We'd like a demo of the analytics features next week."),
    _ex('sal-003', 'easy', 'sales', 'Can I get a quote for 200 licenses?'),
    _ex('sal-004', 'easy', 'sales', 'Interested in the enterprise plan, who do I talk to?'),
    _ex('sal-005', 'no-keyword', 'sales', 'Do you have a nonprofit discount?'),
    _ex('sal-006', 'no-keyword', 'sales', "We're a 300-person company evaluating tools like yours. Can someone walk us through what you offer?"),
    _ex('sal-007', 'no-keyword', 'sales', "What's the difference between the Team and Business tiers?"),
    _ex('sal-008', 'no-keyword', 'sales', 'Does your plan include SSO and audit logs? Our security team requires both before we sign.'),
    _ex('sal-009', 'no-keyword', 'sales', "We'd like to extend our pilot to two more departments. Who should we talk to?"),
    _ex('sal-010', 'no-keyword', 'sales', 'Are volume discounts available when buying more than 1000 seats?'),
    _ex('sal-011', 'misleading-keyword', 'sales', 'Before we sign, we need to understand the payment terms: net 30 or net 60 for a 2-year contract?'),
    _ex('sal-012', 'misleading-keyword', 'sales', "Our current vendor's product crashes constantly, so we're looking to switch to you. What would a migration look like for 80 users?"),
    _ex('sal-013', 'misleading-keyword', 'sales', 'We want to buy, but the evaluation account we created is locked until we talk to someone. Can a rep call us?'),
    _ex('sal-014', 'misleading-keyword', 'sales', 'Is there an extra charge for API access on the Business plan, or is it included?'),
    _ex('sal-015', 'multi-intent', 'sales', "Hi, I run IT for a 60-person agency. We're on the free plan and love it, but we keep hitting the project limit. What would it cost to move everyone up, and is there a discount for paying yearly?"),
    _ex('sal-016', 'multi-intent', 'sales', "Our CFO wants a written proposal before the end of the quarter. We're looking at about 400 seats across three regions. Please have someone reach out."),
    _ex('sal-017', 'multi-intent', 'sales', 'I saw your booth at the conference. My team has a few questions about integrations and how the costs scale with headcount.'),
    _ex('sal-018', 'multi-intent', 'sales', 'We loved the product during the trial. Is it possible to get a custom plan with a dedicated account manager and priority support?'),
    _ex('sal-019', 'terse', 'sales', 'price for 50 users?'),
    _ex('sal-020', 'terse', 'sales', 'need a sales rep'),
    _ex('sal-021', 'terse', 'sales', 'annual discount?'),
    _ex('sal-022', 'noisy', 'sales', 'helo, we want to by 20 licences, how much??'),
    _ex('sal-023', 'noisy', 'sales', 'hi can i talk 2 sombody about bulk plan for my school'),
    _ex('sal-024', 'noisy', 'sales', 'intrested in ur product, plz call me. 555-0100'),
    _ex('sal-025', 'misleading-keyword', 'sales', 'Can you invoice us annually rather than monthly if we commit to 50 seats?'),
    _ex('sal-026', 'no-keyword', 'sales', "My free trial ended and now I can't open my projects."),
]

DATA = DATA_V1 + _NEW

# Examples where the right team is arguable. Reported separately, not in headline accuracy.
AMBIGUOUS_IDS = [
    'bil-011',
    'bil-012',
    'bug-013',
    'bug-026',
    'acc-011',
    'acc-026',
    'sal-014',
    'sal-025',
    'sal-026',
]
