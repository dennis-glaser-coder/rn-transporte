from pathlib import Path
from datetime import date
import json
import re

SITE_URL = "https://dennis-glaser-coder.github.io/rn-transporte/"
TODAY = date.today().isoformat()


def replace_once(html: str, old: str, new: str, label: str) -> str:
    if old not in html:
        raise SystemExit(f"RN regional SEO {label} not found")
    return html.replace(old, new, 1)


def replace_meta(html: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, html, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"RN regional SEO {label} not found")
    return updated


def jsonld(data) -> str:
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + '</script>'


def update_service_area_schema(html: str) -> str:
    scripts = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
    for match in scripts:
        try:
            data = json.loads(match.group(1))
        except Exception:
            continue
        nodes = data.get("@graph") if isinstance(data, dict) else None
        if not isinstance(nodes, list):
            continue
        changed = False
        for node in nodes:
            if isinstance(node, dict) and node.get("@type") == "Service":
                node["areaServed"] = [
                    {"@type": "AdministrativeArea", "name": "Kreis Paderborn"},
                    {"@type": "AdministrativeArea", "name": "Ostwestfalen-Lippe"},
                    {"@type": "AdministrativeArea", "name": "Kreis Soest"},
                    {"@type": "AdministrativeArea", "name": "Kreis Höxter"},
                    {"@type": "AdministrativeArea", "name": "Nordhessen"},
                    {"@type": "AdministrativeArea", "name": "Südniedersachsen"},
                    {"@type": "Country", "name": "Deutschland"},
                ]
                changed = True
        if changed:
            return html[:match.start()] + jsonld(data) + html[match.end():]
    raise SystemExit("RN regional SEO service schema not found")


def update_org_area_schema(html: str) -> str:
    scripts = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S))
    for match in scripts:
        try:
            data = json.loads(match.group(1))
        except Exception:
            continue
        nodes = data.get("@graph") if isinstance(data, dict) else None
        candidates = nodes if isinstance(nodes, list) else [data] if isinstance(data, dict) else []
        changed = False
        for node in candidates:
            if not isinstance(node, dict):
                continue
            types = node.get("@type")
            type_list = types if isinstance(types, list) else [types]
            if "Organization" in type_list or "LocalBusiness" in type_list:
                node["areaServed"] = [
                    {"@type": "AdministrativeArea", "name": "Kreis Paderborn"},
                    {"@type": "AdministrativeArea", "name": "Ostwestfalen-Lippe"},
                    {"@type": "AdministrativeArea", "name": "Kreis Soest"},
                    {"@type": "AdministrativeArea", "name": "Kreis Höxter"},
                    {"@type": "AdministrativeArea", "name": "Nordhessen"},
                    {"@type": "AdministrativeArea", "name": "Südniedersachsen"},
                    {"@type": "Country", "name": "Deutschland"},
                ]
                changed = True
        if changed:
            return html[:match.start()] + jsonld(data) + html[match.end():]
    return html


