"""WCAG contrast audit across every generated palette.

Part of the launch gate: six palettes x two contrast states, checked at build
time so a palette can never quietly ship unreadable. Exits non-zero on failure.
"""
import sys
from palettes import MODES, HUES, palette

# (foreground token, background token, minimum ratio, what it is)
CHECKS = [
    ("fg", "bg", 4.5, "body text on page"),
    ("fg2", "bg", 4.5, "secondary text on page"),
    ("fg2", "pan", 4.5, "sidebar text"),
    ("m", "pan", 3.0, "muted labels (large/uppercase)"),
    ("a", "bg", 4.5, "links and accents"),
    ("a", "sel", 4.5, "selected catalogue item"),
    ("ok", "bg", 3.0, "status dot"),
    ("r", "bg", 1.3, "hairline rules (non-text)"),
]


def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hexcolor):
    r, g, b = (int(hexcolor[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def main():
    failures = []
    for contrast in (False, True):
        for mode in MODES:
            for hue in HUES:
                tok = palette(mode, hue, contrast)
                name = f"{mode}/{hue}" + ("/hc" if contrast else "")
                for fg, bg, want, what in CHECKS:
                    got = ratio(tok[fg], tok[bg])
                    if got < want:
                        failures.append((name, what, fg, bg, got, want))
    total = len(MODES) * len(HUES) * 2 * len(CHECKS)
    if failures:
        print(f"  {len(failures)} of {total} checks FAIL\n")
        for name, what, fg, bg, got, want in failures:
            print(f"    {name:16} {what:32} --{fg} on --{bg}: {got:.2f} (need {want})")
        return 1
    print(f"  all {total} contrast checks pass")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(__file__.rsplit("/", 1)[0]))
    raise SystemExit(main())
