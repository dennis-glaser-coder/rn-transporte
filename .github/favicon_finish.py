from pathlib import Path
import re

FAVICON = '<link rel="icon" type="image/png" sizes="96x96" href="/assets/favicon-96x96.png">'

pages = list(Path(".").glob("*.html")) + list(Path(".").glob("*/index.html"))
for path in pages:
    html = path.read_text(encoding="utf-8")
    # Google Search currently documents PNG/ICO (among other raster formats)
    # for search-result favicons. Replace older SVG icon declarations with one
    # stable root-relative PNG favicon that works on root and nested pages.
    html = re.sub(
        r'<link\s+rel="(?:shortcut\s+)?icon"[^>]*>\s*',
        '',
        html,
        flags=re.I,
    )
    if "</head>" not in html:
        raise SystemExit(f"RN favicon head missing: {path}")
    html = html.replace("</head>", FAVICON + "\n</head>", 1)
    path.write_text(html, encoding="utf-8")

for path in pages:
    html = path.read_text(encoding="utf-8")
    if FAVICON not in html:
        raise SystemExit(f"RN PNG favicon missing: {path}")
    if re.search(r'<link\s+rel="(?:shortcut\s+)?icon"[^>]+\.svg', html, flags=re.I):
        raise SystemExit(f"RN SVG search favicon remains: {path}")