REGIONS = [
    {
        "filename": "betonlogistik-paderborn-salzkotten.html",
        "name": "Paderborn & Salzkotten",
        "short": "Paderborn / Salzkotten",
        "title": "Betonlogistik & Transporte Paderborn | RN Transporte",
        "description": "Betonpumpendienst, Frischbeton- und Kiestransporte für Paderborn, Salzkotten und den Kreis Paderborn. RN Transporte mit kurzen Wegen aus Salzkotten.",
        "hero": "Betonlogistik für Paderborn und den Kreis.",
        "intro": "Kurze Wege aus Salzkotten für Betonpumpendienst, Frischbeton- und Kiestransporte im direkten Umfeld.",
        "heading": "Direkt aus Salzkotten in den Kreis Paderborn.",
        "paragraphs": [
            "Unser Standort in Salzkotten liegt mitten im Kerngebiet. Dadurch können Einsätze im Raum Paderborn, Delbrück, Büren und Bad Wünnenberg mit kurzen Abstimmungswegen geplant werden.",
            "RN Transporte unterstützt Baustellen und Betonwerke mit Betonpumpendienst, Fahrmischern sowie Kies- und Schüttguttransporten. Für größere oder überregionale Projekte sind wir weiterhin deutschlandweit im Einsatz.",
        ],
        "places": ["Salzkotten", "Paderborn", "Delbrück", "Büren", "Bad Wünnenberg"],
        "image": "assets/leistungen/betonpumpendienst.png",
        "image_alt": "RN Transporte Betonlogistik im Raum Paderborn und Salzkotten",
    },
    {
        "filename": "betonlogistik-bielefeld-owl.html",
        "name": "Bielefeld & OWL",
        "short": "Bielefeld / OWL",
        "title": "Betonlogistik Bielefeld & OWL | RN Transporte",
        "description": "Betonpumpendienst und Transporte für Bielefeld und Ostwestfalen-Lippe. RN Transporte aus Salzkotten für Baustellen, Betonwerke und Schüttgüter.",
        "hero": "Betonlogistik für Bielefeld und OWL.",
        "intro": "Zuverlässige Einsätze in Ostwestfalen-Lippe – von Salzkotten aus direkt abgestimmt.",
        "heading": "Für Baustellen und Betonwerke in Ostwestfalen-Lippe.",
        "paragraphs": [
            "Für Projekte in Richtung Bielefeld, Gütersloh, Herford und Detmold verbindet RN Transporte kurze regionale Wege mit eingespielten Abläufen in der Beton- und Baustellenlogistik.",
            "Je nach Bedarf koordinieren wir Betonpumpendienst, Frischbetontransporte und Kies- beziehungsweise Schüttguttransporte. Ansprechpartner und Einsatzplanung bleiben dabei zentral in Salzkotten.",
        ],
        "places": ["Bielefeld", "Gütersloh", "Herford", "Detmold", "Ostwestfalen-Lippe"],
        "image": "assets/leistungen/frischbetontransport.png",
        "image_alt": "RN Transporte Frischbetontransport in Ostwestfalen-Lippe",
    },
    {
        "filename": "betonlogistik-guetersloh-lippstadt-soest.html",
        "name": "Lippstadt, Soest & Geseke",
        "short": "Lippstadt / Soest / Geseke",
        "title": "Betonlogistik Lippstadt, Soest & Geseke | RN Transporte",
        "description": "Betonpumpendienst, Frischbeton- und Kiestransporte im Raum Lippstadt, Soest und Geseke. RN Transporte koordiniert Einsätze aus Salzkotten.",
        "hero": "Betonlogistik für Lippstadt, Soest und Geseke.",
        "intro": "Regional gut erreichbar für Baustellen im Raum Lippstadt, Geseke und Soest.",
        "heading": "Kurze Wege für Baustellen westlich von Salzkotten.",
        "paragraphs": [
            "Geseke und Lippstadt liegen unmittelbar westlich unseres Standorts; auch Erwitte, Anröchte und Soest gehören zu unserem regionalen Kerngebiet. Das erleichtert die direkte Abstimmung bei zeitkritischen Baustelleneinsätzen.",
            "Wir übernehmen Betonpumpeneinsätze, Fahrmischertransporte sowie Kies- und Schüttguttransporte und stimmen die Logistik passend zum Ablauf vor Ort ab.",
        ],
        "places": ["Lippstadt", "Geseke", "Erwitte", "Anröchte", "Soest"],
        "image": "assets/leistungen/Kiestransporte.png",
        "image_alt": "RN Transporte Baustofftransport im Raum Lippstadt und Soest",
    },
    {
        "filename": "betonlogistik-hoexter-warburg.html",
        "name": "Höxter & Warburg",
        "short": "Höxter / Warburg",
        "title": "Betonlogistik Höxter & Warburg | RN Transporte",
        "description": "Betonpumpendienst und Transporte für Höxter, Warburg und den Kreis Höxter. RN Transporte aus Salzkotten für Beton- und Baustellenlogistik.",
        "hero": "Betonlogistik für Höxter und Warburg.",
        "intro": "Betonpumpendienst und Transporte für den östlichen Teil des regionalen Kerngebiets.",
        "heading": "Zuverlässig in Richtung Höxter und Warburg.",
        "paragraphs": [
            "Der Kreis Höxter mit Warburg, Brakel, Höxter und Beverungen liegt gut erreichbar östlich von Salzkotten. Für Baustellen in dieser Region planen wir Einsätze mit direkter Abstimmung und klaren Ansprechpartnern.",
            "Unsere Leistungen reichen vom Betonpumpendienst über Frischbetontransporte bis zu Kies- und Schüttguttransporten. Auch weiter entfernte Projekte können nach Abstimmung übernommen werden.",
        ],
        "places": ["Höxter", "Warburg", "Brakel", "Beverungen", "Kreis Höxter"],
        "image": "assets/leistungen/betonpumpendienst.png",
        "image_alt": "RN Transporte Betonpumpendienst im Raum Höxter und Warburg",
    },
    {
        "filename": "betonlogistik-kassel-nordhessen.html",
        "name": "Kassel & Nordhessen",
        "short": "Kassel / Nordhessen",
        "title": "Betonlogistik Kassel & Nordhessen | RN Transporte",
        "description": "Betonpumpendienst, Frischbeton- und Kiestransporte für Kassel und Nordhessen. RN Transporte plant Einsätze von Salzkotten aus.",
        "hero": "Betonlogistik für Kassel und Nordhessen.",
        "intro": "Von Salzkotten aus zuverlässig in Richtung Kassel und das nordhessische Umland.",
        "heading": "Beton- und Transportlogistik für Nordhessen.",
        "paragraphs": [
            "Kassel und das nordhessische Umland gehören zu den Regionen, die wir von Salzkotten aus gut erreichen. Gerade bei Baustellen mit Betonbedarf sind verlässliche Zeitfenster und direkte Kommunikation entscheidend.",
            "RN Transporte koordiniert Betonpumpendienst, Frischbetontransporte sowie Kies- und Schüttguttransporte aus einer Hand und stimmt den Einsatz mit Baustelle und Betonwerk ab.",
        ],
        "places": ["Kassel", "Hofgeismar", "Wolfhagen", "Nordhessen"],
        "image": "assets/leistungen/frischbetontransport.png",
        "image_alt": "RN Transporte Betonlogistik für Kassel und Nordhessen",
    },
    {
        "filename": "betonlogistik-suedniedersachsen.html",
        "name": "Südniedersachsen",
        "short": "Südniedersachsen",
        "title": "Betonlogistik Südniedersachsen | RN Transporte",
        "description": "Betonpumpendienst und Transporte für Südniedersachsen, unter anderem Holzminden, Göttingen und Northeim. RN Transporte aus Salzkotten.",
        "hero": "Betonlogistik für Südniedersachsen.",
        "intro": "Planbare Baustelleneinsätze nördlich und östlich unseres Standorts in Salzkotten.",
        "heading": "Im Einsatz zwischen Holzminden, Göttingen und Northeim.",
        "paragraphs": [
            "Für Projekte in Südniedersachsen erreichen wir unter anderem den Raum Holzminden, Göttingen und Northeim von Salzkotten aus. Die regionale Nähe ermöglicht eine unkomplizierte Abstimmung für planbare Baustelleneinsätze.",
            "Zum Leistungsspektrum gehören Betonpumpendienst, Frischbetontransporte sowie Kies- und Schüttguttransporte. Deutschlandweite Einsätze bleiben darüber hinaus weiterhin möglich.",
        ],
        "places": ["Holzminden", "Göttingen", "Northeim", "Südniedersachsen"],
        "image": "assets/leistungen/Baustelleneinsatz.png",
        "image_alt": "RN Transporte Baustelleneinsatz in Südniedersachsen",
    },
]


