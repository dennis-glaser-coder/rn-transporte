from pathlib import Path
from datetime import date
import json
import re

SITE = "https://rn-transporte.de/"
TODAY = date.today().isoformat()
CONTACT_EMAIL = "kontakt@rn-transporte.de"
PHONE = "+49 173 7275165"
LEGAL_NAME = "RN Torwesten Transporte UG (haftungsbeschränkt)"
BRAND = "RN Transporte"

IMPORTANT = {
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
}


def canonical_for(path: Path) -> str:
    if path.name == "index.html" and path.parent == Path("."):
        return SITE
    if path.name == "index.html" and path.parent != Path("."):
        return SITE + path.parent.as_posix().strip("/") + "/"
    return SITE + path.as_posix().lstrip("./")


def ensure_canonical(path: Path):
    html = path.read_text(encoding="utf-8")
    url = canonical_for(path)
    if re.search(r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?>', html, flags=re.I):
        html = re.sub(r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?>', f'<link rel="canonical" href="{url}">', html, count=1, flags=re.I)
    elif "</head>" in html:
        html = html.replace("</head>", f'<link rel="canonical" href="{url}">\n</head>', 1)
    if '<meta name="robots"' in html:
        html = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="index,follow,max-image-preview:large">', html, count=1)
    path.write_text(html, encoding="utf-8")


def org_node():
    return {
        "@type": ["Organization", "LocalBusiness"],
        "@id": SITE + "#organization",
        "name": BRAND,
        "legalName": LEGAL_NAME,
        "url": SITE,
        "logo": SITE + "assets/logo.webp",
        "image": SITE + "assets/rn-social-preview.jpg",
        "telephone": PHONE,
        "email": CONTACT_EMAIL,
        "foundingDate": "2010-04-13",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Lohweg 55a",
            "postalCode": "33154",
            "addressLocality": "Salzkotten",
            "addressRegion": "Nordrhein-Westfalen",
            "addressCountry": "DE",
        },
        "areaServed": [
            {"@type": "AdministrativeArea", "name": "Kreis Paderborn"},
            {"@type": "AdministrativeArea", "name": "Ostwestfalen-Lippe"},
            {"@type": "AdministrativeArea", "name": "Kreis Soest"},
            {"@type": "AdministrativeArea", "name": "Kreis Höxter"},
            {"@type": "AdministrativeArea", "name": "Nordhessen"},
            {"@type": "AdministrativeArea", "name": "Südniedersachsen"},
            {"@type": "Country", "name": "Deutschland"},
        ],
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": PHONE,
            "email": CONTACT_EMAIL,
            "contactType": "customer service",
            "availableLanguage": "de",
        },
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Leistungen",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Betonpumpendienst", "url": SITE + "betonpumpendienst.html"}},
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Frischbetontransporte", "url": SITE + "frischbetontransporte.html"}},
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Kies- und Schüttguttransporte", "url": SITE + "kiestransporte.html"}},
            ],
        },
    }


def strengthen_home_schema():
    path = Path("index.html")
    html = path.read_text(encoding="utf-8")
    scripts = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
    organization_done = False
    website_done = False
    for match in reversed(scripts):
        try:
            data = json.loads(match.group(1))
        except Exception:
            continue
        changed = False
        nodes = data.get("@graph") if isinstance(data, dict) else None
        candidates = nodes if isinstance(nodes, list) else [data] if isinstance(data, dict) else []
        for node in candidates:
            if not isinstance(node, dict):
                continue
            types = node.get("@type")
            types = types if isinstance(types, list) else [types]
            if "Organization" in types or "LocalBusiness" in types:
                node.clear()
                node.update(org_node())
                organization_done = True
                changed = True
            if "WebSite" in types:
                node.update({"@type": "WebSite", "@id": SITE + "#website", "url": SITE, "name": "RN Transporte", "alternateName": "RN Torwesten Transporte", "publisher": {"@id": SITE + "#organization"}})
                website_done = True
                changed = True
        if changed:
            replacement = '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + '</script>'
            html = html[:match.start()] + replacement + html[match.end():]
    additions = []
    if not organization_done:
        additions.append(org_node())
    if not website_done:
        additions.append({"@type": "WebSite", "@id": SITE + "#website", "url": SITE, "name": "RN Transporte", "alternateName": "RN Torwesten Transporte", "publisher": {"@id": SITE + "#organization"}})
    if additions:
        script = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": additions}, ensure_ascii=False, separators=(",", ":")) + '</script>'
        html = html.replace("</head>", script + "\n</head>", 1)
    path.write_text(html, encoding="utf-8")


