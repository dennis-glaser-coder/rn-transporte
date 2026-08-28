from pathlib import Path
import json
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

# Give Google one unambiguous canonical identity for the company. The public
# short brand remains RN Transporte in visible copy; structured data links it
# to the real company name, current mobile number, current email, logo and a
# genuine RN work photo.
index_path = Path("index.html")
index_html = index_path.read_text(encoding="utf-8")
identity_updates = 0


def patch_identity(value):
    global identity_updates
    if isinstance(value, list):
        return [patch_identity(item) for item in value]
    if not isinstance(value, dict):
        return value

    types = value.get("@type")
    type_set = set(types) if isinstance(types, list) else {types}
    is_company = bool({"LocalBusiness", "Organization"} & type_set)
    canonical = str(value.get("@id", "")).endswith("#organization")
    if is_company and canonical:
        value["name"] = "RN Torwesten Transporte"
        value["alternateName"] = "RN Transporte"
        value["legalName"] = "RN Torwesten Transporte UG (haftungsbeschränkt)"
        value["url"] = SITE_URL
        value["logo"] = SITE_URL + "assets/logo.webp"
        value["image"] = SITE_URL + "assets/leistungen/Baustelleneinsatz.png"
        value["telephone"] = "+491737275165"
        value["email"] = "kontakt@rn-transporte.de"
        contact = value.get("contactPoint")
        if isinstance(contact, dict):
            contact["telephone"] = "+491737275165"
        identity_updates += 1

    for key, item in list(value.items()):
        value[key] = patch_identity(item)
    return value


matches = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', index_html, re.S))
for match in reversed(matches):
    try:
        data = json.loads(match.group(1))
    except Exception:
        continue
    data = patch_identity(data)
    script = '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + '</script>'
    index_html = index_html[:match.start()] + script + index_html[match.end():]

if identity_updates != 1:
    raise SystemExit(f"RN canonical Google identity update count invalid: {identity_updates}")
index_path.write_text(index_html, encoding="utf-8")

print(f"RN uploaded social preview preserved unchanged: {preview_path}")
print(f"RN social preview metadata applied to {len(PUBLIC_PAGES)} public pages")
print("RN Google identity signals normalized: name, phone, email, logo and work image")