services_path = Path("leistungen.html")
services_html = services_path.read_text(encoding="utf-8")
if 'id="rn-regional-focus"' in services_html:
    raise SystemExit("RN regional SEO focus already present")

region_links = ''.join(
    f'<a href="{r["filename"]}"><span>{r["short"]}</span><span aria-hidden="true">→</span></a>'
    for r in REGIONS
)
regional_hub = f'''
<section class="regional-focus" id="einsatzgebiet">
  <div class="regional-focus-head"><span class="regional-focus-kicker">Regionales Kerngebiet</span><h2>Rund um Salzkotten besonders nah am Einsatz.</h2><p>Unser Schwerpunkt liegt im Umkreis von rund 150 km um Salzkotten. Darüber hinaus übernimmt RN Transporte weiterhin deutschlandweite Einsätze nach Abstimmung.</p></div>
  <div class="regional-focus-links">{region_links}</div>
</section>
'''
services_html = replace_once(services_html, '    <div class="page-cta service-page-cta">', regional_hub + '\n    <div class="page-cta service-page-cta">', "services CTA anchor")

regional_hub_style = r'''<style id="rn-regional-focus">
.regional-focus{margin-top:94px;padding:52px 0 8px;border-top:1px solid #d8dada}
.regional-focus-head{display:grid;grid-template-columns:minmax(150px,.42fr) minmax(0,1.1fr) minmax(300px,.7fr);gap:38px;align-items:start}
.regional-focus-kicker{padding-top:8px;color:#74797d;font-size:9px;font-weight:780;letter-spacing:.16em;text-transform:uppercase}
.regional-focus h2{margin:0;color:#1d2022;font-size:clamp(32px,3.55vw,48px);line-height:1;letter-spacing:-.052em;font-weight:510;text-wrap:balance}
.regional-focus p{margin:4px 0 0;color:#686d71;font-size:14px;line-height:1.68}
.regional-focus-links{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));margin-top:38px;border-top:1px solid #d8dada;border-bottom:1px solid #d8dada}
.regional-focus-links a{display:flex;align-items:center;justify-content:space-between;gap:18px;min-height:70px;padding:0 18px;color:#24272a;font-size:12px;font-weight:650;border-right:1px solid #e0e1e1}
.regional-focus-links a:nth-child(3n){border-right:0}.regional-focus-links a:nth-child(n+4){border-top:1px solid #e0e1e1}
.regional-focus-links a span:last-child{color:var(--red);font-size:16px}
@media(hover:hover){.regional-focus-links a:hover{background:#f7f7f5}}
@media(max-width:900px){.regional-focus{margin-top:64px;padding-top:38px}.regional-focus-head{grid-template-columns:1fr;gap:13px}.regional-focus-kicker{padding-top:0}.regional-focus h2{font-size:34px}.regional-focus p{font-size:13px}.regional-focus-links{grid-template-columns:1fr 1fr;margin-top:28px}.regional-focus-links a,.regional-focus-links a:nth-child(3n){border-right:1px solid #e0e1e1}.regional-focus-links a:nth-child(2n){border-right:0}.regional-focus-links a:nth-child(n+3){border-top:1px solid #e0e1e1}}
@media(max-width:520px){.regional-focus-links{grid-template-columns:1fr}.regional-focus-links a,.regional-focus-links a:nth-child(n){min-height:58px;padding:0 4px;border-right:0}.regional-focus-links a:nth-child(n+2){border-top:1px solid #e0e1e1}}
</style>'''
services_html = services_html.replace("</head>", regional_hub_style + "\n</head>", 1)
services_path.write_text(services_html, encoding="utf-8")


