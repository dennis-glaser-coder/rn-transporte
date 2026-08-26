from pathlib import Path
import re

SITE_URL = "https://rn-transporte.de/"
PREVIEW_REL = "assets/rn-social-preview.jpg"
# Cache-bust the old generated preview so social platforms fetch the uploaded file.
PREVIEW_URL = SITE_URL + PREVIEW_REL + "?v=20260826-upload"
W, H = 1200, 630

preview_path = Path(PREVIEW_REL)
if not preview_path.exists():
    raise SystemExit("Uploaded RN social preview missing")

PUBLIC_PAGES = [
    "index.html",
    "leistungen.html",
    "referenzen.html",
    "unternehmen.html",
    "karriere.html",
    "kontakt.html",
    "betonpumpendienst.html",
    "frischbetontransporte.html",
    "kiestransporte.html",
    "betonlogistik-paderborn-salzkotten.html",
    "betonlogistik-bielefeld-owl.html",
    "betonlogistik-guetersloh-lippstadt-soest.html",
    "betonlogistik-hoexter-warburg.html",
    "betonlogistik-kassel-nordhessen.html",
    "betonlogistik-suedniedersachsen.html",
]

extra_meta = (
    f'<meta property="og:image:width" content="{W}">\n'
    f'<meta property="og:image:height" content="{H}">\n'
    '<meta property="og:image:type" content="image/jpeg">\n'
    '<meta property="og:image:alt" content="RN Torwesten Transporte – Betonlogistik und Transport">\n'
    '<meta name="twitter:image:alt" content="RN Torwesten Transporte – Betonlogistik und Transport">'
)

for filename in PUBLIC_PAGES:
    path = Path(filename)
    if not path.exists():
        raise SystemExit(f"RN social preview page missing: {filename}")

    html = path.read_text(encoding="utf-8")
    html, og_count = re.subn(
        r'<meta property="og:image" content="[^"]*">',
        f'<meta property="og:image" content="{PREVIEW_URL}">',
        html,
        count=1,
    )
    html, tw_count = re.subn(
        r'<meta name="twitter:image" content="[^"]*">',
        f'<meta name="twitter:image" content="{PREVIEW_URL}">',
        html,
        count=1,
    )
    if og_count != 1 or tw_count != 1:
        raise SystemExit(f"RN social image metadata not found exactly once: {filename}")

    html = re.sub(r'\n?<meta property="og:image:alt" content="[^"]*">', '', html)
    html = re.sub(r'\n?<meta property="og:image:width" content="[^"]*">', '', html)
    html = re.sub(r'\n?<meta property="og:image:height" content="[^"]*">', '', html)
    html = re.sub(r'\n?<meta property="og:image:type" content="[^"]*">', '', html)
    html = re.sub(r'\n?<meta name="twitter:image:alt" content="[^"]*">', '', html)

    marker = f'<meta property="og:image" content="{PREVIEW_URL}">'
    html = html.replace(marker, marker + "\n" + extra_meta, 1)

    if html.count(PREVIEW_URL) != 2:
        raise SystemExit(f"RN social preview URL count invalid: {filename}")
    path.write_text(html, encoding="utf-8")

print(f"RN uploaded social preview preserved unchanged: {preview_path}")
print(f"RN social preview metadata applied to {len(PUBLIC_PAGES)} public pages")
