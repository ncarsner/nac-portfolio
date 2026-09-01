"""
PROTOTYPE — the rotating headline under the name.

Five widely published standards, used here as PLACEHOLDERS; swap them for lines
that are actually yours before this is anything but a prototype.

The quote changes once a day, not once a reload. Seeding from the ordinal date
gets that for free: no storage, no cookie, no session state, and every visitor
sees the same line on the same day — which is what makes it feel like a
publication rather than a slot machine.
"""
import datetime

QUOTES = [
    ("Simplicity is prerequisite for reliability.",
     "Edsger W. Dijkstra"),
    ("Programs must be written for people to read, and only incidentally "
     "for machines to execute.",
     "Abelson & Sussman"),
    ("Premature optimization is the root of all evil.",
     "Donald Knuth"),
    ("Make it work, make it right, make it fast.",
     "Kent Beck"),
    ("Any fool can write code that a computer can understand. Good programmers "
     "write code that humans can understand.",
     "Martin Fowler"),
]


def today(on=None):
    """The quote for a given day. Deterministic, so a reload never rerolls it."""
    day = on or datetime.date.today()
    return QUOTES[day.toordinal() % len(QUOTES)]