service_files = ("betonpumpendienst.html", "frischbetontransporte.html", "kiestransporte.html")
service_focus_style = r'''<style id="rn-service-regional-focus">
.seo-regional-note{margin-top:18px;padding:16px 18px;border-left:2px solid var(--red);background:#f6f6f4;color:#5f6468;font-size:12px;line-height:1.6}
.seo-regional-note strong{color:#25282b}.seo-regional-note a{color:#25282b;font-weight:680;border-bottom:1px solid #c9cbcb}
@media(hover:hover){.seo-regional-note a:hover{color:var(--red);border-color:var(--red)}}
</style>'''
for filename in service_files:
    path = Path(filename)
    html = path.read_text(encoding="utf-8")
    if 'id="rn-service-regional-focus"' in html:
        raise SystemExit(f"RN service regional focus already present: {filename}")
    note = '<div class="seo-regional-note"><strong>Regionales Kerngebiet:</strong> rund 150 km um Salzkotten – unter anderem Paderborn/OWL, Lippstadt/Soest, Höxter/Warburg, Kassel/Nordhessen und Südniedersachsen. <a href="leistungen.html#einsatzgebiet">Regionen ansehen →</a></div>'
    html = replace_once(html, '    <div class="seo-service-actions">', note + '\n    <div class="seo-service-actions">', f"regional note {filename}")
    html = html.replace("</head>", service_focus_style + "\n</head>", 1)
    html = update_service_area_schema(html)
    path.write_text(html, encoding="utf-8")


