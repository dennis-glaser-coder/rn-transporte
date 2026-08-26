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


def replace_meta(html: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, html, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"RN final {label} not found exactly once")
    return updated


def rewrite_jsonld(html: str, transform):
    matches = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
    for match in reversed(matches):
        try:
            data = json.loads(match.group(1))
        except Exception:
            continue
        updated = transform(data)
        if updated is None:
            continue
        script = '<script type="application/ld+json">' + json.dumps(updated, ensure_ascii=False, separators=(",", ":")) + '</script>'
        html = html[:match.start()] + script + html[match.end():]
    return html


# --- Regional grouping: no overlapping OWL umbrella in the visible list. ---
# Paderborn and Höxter already have their own regional entries, so the second
# group is deliberately the concrete Bielefeld/Gütersloh corridor.
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
        return None
    changed = False
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
            changed = True
        if node.get("@type") == "BreadcrumbList":
            for item in node.get("itemListElement", []):
                if isinstance(item, dict) and "Bielefeld" in str(item.get("name", "")):
                    item["name"] = "Einsatzgebiet Bielefeld & Gütersloh"
                    changed = True
    return data if changed else None


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
# an accidental nested path. No JavaScript interception is necessary.
for path in Path(".").glob("*.html"):
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'href="(betonlogistik-[a-z0-9-]+\.html)"', r'href="/\1"', text, flags=re.I)
    path.write_text(text, encoding="utf-8")

# --- Service consistency: Holztransporte are part of the actual offer. ---
services_path = Path("leistungen.html")
services = services_path.read_text(encoding="utf-8")
services_title = "Betonpumpendienst, Frischbeton-, Kies- & Holztransporte | RN Transporte"
services_desc = "Betonpumpendienst, Frischbeton-, Kies-, Baustoff- und Holztransporte von RN Transporte aus Salzkotten. Zuverlässig für Baustellen und Auftraggeber – deutschlandweit im Einsatz."
services = replace_meta(services, r'<title>.*?</title>', f'<title>{services_title}</title>', "services title")
services = replace_meta(services, r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{services_desc}">', "services description")
services = replace_meta(services, r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{services_title}">', "services OG title")
services = replace_meta(services, r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{services_desc}">', "services OG description")
services = replace_meta(services, r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{services_title}">', "services Twitter title")
services = replace_meta(services, r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{services_desc}">', "services Twitter description")
if 'id="holztransporte"' not in services:
    raise SystemExit("RN final Holztransporte section missing")
services_path.write_text(services, encoding="utf-8")

# Keep the homepage overview aligned with the complete service offer without
# making the hero line longer.
home = Path("index.html")
home_html = home.read_text(encoding="utf-8")
home_html = home_html.replace(
    "Betonpumpendienst, Frischbeton- und Kiestransporte.</p>",
    "Betonpumpendienst, Frischbeton-, Kies- und Holztransporte.</p>",
    1,
)
home.write_text(home_html, encoding="utf-8")

# Regional pages link to all four service categories. Holztransporte use the
# anchored service overview until a dedicated Holztransport page/photo exists.
regional_service_old = (
    '<div class="regional-service-links"><a href="betonpumpendienst.html">Betonpumpendienst</a>'
    '<a href="frischbetontransporte.html">Frischbetontransporte</a>'
    '<a href="kiestransporte.html">Kiestransporte</a></div>'
)
regional_service_new = (
    '<div class="regional-service-links"><a href="/betonpumpendienst.html">Betonpumpendienst</a>'
    '<a href="/frischbetontransporte.html">Frischbetontransporte</a>'
    '<a href="/kiestransporte.html">Kiestransporte</a>'
    '<a href="/leistungen.html#holztransporte">Holztransporte</a></div>'
)
for path in Path(".").glob("betonlogistik-*.html"):
    text = path.read_text(encoding="utf-8")
    if regional_service_old not in text:
        raise SystemExit(f"RN final regional service links missing: {path}")
    text = text.replace(regional_service_old, regional_service_new, 1)
    text = text.replace(
        '.regional-service-links{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));',
        '.regional-service-links{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));',
        1,
    )
    path.write_text(text, encoding="utf-8")

# Apply the uploaded social preview after final page content is established.
try:
    import PIL  # noqa: F401
except ModuleNotFoundError:
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "--disable-pip-version-check",
        "--quiet",
        "Pillow",
    ])
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

# --- Final validation: no stale labels, no old host, no broken local targets. ---
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
    for attr, value in re.findall(r'\b(href|src)="([^"]+)"', html, flags=re.I):
        target = local_target(value)
        if target is None:
            continue
        if attr.lower() == "href" and not str(target).lower().endswith(".html"):
            continue
        if not target.exists():
            raise SystemExit(f"RN final broken local {attr} in {html_path}: {value}")
