import json
import re
import runpy
import subprocess
import sys
from pathlib import Path

# Generate the established regional pages first. This file is the final public
# consistency pass: labels, metadata, links and validation all end up here.
runpy.run_path(".github/regional_seo_core.py", run_name="__main__")

PRODUCTION_SITE = "https://rn-transporte.de/"
OLD_SITE = "https://dennis-glaser-coder.github.io/rn-transporte/"


def rewrite_jsonld(html: str, transform):
    matches = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
    for match in reversed(matches):
        try:
            data = json.loads(match.group(1))
        except Exception:
            continue
        updated = transform(data)
        script = '<script type="application/ld+json">' + json.dumps(updated, ensure_ascii=False, separators=(",", ":")) + '</script>'
        html = html[:match.start()] + script + html[match.end():]
    return html


# --- Regional grouping: use concrete, non-overlapping labels in the hub. ---
bielefeld_path = Path("betonlogistik-bielefeld-owl.html")
bielefeld = bielefeld_path.read_text(encoding="utf-8")
replacements = {
    "Betonlogistik Bielefeld & OWL | RN Transporte": "Betonlogistik Bielefeld & Gütersloh | RN Transporte",
    "Betonpumpendienst und Transporte für Bielefeld und Ostwestfalen-Lippe. RN Transporte aus Salzkotten für Baustellen, Betonwerke und Schüttgüter.": "Betonpumpendienst und Transporte für Bielefeld, Gütersloh und das nördliche Ostwestfalen. RN Transporte aus Salzkotten für Baustellen, Betonwerke und Schüttgüter.",
    "Betonlogistik für Bielefeld und OWL.": "Betonlogistik für Bielefeld und Gütersloh.",
    "Zuverlässige Einsätze in Ostwestfalen-Lippe – von Salzkotten aus direkt abgestimmt.": "Zuverlässige Einsätze im Raum Bielefeld und Gütersloh – von Salzkotten aus direkt abgestimmt.",
    "Für Baustellen und Betonwerke in Ostwestfalen-Lippe.": "Für Baustellen und Betonwerke rund um Bielefeld und Gütersloh.",
    "Bielefeld & OWL": "Bielefeld & Gütersloh",
    "Bielefeld / OWL": "Bielefeld / Gütersloh",
}
for old, new in replacements.items():
    bielefeld = bielefeld.replace(old, new)
bielefeld = bielefeld.replace('<span>Ostwestfalen-Lippe</span>', '')


def refine_bielefeld_schema(data):
    graph = data.get("@graph") if isinstance(data, dict) else None
    if not isinstance(graph, list):
        return data
    for node in graph:
        if not isinstance(node, dict):
            continue
        if node.get("@type") == "Service" and "Bielefeld" in str(node.get("name", "")):
            node["name"] = "Betonlogistik und Transporte – Bielefeld & Gütersloh"
            node["description"] = "Betonpumpendienst und Transporte für Bielefeld, Gütersloh und das nördliche Ostwestfalen. RN Transporte aus Salzkotten für Baustellen, Betonwerke und Schüttgüter."
            node["areaServed"] = [
                {"@type": "City", "name": "Bielefeld"},
                {"@type": "City", "name": "Gütersloh"},
                {"@type": "City", "name": "Herford"},
                {"@type": "City", "name": "Detmold"},
            ]
        if node.get("@type") == "BreadcrumbList":
            for item in node.get("itemListElement", []):
                if isinstance(item, dict) and "Bielefeld" in str(item.get("name", "")):
                    item["name"] = "Einsatzgebiet Bielefeld & Gütersloh"
    return data


bielefeld = rewrite_jsonld(bielefeld, refine_bielefeld_schema)
bielefeld_path.write_text(bielefeld, encoding="utf-8")

# Update every public occurrence of the regional short label, including the
# hub and the cross-links at the bottom of regional pages.
for path in Path(".").glob("*.html"):
    text = path.read_text(encoding="utf-8")
    text = text.replace("Bielefeld / OWL", "Bielefeld / Gütersloh")
    text = text.replace(
        "Paderborn/OWL, Lippstadt/Soest, Höxter/Warburg, Kassel/Nordhessen und Südniedersachsen",
        "Paderborn/Salzkotten, Bielefeld/Gütersloh, Lippstadt/Soest, Höxter/Warburg, Kassel/Nordhessen und Südniedersachsen",
    )
    path.write_text(text, encoding="utf-8")

# Regional links use root-relative URLs so Safari cannot resolve them against
# an accidental nested path.
for path in Path(".").glob("*.html"):
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'href="(betonlogistik-[a-z0-9-]+\.html)"', r'href="/\1"', text, flags=re.I)
    path.write_text(text, encoding="utf-8")

# The first regional row was still unreliable on iOS although the generated
# target exists. Make that one destination fully explicit and keep the whole
# regional link layer above neighbouring decorative/CTA layers.
paderborn_target = Path("betonlogistik-paderborn-salzkotten.html")
if not paderborn_target.is_file():
    raise SystemExit("RN Paderborn/Salzkotten target page missing")
services_path = Path("leistungen.html")
services = services_path.read_text(encoding="utf-8")
paderborn_relative = 'href="/betonlogistik-paderborn-salzkotten.html"'
paderborn_absolute = 'href="https://rn-transporte.de/betonlogistik-paderborn-salzkotten.html"'
if paderborn_relative not in services:
    raise SystemExit("RN Paderborn/Salzkotten hub link missing")
