#!/usr/bin/env python3
"""Inline the shared stylesheet for the homepage; use --check to detect drift.

Run this whenever styles.css changes. Other pages continue using styles.css.
No new build system or runtime JavaScript is required.
"""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
page = root / "index.html"
source = (root / "styles.css").read_text().strip()
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
        raise SystemExit("Homepage CSS is out of sync; run tools/sync-homepage-styles.py")
    print("PASS: homepage inline CSS matches styles.css")
else:
    html = re.sub(pattern, lambda _: block, html, count=1, flags=re.S)
    page.write_text(html)
    print("Updated homepage CSS from styles.css")