def strengthen_nested_page(path: Path):
    if not path.is_file():
        return
    html = path.read_text(encoding="utf-8")
    html = html.replace('../assets/logo.svg', '../assets/logo.webp')
    scripts = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
    for match in reversed(scripts):
        try:
            data = json.loads(match.group(1))
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        graph = data.get("@graph")
        candidates = graph if isinstance(graph, list) else [data]
        changed = False
        for node in candidates:
            if not isinstance(node, dict) or node.get("@type") != "Service":
                continue
            node["url"] = canonical_for(path)
            node["provider"] = {
                "@type": "Organization",
                "@id": SITE + "#organization",
                "name": BRAND,
                "legalName": LEGAL_NAME,
                "url": SITE,
                "telephone": PHONE,
                "email": CONTACT_EMAIL,
                "address": org_node()["address"],
            }
            changed = True
        if changed:
            replacement = '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + '</script>'
            html = html[:match.start()] + replacement + html[match.end():]
            break
    path.write_text(html, encoding="utf-8")


def add_pump_region_links():
    path = Path("betonpumpendienst.html")
    html = path.read_text(encoding="utf-8")
    marker = 'id="rn-pump-region-links"'
    if marker in html:
        return
    section = '''
<section class="rn-pump-regions" id="rn-pump-region-links"><div class="wrap rn-pump-regions-inner"><span class="rn-pump-regions-label">Betonpumpendienst in der Region</span><div class="rn-pump-regions-links"><a href="/betonpumpe-salzkotten/">Betonpumpe Salzkotten</a><a href="/betonpumpe-paderborn/">Betonpumpe Paderborn</a><a href="/betonpumpe-owl/">Betonpumpe OWL</a></div></div></section>
'''
    style = '''<style id="rn-pump-region-style">.rn-pump-regions{padding:0 0 96px;background:#fff}.rn-pump-regions-inner{padding-top:34px;border-top:1px solid #d8dada}.rn-pump-regions-label{display:block;margin-bottom:18px;color:#757a7e;font-size:9px;font-weight:780;letter-spacing:.15em;text-transform:uppercase}.rn-pump-regions-links{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid #e0e1e1;border-bottom:1px solid #e0e1e1}.rn-pump-regions-links a{display:flex;align-items:center;justify-content:space-between;min-height:68px;padding:0 18px;color:#24272a;font-size:14px;font-weight:610}.rn-pump-regions-links a+a{border-left:1px solid #e0e1e1}.rn-pump-regions-links a:after{content:"→";color:var(--red);font-size:17px}@media(max-width:900px){.rn-pump-regions{padding-bottom:66px}.rn-pump-regions-links{grid-template-columns:1fr}.rn-pump-regions-links a+a{border-left:0;border-top:1px solid #e0e1e1}}</style>'''
    html = html.replace("</head>", style + "\n</head>", 1)
    html = html.replace("</main>", section + "</main>", 1)
    path.write_text(html, encoding="utf-8")


