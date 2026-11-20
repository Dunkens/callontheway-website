#!/usr/bin/env python3
"""Generate homepage critical CSS from shared styles.css; --check detects drift.

Run whenever styles.css changes. The full stylesheet loads asynchronously,
with a no-JavaScript fallback. No runtime or new build system is required.
"""
from pathlib import Path
import re
import sys


def critical_css(source):
    """Keep shared base/above-fold styles, mega navigation and all breakpoints."""
    source = source.strip()
    markers = [".mission-section{", ".nav-dropdown-mega{",
               ".faq-section .section-header h2{", "@media(max-width:992px){"]
    if any(source.count(marker) != count for marker, count in zip(markers, [1, 2, 1, 1])):
        raise ValueError("Shared CSS markers changed; review critical-CSS extraction")
    mission, mega, faq, responsive = [source.index(marker) for marker in markers]
    services = source.index('.services-grid{')
    if not mission < services < mega < faq < responsive:
        raise ValueError("Shared CSS source order changed; review extraction")
    return source[:services] + source[mega:faq] + source[responsive:]


def main():
    root = Path(__file__).resolve().parents[1]
    page = root / "index.html"
    source = critical_css((root / "styles.css").read_text())
    if "</style" in source.lower():
        raise SystemExit("Unexpected closing style tag in shared stylesheet")
    block = '<style id="homepage-styles">\n' + source + '\n    </style>'
    pattern = r'<style id="homepage-styles">.*?</style>'
    html = page.read_text()
    match = re.search(pattern, html, flags=re.S)
    if match is None:
        raise SystemExit("Missing homepage-styles block")
    if "--check" in sys.argv:
        if match.group(0) != block:
            raise SystemExit("Homepage critical CSS is out of sync; run tools/sync-homepage-styles.py")
        print("PASS: homepage critical CSS matches shared source and breakpoints")
    else:
        page.write_text(re.sub(pattern, lambda _: block, html, count=1, flags=re.S))
        print("Updated homepage critical CSS from styles.css")


if __name__ == "__main__":
    main()