regional_page_style = r'''<style id="rn-regional-page">
.regional-page{padding:90px 0 102px;background:#fff}
.regional-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(390px,.82fr);gap:76px;align-items:center}
.regional-media{overflow:hidden;background:#ececea;box-shadow:0 24px 58px rgba(22,24,26,.055)}
.regional-media img{display:block;width:100%;aspect-ratio:16/10;object-fit:cover;filter:saturate(.84) contrast(1.025)}
.regional-copy{max-width:650px}.regional-kicker{display:block;margin-bottom:18px;color:#767b7f;font-size:9px;font-weight:780;letter-spacing:.16em;text-transform:uppercase}
.regional-copy h2{margin:0;color:#191b1e;font-size:clamp(35px,3.65vw,51px);line-height:1;letter-spacing:-.052em;font-weight:510;text-wrap:balance}
.regional-copy p{margin:19px 0 0;color:#5f6468;font-size:15px;line-height:1.74}
.regional-facts{display:grid;grid-template-columns:1fr 1fr;margin-top:28px;border-top:1px solid #dedfdf;border-bottom:1px solid #dedfdf}
.regional-facts span{padding:18px 0;color:#666b6f;font-size:12px;line-height:1.45}.regional-facts span+span{padding-left:24px;border-left:1px solid #dedfdf}
.regional-facts strong{display:block;margin-bottom:4px;color:#24272a;font-size:9px;letter-spacing:.12em;text-transform:uppercase}
.regional-places{margin-top:24px}.regional-places strong{display:block;margin-bottom:10px;color:#24272a;font-size:9px;letter-spacing:.12em;text-transform:uppercase}.regional-place-list{display:flex;flex-wrap:wrap;gap:7px}.regional-place-list span{padding:7px 10px;background:#f3f3f1;color:#5c6165;font-size:11px}
.regional-actions{display:flex;gap:10px;margin-top:30px}.regional-actions a{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 18px;font-size:11px;font-weight:760;letter-spacing:.035em;text-transform:uppercase}.regional-actions .primary{background:var(--red);color:#fff}.regional-actions .secondary{border:1px solid #d0d2d2;color:#292c2f;background:#fff}
.regional-services{padding:0 0 92px;background:#fff}.regional-services-inner{padding-top:34px;border-top:1px solid #d8dada}.regional-services-label{display:block;margin-bottom:20px;color:#757a7e;font-size:9px;font-weight:780;letter-spacing:.15em;text-transform:uppercase}.regional-service-links{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid #e0e1e1;border-bottom:1px solid #e0e1e1}.regional-service-links a{display:flex;align-items:center;justify-content:space-between;min-height:70px;padding:0 18px;color:#24272a;font-size:13px;font-weight:620}.regional-service-links a+a{border-left:1px solid #e0e1e1}.regional-service-links a:after{content:"→";color:var(--red);font-size:16px}
.regional-other{padding:0 0 100px;background:#fff}.regional-other-inner{padding-top:32px;border-top:1px solid #d8dada}.regional-other-links{display:flex;flex-wrap:wrap;gap:8px}.regional-other-links a{padding:9px 12px;background:#f3f3f1;color:#4f5458;font-size:11px}
@media(hover:hover){.regional-actions .primary:hover{background:var(--red-dark)}.regional-actions .secondary:hover,.regional-service-links a:hover,.regional-other-links a:hover{background:#f7f7f5}}
@media(max-width:900px){.regional-page{padding:58px 0 72px}.regional-grid{grid-template-columns:1fr;gap:36px}.regional-media{order:1}.regional-copy{order:2;max-width:none}.regional-copy h2{font-size:36px}.regional-copy p{font-size:14px}.regional-services{padding-bottom:68px}.regional-service-links{grid-template-columns:1fr}.regional-service-links a+a{border-left:0;border-top:1px solid #e0e1e1}.regional-other{padding-bottom:70px}}
@media(max-width:430px){.regional-page{padding-top:50px}.regional-media{margin-left:-16px;margin-right:-16px}.regional-copy h2{font-size:33px}.regional-facts{grid-template-columns:1fr}.regional-facts span+span{padding-left:0;border-left:0;border-top:1px solid #dedfdf}.regional-actions{display:grid}.regional-actions a{width:100%}}
</style>'''