services = services.replace(paderborn_relative, paderborn_absolute, 1)
regional_link_hardening = r'''<style id="rn-regional-link-hardening">
.regional-focus{position:relative;z-index:10;isolation:isolate}
.regional-focus-links{position:relative;z-index:20}
.regional-focus-links a{position:relative;z-index:21;pointer-events:auto!important;touch-action:manipulation;-webkit-tap-highlight-color:rgba(0,0,0,0)}
</style>'''
if 'id="rn-regional-link-hardening"' not in services:
    if "</head>" not in services:
        raise SystemExit("RN regional link hardening head closing tag missing")
    services = services.replace("</head>", regional_link_hardening + "\n</head>", 1)
services_path.write_text(services, encoding="utf-8")

# Holztransporte came from an older company description and are not treated as
# a confirmed current service. Remove those legacy references from the public
# artifact instead of inferring a service from old copy.
WOOD_TEXT_REPLACEMENTS = {
    "Unser Leistungsspektrum umfasst den Transport von Frischbeton mit Fahrmischern, Baustofftransporte mit Sattelkippern, Holztransporte sowie das fachgerechte Fördern und Pumpen von Beton mit unseren Betonpumpen.":
        "Unser Leistungsspektrum umfasst den Transport von Frischbeton mit Fahrmischern, Baustofftransporte mit Sattelkippern sowie das fachgerechte Fördern und Pumpen von Beton mit unseren Betonpumpen.",
    "Betonpumpendienst, Frischbeton-, Baustoff-, Kies- und Holztransporte aus Salzkotten. Bundesweit im Einsatz.":
        "Betonpumpendienst, Frischbeton-, Baustoff- und Kiestransporte aus Salzkotten. Bundesweit im Einsatz.",
    "RN Transporte aus Salzkotten: Betonpumpendienst, Frischbeton-, Baustoff-, Kies- und Holztransporte. Bundesweit im Einsatz – jetzt Projekt anfragen.":
        "RN Transporte aus Salzkotten: Betonpumpendienst, Frischbeton-, Baustoff- und Kiestransporte. Bundesweit im Einsatz – jetzt Projekt anfragen.",
}


def is_wood_offer(value):
    if not isinstance(value, dict) or value.get("@type") != "Offer":
        return False
    offered = value.get("itemOffered")
    return isinstance(offered, dict) and offered.get("name") == "Holztransporte"


def clean_wood_json(value):
    if isinstance(value, list):
        return [clean_wood_json(item) for item in value if not is_wood_offer(item)]
    if isinstance(value, dict):
        return {key: clean_wood_json(item) for key, item in value.items()}
    if isinstance(value, str):
        for old, new in WOOD_TEXT_REPLACEMENTS.items():
            value = value.replace(old, new)
    return value


for path in Path(".").glob("*.html"):
    text = path.read_text(encoding="utf-8")
    for old, new in WOOD_TEXT_REPLACEMENTS.items():
        text = text.replace(old, new)
    text = re.sub(
        r'\s*<article class="service-text-row service-text-row-wood" id="holztransporte">.*?</article>\s*',
        "\n",
        text,
        count=1,
        flags=re.S,
    )
    text = rewrite_jsonld(text, clean_wood_json)
    path.write_text(text, encoding="utf-8")

# Apply the uploaded social preview after final page content is established.
subprocess.check_call([sys.executable, ".github/social_preview.py"])

# Older build stages still emit the former GitHub Pages base URL. Normalize it
# once at the very end so every canonical/social/schema URL is production-only.
public_paths = list(Path(".").glob("*.html")) + [Path("robots.txt"), Path("sitemap.xml")]
for path in public_paths:
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    text = text.replace(OLD_SITE, PRODUCTION_SITE)
    path.write_text(text, encoding="utf-8")

# --- Final validation: no stale labels, no unconfirmed services, no bad URLs. ---
services_path = Path("leistungen.html")
services = services_path.read_text(encoding="utf-8")
for label in (
    "Paderborn / Salzkotten",
    "Bielefeld / Gütersloh",
    "Lippstadt / Soest / Geseke",
    "Höxter / Warburg",
    "Kassel / Nordhessen",
    "Südniedersachsen",
):
    if label not in services:
        raise SystemExit(f"RN final region label missing: {label}")
for stale in ("Bielefeld / OWL", "Gütersloh / Lippstadt / Soest"):
    if stale in services:
        raise SystemExit(f"RN final stale region label remains: {stale}")
if paderborn_absolute not in services or 'id="rn-regional-link-hardening"' not in services:
    raise SystemExit("RN Paderborn/Salzkotten link hardening missing")


def local_target(value: str):
    value = value.strip()
    if not value or value.startswith(("#", "http://", "https://", "mailto:", "tel:", "javascript:", "data:")):
        return None
    clean = value.split("#", 1)[0].split("?", 1)[0].lstrip("/")
    return Path(clean) if clean else None


for html_path in Path(".").glob("*.html"):
    html = html_path.read_text(encoding="utf-8")
    if OLD_SITE in html:
        raise SystemExit(f"RN final old URL remains in {html_path}")
    if "Holztransporte" in html:
        raise SystemExit(f"RN unconfirmed Holztransporte reference remains in {html_path}")
    for attr, value in re.findall(r'\b(href|src)="([^"]+)"', html, flags=re.I):
        target = local_target(value)
        if target is None:
            continue
        if attr.lower() == "href" and not str(target).lower().endswith(".html"):
            continue
        if not target.exists():
            raise SystemExit(f"RN final broken local {attr} in {html_path}: {value}")
