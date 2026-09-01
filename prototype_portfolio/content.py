"""
PROTOTYPE — throwaway content for the portfolio UI prototype.

All names, projects, metrics and links below are FAKE placeholder data.
They exist only so the layouts are judged at realistic density.
Nothing here is persisted; it is a module-level constant, in memory.
"""

SITE = {
    "name": "Sam Rivera",
    "role": "Software engineer",
    "tagline": "I build small tools that survive contact with production.",
    "location": "Portland, OR",
    "blurb": (
        "Backend and developer-tooling work, mostly Python and TypeScript. "
        "I like problems where the hard part is the data model, not the framework. "
        "Currently building observability tooling; previously infrastructure at two "
        "mid-size startups."
    ),
    "links": {
        "GitHub": "https://github.com/",
        "Email": "mailto:sam@example.com",
        "LinkedIn": "https://linkedin.com/",
        "Resume": "#",
    },
}

# kind: app | package | site | writing
ARTIFACTS = [
    {
        "id": "regex-lab",
        "kind": "app",
        "name": "Regex Lab",
        "year": "2026",
        "one_liner": "Live regex tester with match highlighting and capture-group inspection.",
        "tags": ["TypeScript", "Canvas", "Zero-dep"],
        "role": "Sole author",
        "status": "Live",
        "stack": ["TypeScript", "Vite", "No runtime deps"],
        "metrics": {"Bundle": "9 kB", "Users / mo": "4.1k", "Deps": "0"},
        "links": {"Demo": "#", "Code": "https://github.com/", "Docs": "#"},
        "embed": "regex_lab",
        "prose": [
            "Every regex tester I tried made me choose between highlighting and "
            "explaining. This one does both in the same pass: the match highlighter "
            "and the capture-group table read from a single parse, so they can never "
            "disagree with each other.",
            "The interesting constraint was zero runtime dependencies. That ruled out "
            "the usual syntax-highlighting libraries and forced the tokenizer to be "
            "small enough to read in one sitting — about 180 lines.",
        ],
    },
    {
        "id": "deploy-board",
        "kind": "app",
        "name": "Deploy Board",
        "year": "2025",
        "one_liner": "Single-screen deploy status across 40 services, refreshed every 5s.",
        "tags": ["Python", "SSE", "Observability"],
        "role": "Lead, team of 3",
        "status": "Internal",
        "stack": ["Python", "FastAPI", "Server-sent events", "Postgres"],
        "metrics": {"Services": "40", "p95 refresh": "180 ms", "Uptime": "99.95%"},
        "links": {"Demo": "#", "Code": "https://github.com/"},
        "embed": "deploy_board",
        "prose": [
            "The old dashboard answered 'is the deploy green?' in four clicks. That is "
            "three clicks too many at 2am, so this one answers it above the fold for "
            "every service at once.",
            "Server-sent events instead of polling cut the database load by roughly 90%. "
            "The unglamorous win was a single denormalized status table — the previous "
            "version joined five tables per row on every refresh.",
        ],
    },
    {
        "id": "ledgerkit",
        "kind": "package",
        "name": "ledgerkit",
        "year": "2025",
        "one_liner": "Double-entry accounting primitives for Python. Decimal-safe, immutable.",
        "tags": ["Python", "OSS", "Typed"],
        "role": "Maintainer",
        "status": "v2.3.0",
        "stack": ["Python 3.11+", "Hypothesis", "mypy strict"],
        "metrics": {"Downloads / mo": "82k", "Coverage": "97%", "Stars": "1.2k"},
        "links": {"PyPI": "#", "Code": "https://github.com/", "Docs": "#"},
        "embed": None,
        "install": "pip install ledgerkit",
        "sample": '''from ledgerkit import Ledger, Account, Money

cash = Account("assets:cash")
rent = Account("expenses:rent")

ledger = Ledger()
ledger.post(
    "2026-01-01",
    "January rent",
    debits=[(rent, Money("1800.00", "USD"))],
    credits=[(cash, Money("1800.00", "USD"))],
)

assert ledger.balance(cash) == Money("-1800.00", "USD")
assert ledger.is_balanced()''',
        "prose": [
            "Most Python accounting libraries let you post an unbalanced transaction and "
            "find out later. ledgerkit makes that unrepresentable: a posting is "
            "constructed balanced or it raises, and every ledger operation returns a new "
            "ledger rather than mutating one.",
            "Property-based tests do the heavy lifting. Hypothesis generates random "
            "transaction sequences and asserts the invariant that debits equal credits "
            "after any interleaving — which found three rounding bugs the example-based "
            "tests never would have.",
        ],
    },
    {
        "id": "tracewalk",
        "kind": "package",
        "name": "tracewalk",
        "year": "2024",
        "one_liner": "Turn OpenTelemetry spans into a readable call tree in your terminal.",
        "tags": ["Python", "CLI", "OTel"],
        "role": "Sole author",
        "status": "v1.8.2",
        "stack": ["Python", "Rich", "OpenTelemetry"],
        "metrics": {"Downloads / mo": "31k", "Stars": "640"},
        "links": {"PyPI": "#", "Code": "https://github.com/"},
        "embed": None,
        "install": "pipx install tracewalk",
        "sample": '''$ tracewalk trace 4f9a2c —-slowest

checkout.submit                          1,240 ms
├─ auth.verify                              12 ms
├─ cart.price                              108 ms
│  └─ tax.lookup                            94 ms   ← 7.6% self
└─ payment.charge                        1,104 ms   ← 89.0% self
   └─ stripe.api.POST /v1/charges        1,098 ms''',
        "prose": [
            "Trace UIs are excellent when you already know which trace to open. They are "
            "terrible when you are grepping through two hundred of them from a shell. "
            "tracewalk is for the second case.",
            "The whole design is one decision: sort children by self-time, not start "
            "time. Wall-clock ordering tells you what happened; self-time ordering tells "
            "you what to fix.",
        ],
    },
    {
        "id": "field-notes",
        "kind": "site",
        "name": "Field Notes",
        "year": "2024—",
        "one_liner": "A slow blog about data modelling, mostly written on trains.",
        "tags": ["Writing", "Static site", "Astro"],
        "role": "Sole author",
        "status": "24 posts",
        "stack": ["Astro", "Markdown", "Netlify"],
        "metrics": {"Posts": "24", "Readers / mo": "9.4k"},
        "links": {"Site": "#", "RSS": "#", "Code": "https://github.com/"},
        "embed": None,
        "prose": [
            "I write to find out what I think, and the posts that took longest to write "
            "are the ones people actually cite. The archive is deliberately small — I "
            "delete more than I publish.",
        ],
    },
    {
        "id": "schema-drift",
        "kind": "writing",
        "name": "Schema drift is a people problem",
        "year": "2025",
        "one_liner": "Why migration tooling keeps failing, and what actually fixed it for us.",
        "tags": ["Essay", "5.2k words"],
        "role": "Author",
        "status": "Featured",
        "stack": [],
        "metrics": {"Reads": "61k", "HN points": "412"},
        "links": {"Read": "#"},
        "embed": None,
        "prose": [
            "We spent eighteen months buying and building migration tools before "
            "admitting the tools were never the bottleneck. The bottleneck was that "
            "nobody owned the schema, so every migration was a negotiation.",
            "This essay is the writeup of what changed when we gave the schema a single "
            "owner and made every change go through a two-page RFC. Deployment "
            "frequency went up, which was not the outcome anyone predicted.",
        ],
    },
    {
        "id": "gridpaper",
        "kind": "app",
        "name": "Gridpaper",
        "year": "2023",
        "one_liner": "Constraint-based diagram editor that snaps to a semantic grid, not pixels.",
        "tags": ["TypeScript", "SVG", "Solver"],
        "role": "Sole author",
        "status": "Archived",
        "stack": ["TypeScript", "SVG", "Cassowary solver"],
        "metrics": {"Stars": "310", "Status": "Archived 2024"},
        "links": {"Code": "https://github.com/", "Writeup": "#"},
        "embed": None,
        "prose": [
            "An experiment in whether a constraint solver makes diagramming feel better "
            "than freehand dragging. Answer: yes for architecture diagrams, no for "
            "anything organic.",
            "Archived honestly — I stopped using it myself, which is the only signal that "
            "matters for a personal tool.",
        ],
    },
]

TIMELINE = [
    ("2024 — now", "Staff engineer", "Meridian Observability", "Developer tooling and trace infrastructure."),
    ("2021 — 2024", "Senior engineer", "Northgate", "Payments platform, then internal platform team."),
    ("2019 — 2021", "Engineer", "Cauldron Labs", "First engineering hire. Built most of the original backend."),
]

KIND_LABEL = {"app": "App", "package": "Package", "site": "Site", "writing": "Writing"}


def by_kind(kind):
    return [a for a in ARTIFACTS if a["kind"] == kind]


def get(artifact_id):
    return next(a for a in ARTIFACTS if a["id"] == artifact_id)