template = Path("betonpumpendienst.html").read_text(encoding="utf-8")
if not re.search(r'<main>.*?</main>', template, re.S):
    raise SystemExit("RN regional SEO template main not found")

for region in REGIONS:
    url = SITE_URL + region["filename"]
    image_url = SITE_URL + region["image"]
    page = template
    page = replace_meta(page, r'<title>.*?</title>', f'<title>{region["title"]}</title>', f'title {region["filename"]}')
    page = replace_meta(page, r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{region["description"]}">', f'description {region["filename"]}')
    page = replace_meta(page, r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{region["title"]}">', f'OG title {region["filename"]}')
    page = replace_meta(page, r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{region["description"]}">', f'OG description {region["filename"]}')
    page = replace_meta(page, r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', f'OG URL {region["filename"]}')
    page = replace_meta(page, r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{image_url}">', f'OG image {region["filename"]}')
    page = replace_meta(page, r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{region["title"]}">', f'Twitter title {region["filename"]}')
    page = replace_meta(page, r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{region["description"]}">', f'Twitter description {region["filename"]}')
    page = replace_meta(page, r'<meta name="twitter:image" content="[^"]*">', f'<meta name="twitter:image" content="{image_url}">', f'Twitter image {region["filename"]}')
    page = replace_meta(page, r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', f'canonical {region["filename"]}')

    paragraphs = ''.join(f'<p>{p}</p>' for p in region["paragraphs"])
    places = ''.join(f'<span>{p}</span>' for p in region["places"])
    other_links = ''.join(
        f'<a href="{other["filename"]}">{other["short"]}</a>'
        for other in REGIONS if other["filename"] != region["filename"]
    )
    main = f'''<main>
<section class="page-hero"><div class="wrap page-hero-grid"><div class="eyebrow">Einsatzgebiet</div><div><h1>{region["hero"]}</h1><p>{region["intro"]}</p></div></div></section>
<section class="regional-page"><div class="wrap regional-grid">
  <div class="regional-media"><img src="{region["image"]}" alt="{region["image_alt"]}" decoding="async" fetchpriority="high"></div>
  <div class="regional-copy"><span class="regional-kicker">RN Transporte · Standort Salzkotten</span><h2>{region["heading"]}</h2>{paragraphs}
    <div class="regional-facts"><span><strong>Kerngebiet</strong>Rund 150 km um Salzkotten</span><span><strong>Darüber hinaus</strong>Deutschlandweit nach Abstimmung</span></div>
    <div class="regional-places"><strong>Region im Fokus</strong><div class="regional-place-list">{places}</div></div>
    <div class="regional-actions"><a class="primary" href="kontakt.html">Einsatz anfragen →</a><a class="secondary" href="leistungen.html">Leistungen ansehen</a></div>
  </div>
</div></section>
<section class="regional-services"><div class="wrap regional-services-inner"><span class="regional-services-label">Leistungen in dieser Region</span><div class="regional-service-links"><a href="betonpumpendienst.html">Betonpumpendienst</a><a href="frischbetontransporte.html">Frischbetontransporte</a><a href="kiestransporte.html">Kiestransporte</a></div></div></section>
<section class="regional-other"><div class="wrap regional-other-inner"><span class="regional-services-label">Weitere Regionen im Kerngebiet</span><div class="regional-other-links">{other_links}</div></div></section>
</main>'''
    main_match = re.search(r'<main>.*?</main>', page, re.S)
    if not main_match:
        raise SystemExit(f"RN regional SEO current main not found: {region['filename']}")
    page = page[:main_match.start()] + main + page[main_match.end():]

    schema_match = None
    for candidate in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', page, re.S):
        try:
            candidate_data = json.loads(candidate.group(1))
        except Exception:
            continue
        graph = candidate_data.get("@graph") if isinstance(candidate_data, dict) else None
        if isinstance(graph, list) and any(isinstance(node, dict) and node.get("@type") == "Service" for node in graph):
            schema_match = candidate
            break
    if schema_match is None:
        raise SystemExit(f"RN regional SEO service schema anchor missing: {region['filename']}")
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Service",
                "@id": url + "#service",
                "name": "Betonlogistik und Transporte – " + region["name"],
                "serviceType": ["Betonpumpendienst", "Frischbetontransport", "Kies- und Schüttguttransport"],
                "url": url,
                "description": region["description"],
                "provider": {"@id": SITE_URL + "#organization"},
                "areaServed": [{"@type": "City", "name": p} for p in region["places"] if p not in ("Ostwestfalen-Lippe", "Kreis Höxter", "Nordhessen", "Südniedersachsen")]
                    + [{"@type": "AdministrativeArea", "name": p} for p in region["places"] if p in ("Ostwestfalen-Lippe", "Kreis Höxter", "Nordhessen", "Südniedersachsen")],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Startseite", "item": SITE_URL},
                    {"@type": "ListItem", "position": 2, "name": "Leistungen", "item": SITE_URL + "leistungen.html"},
                    {"@type": "ListItem", "position": 3, "name": "Einsatzgebiet " + region["name"], "item": url},
                ],
            },
        ],
    }
    page = page[:schema_match.start()] + jsonld(schema) + page[schema_match.end():]
    page = page.replace("</head>", regional_page_style + "\n</head>", 1)
    Path(region["filename"]).write_text(page, encoding="utf-8")


index_path = Path("index.html")
index_html = index_path.read_text(encoding="utf-8")
index_html = update_org_area_schema(index_html)
index_path.write_text(index_html, encoding="utf-8")


sitemap_path = Path("sitemap.xml")
sitemap = sitemap_path.read_text(encoding="utf-8")
entries = []
for region in REGIONS:
    url = SITE_URL + region["filename"]
    if f'<loc>{url}</loc>' not in sitemap:
        entries.append(f'''  <url>\n    <loc>{url}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.72</priority>\n  </url>''')
if entries:
    if "</urlset>" not in sitemap:
        raise SystemExit("RN regional SEO sitemap closing tag missing")
    sitemap = sitemap.replace("</urlset>", "\n" + "\n".join(entries) + "\n</urlset>", 1)
sitemap_path.write_text(sitemap, encoding="utf-8")


if services_html.count('class="regional-focus-links"') != 1:
    raise SystemExit("RN regional SEO services hub malformed")
for region in REGIONS:
    text = Path(region["filename"]).read_text(encoding="utf-8")
    if region["hero"] not in text or 'id="rn-regional-page"' not in text:
        raise SystemExit(f"RN regional SEO page malformed: {region['filename']}")
    if 'Rund 150 km um Salzkotten' not in text:
        raise SystemExit(f"RN regional SEO radius missing: {region['filename']}")
    if text.count("<main>") != 1 or text.count("</main>") != 1 or "</header>" not in text or "<footer>" not in text:
        raise SystemExit(f"RN regional SEO document structure malformed: {region['filename']}")