def add_home_discovery_links():
    path = Path("index.html")
    html = path.read_text(encoding="utf-8")
    if 'id="rn-home-discovery-links"' in html:
        return
    links = '''<nav class="rn-home-discovery" id="rn-home-discovery-links" aria-label="Betonpumpendienst und Einsatzgebiete"><div class="wrap rn-home-discovery-inner"><span>Betonpumpendienst:</span><a href="/betonpumpe-salzkotten/">Salzkotten</a><a href="/betonpumpe-paderborn/">Paderborn</a><a href="/betonpumpe-owl/">OWL</a><span class="rn-home-discovery-sep">Einsatzgebiete:</span><a href="/betonlogistik-paderborn-salzkotten.html">Paderborn / Salzkotten</a><a href="/betonlogistik-bielefeld-owl.html">Bielefeld / Gütersloh</a><a href="/betonlogistik-guetersloh-lippstadt-soest.html">Lippstadt / Soest</a><a href="/betonlogistik-hoexter-warburg.html">Höxter / Warburg</a><a href="/betonlogistik-kassel-nordhessen.html">Kassel / Nordhessen</a><a href="/betonlogistik-suedniedersachsen.html">Südniedersachsen</a></div></nav>'''
    style = '''<style id="rn-home-discovery-style">.rn-home-discovery{border-top:1px solid rgba(255,255,255,.14);padding:17px 0 20px}.rn-home-discovery-inner{display:flex;flex-wrap:wrap;align-items:center;gap:7px 14px;color:rgba(255,255,255,.56);font-size:10px;line-height:1.5}.rn-home-discovery-inner span{font-weight:760;letter-spacing:.08em;text-transform:uppercase}.rn-home-discovery-inner a{color:rgba(255,255,255,.78);text-decoration:none}.rn-home-discovery-inner a:hover{color:#fff}.rn-home-discovery-sep{margin-left:10px}@media(max-width:700px){.rn-home-discovery{padding:16px 0 22px}.rn-home-discovery-inner{gap:6px 11px;font-size:10px}.rn-home-discovery-sep{width:100%;margin:5px 0 0}}</style>'''
    if "</head>" not in html or "</footer>" not in html:
        raise SystemExit("Homepage discovery insertion point missing")
    html = html.replace("</head>", style + "\n</head>", 1)
    html = html.replace("</footer>", links + "</footer>", 1)
    path.write_text(html, encoding="utf-8")


def add_sitemap_entries():
    path = Path("sitemap.xml")
    sitemap = path.read_text(encoding="utf-8")
    urls = [
        SITE + "betonpumpe-salzkotten/",
        SITE + "betonpumpe-paderborn/",
        SITE + "betonpumpe-owl/",
    ]
    entries = []
    for url in urls:
        if f"<loc>{url}</loc>" not in sitemap:
            entries.append(f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.9</priority>\n  </url>")
    if entries:
        sitemap = sitemap.replace("</urlset>", "\n" + "\n".join(entries) + "\n</urlset>", 1)
    path.write_text(sitemap, encoding="utf-8")


def make_service_title_unique():
    path = Path("betonpumpendienst.html")
    html = path.read_text(encoding="utf-8")
    old = "Betonpumpendienst & Transporte | RN Transporte Salzkotten"
    new = "Betonpumpendienst | RN Transporte Salzkotten"
    if f"<title>{old}</title>" not in html:
        raise SystemExit("Expected generic concrete-pump title not found")
    html = html.replace(f"<title>{old}</title>", f"<title>{new}</title>", 1)
    html = html.replace(f'<meta property="og:title" content="{old}">', f'<meta property="og:title" content="{new}">', 1)
    html = html.replace(f'<meta name="twitter:title" content="{old}">', f'<meta name="twitter:title" content="{new}">', 1)
    path.write_text(html, encoding="utf-8")


for html_path in list(Path(".").glob("*.html")) + list(Path(".").glob("*/index.html")):
    ensure_canonical(html_path)

strengthen_home_schema()
for nested in (Path("betonpumpe-salzkotten/index.html"), Path("betonpumpe-paderborn/index.html"), Path("betonpumpe-owl/index.html")):
    strengthen_nested_page(nested)
add_pump_region_links()
add_home_discovery_links()
add_sitemap_entries()
make_service_title_unique()

for nested in (Path("betonpumpe-salzkotten/index.html"), Path("betonpumpe-paderborn/index.html"), Path("betonpumpe-owl/index.html")):
    if nested.is_file():
        text = nested.read_text(encoding="utf-8")
        if '../assets/logo.svg' in text:
            raise SystemExit(f"Old nested logo path remains: {nested}")
        if CONTACT_EMAIL not in text:
            raise SystemExit(f"Current contact email missing from schema: {nested}")

if "<title>Betonpumpendienst | RN Transporte Salzkotten</title>" not in Path("betonpumpendienst.html").read_text(encoding="utf-8"):
    raise SystemExit("Unique Betonpumpendienst title missing")
if 'id="rn-home-discovery-links"' not in Path("index.html").read_text(encoding="utf-8"):
    raise SystemExit("Homepage discovery links missing")

print("RN Google discovery boost applied")
