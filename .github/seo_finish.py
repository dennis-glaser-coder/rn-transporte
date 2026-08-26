from pathlib import Path
from datetime import date
import json
import re

SITE_URL = "https://dennis-glaser-coder.github.io/rn-transporte/"
TODAY = date.today().isoformat()


def replace_meta(html: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, html, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"RN SEO {label} not found")
    return updated


def jsonld(data) -> str:
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + '</script>'


# ---------- Improve the main services hub ----------
services_path = Path("leistungen.html")
services_html = services_path.read_text(encoding="utf-8")

services_title = "Betonpumpendienst, Frischbeton- & Kiestransporte | RN Transporte"
services_desc = "Betonpumpendienst, Frischbeton- und Kiestransporte von RN Transporte aus Salzkotten. Zuverlässig für Baustellen und Betonwerke – bundesweit im Einsatz."

services_html = replace_meta(services_html, r'<title>.*?</title>', f'<title>{services_title}</title>', "services title")
services_html = replace_meta(services_html, r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{services_desc}">', "services description")
services_html = replace_meta(services_html, r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{services_title}">', "services OG title")
services_html = replace_meta(services_html, r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{services_desc}">', "services OG description")
services_html = replace_meta(services_html, r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{services_title}">', "services Twitter title")
services_html = replace_meta(services_html, r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{services_desc}">', "services Twitter description")

service_links = (
    (
        '<h2>Betonpumpendienst</h2>\n        <p>Fördern und Einbringen von Beton direkt am Einsatzort.</p>',
        '<h2>Betonpumpendienst</h2>\n        <p>Fördern und Einbringen von Beton direkt am Einsatzort.</p>\n        <a class="service-detail-link" href="betonpumpendienst.html">Betonpumpendienst im Detail →</a>',
    ),
    (
        '<h2>Frischbetontransporte</h2>\n        <p>Frischbetontransporte mit Fahrmischern zwischen Betonwerk und Baustelle.</p>',
        '<h2>Frischbetontransporte</h2>\n        <p>Frischbetontransporte mit Fahrmischern zwischen Betonwerk und Baustelle.</p>\n        <a class="service-detail-link" href="frischbetontransporte.html">Frischbetontransporte im Detail →</a>',
    ),
    (
        '<h2>Kiestransporte</h2>\n        <p>Transport von Kies und Schüttgütern zum jeweiligen Einsatzort.</p>',
        '<h2>Kiestransporte</h2>\n        <p>Transport von Kies und Schüttgütern zum jeweiligen Einsatzort.</p>\n        <a class="service-detail-link" href="kiestransporte.html">Kiestransporte im Detail →</a>',
    ),
)
for old, new in service_links:
    if old not in services_html:
        raise SystemExit("RN SEO services internal-link target not found")
    services_html = services_html.replace(old, new, 1)

hub_style = r'''<style id="rn-seo-service-links">
.service-detail-link{display:inline-flex;align-items:center;margin-top:22px;color:#282b2e;font-size:10px;font-weight:780;letter-spacing:.065em;text-transform:uppercase;border-bottom:1px solid #bfc2c3;padding-bottom:5px;transition:color .2s ease,border-color .2s ease}
@media(hover:hover){.service-detail-link:hover{color:var(--red);border-color:var(--red)}}
@media(max-width:900px){.service-detail-link{margin-top:17px;min-height:44px;align-items:center;padding-bottom:0;border-bottom:0}}
</style>'''
if 'id="rn-seo-service-links"' in services_html:
    raise SystemExit("RN SEO service link style already present")
services_html = services_html.replace("</head>", hub_style + "\n</head>", 1)
services_path.write_text(services_html, encoding="utf-8")


# ---------- Dedicated service landing pages ----------
service_page_style = r'''<style id="rn-seo-service-page">
.seo-service-page{padding:92px 0 104px;background:#fff}
.seo-service-grid{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(380px,.82fr);gap:76px;align-items:center}
.seo-service-media{position:relative;overflow:hidden;background:#ececea;box-shadow:0 24px 58px rgba(22,24,26,.055)}
.seo-service-media:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,transparent 70%,rgba(255,255,255,.12));pointer-events:none}
.seo-service-media img{width:100%;aspect-ratio:16/10;object-fit:cover;filter:saturate(.84) contrast(1.025)}
.seo-service-copy{max-width:620px}
.seo-service-kicker{display:block;margin-bottom:19px;color:#777b7f;font-size:10px;font-weight:780;letter-spacing:.16em;text-transform:uppercase}
.seo-service-copy h2{margin:0;color:#191b1e;font-size:clamp(35px,3.7vw,52px);line-height:.99;letter-spacing:-.052em;font-weight:510;text-wrap:balance}
.seo-service-copy p{margin:20px 0 0;color:#5f6468;font-size:15px;line-height:1.75;max-width:590px}
.seo-service-meta{display:grid;grid-template-columns:1fr 1fr;gap:0;margin-top:32px;padding:21px 0;border-top:1px solid #dedfdf;border-bottom:1px solid #dedfdf}
.seo-service-meta span{color:#666b6f;font-size:12px;line-height:1.45}
.seo-service-meta span+span{padding-left:24px;border-left:1px solid #dedfdf}
.seo-service-meta strong{display:block;margin-bottom:4px;color:#24272a;font-size:9px;letter-spacing:.12em;text-transform:uppercase}
.seo-service-actions{display:flex;align-items:center;gap:12px;margin-top:30px}
.seo-service-actions a{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 18px;font-size:11px;font-weight:760;letter-spacing:.035em;text-transform:uppercase}
.seo-service-actions .seo-primary{background:var(--red);color:#fff}
.seo-service-actions .seo-secondary{border:1px solid #d0d2d2;color:#292c2f;background:#fff}
.seo-related{padding:0 0 100px;background:#fff}
.seo-related-inner{padding-top:34px;border-top:1px solid #d8dada}
.seo-related-label{display:block;margin-bottom:20px;color:#757a7e;font-size:9px;font-weight:780;letter-spacing:.15em;text-transform:uppercase}
.seo-related-links{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid #e0e1e1;border-bottom:1px solid #e0e1e1}
.seo-related-links a{display:flex;align-items:center;justify-content:space-between;gap:18px;min-height:74px;padding:0 20px;color:#24272a;font-size:14px;font-weight:610}
.seo-related-links a+a{border-left:1px solid #e0e1e1}
.seo-related-links a:after{content:"→";color:var(--red);font-size:17px}
@media(hover:hover){.seo-service-actions .seo-primary:hover{background:var(--red-dark)}.seo-service-actions .seo-secondary:hover,.seo-related-links a:hover{background:#f6f6f4}}
@media(max-width:900px){
  .seo-service-page{padding:60px 0 72px}
  .seo-service-grid{grid-template-columns:1fr;gap:38px}
  .seo-service-media{order:1}
  .seo-service-copy{order:2;max-width:none}
  .seo-service-copy h2{font-size:36px}
  .seo-service-copy p{font-size:14px}
  .seo-service-actions a{min-height:48px}
  .seo-related{padding-bottom:70px}
  .seo-related-links{grid-template-columns:1fr}
  .seo-related-links a{min-height:62px;padding:0 4px}
  .seo-related-links a+a{border-left:0;border-top:1px solid #e0e1e1}
}
@media(max-width:430px){
  .seo-service-page{padding-top:50px}
  .seo-service-grid{gap:30px}
  .seo-service-media{margin-left:-16px;margin-right:-16px}
  .seo-service-copy h2{font-size:33px}
  .seo-service-meta{grid-template-columns:1fr;gap:14px}
  .seo-service-meta span+span{padding-left:0;padding-top:14px;border-left:0;border-top:1px solid #e3e4e4}
  .seo-service-actions{display:grid;grid-template-columns:1fr}
  .seo-service-actions a{width:100%}
}
</style>'''

services = [
    {
        "filename": "betonpumpendienst.html",
        "name": "Betonpumpendienst",
        "title": "Betonpumpendienst & Transporte | RN Transporte Salzkotten",
        "description": "Betonpumpendienst von RN Transporte aus Salzkotten: Beton zuverlässig fördern und direkt am Einsatzort einbringen. Bundesweit für Baustellen im Einsatz.",
        "hero": "Betonpumpendienst für Baustellen und Betonwerke.",
        "intro": "Beton zuverlässig fördern und dort einbringen, wo er gebraucht wird – mit direkter Abstimmung am Einsatzort.",
        "image": "assets/leistungen/betonpumpendienst.png",
        "image_alt": "RN Transporte Betonpumpendienst im Baustelleneinsatz",
        "section": "Beton direkt am Einsatzort fördern.",
        "paragraphs": [
            "Mit unseren Betonpumpen fördern wir Beton direkt an den vorgesehenen Einbauort. Entscheidend sind ein sicherer Aufbau, eine klare Abstimmung und ein verlässlicher Ablauf auf der Baustelle.",
            "RN Transporte koordiniert Betonpumpeneinsätze von Salzkotten aus und ist für Kunden deutschlandweit im Einsatz.",
        ],
        "service_type": "Betonpumpendienst",
    },
    {
        "filename": "frischbetontransporte.html",
        "name": "Frischbetontransporte",
        "title": "Frischbetontransporte | RN Transporte Salzkotten",
        "description": "Frischbetontransporte mit Fahrmischern zwischen Betonwerk und Baustelle. RN Transporte aus Salzkotten ist deutschlandweit zuverlässig im Einsatz.",
        "hero": "Frischbetontransporte zwischen Betonwerk und Baustelle.",
        "intro": "Fahrmischer, direkte Abstimmung und verlässliche Transportlogistik für den täglichen Baustelleneinsatz.",
        "image": "assets/leistungen/frischbetontransport.png",
        "image_alt": "RN Transporte Fahrmischer beim Frischbetontransport",
        "section": "Frischbeton zuverlässig ans Ziel bringen.",
        "paragraphs": [
            "Wir transportieren Frischbeton mit Fahrmischern vom Betonwerk zur Baustelle. Dabei stehen abgestimmte Abläufe und eine direkte Kommunikation mit Werk und Einsatzort im Mittelpunkt.",
            "RN Transporte sitzt in Salzkotten und übernimmt Frischbetontransporte deutschlandweit.",
        ],
        "service_type": "Frischbetontransport",
    },
    {
        "filename": "kiestransporte.html",
        "name": "Kiestransporte",
        "title": "Kiestransporte & Schüttgüter | RN Transporte Salzkotten",
        "description": "Kiestransporte und Schüttgüter zuverlässig zum Einsatzort. RN Transporte aus Salzkotten übernimmt Transporte für Baustellen deutschlandweit.",
        "hero": "Kiestransporte und Schüttgüter für Baustellen.",
        "intro": "Baustoffe zuverlässig zum Einsatzort transportieren – passend zum Ablauf auf der Baustelle.",
        "image": "assets/leistungen/Kiestransporte.png",
        "image_alt": "RN Transporte Kiestransport mit Sattelkipper im Einsatz",
        "section": "Kies und Schüttgüter zuverlässig transportieren.",
        "paragraphs": [
            "Mit Sattelkippern transportieren wir Kies, Baustoffe und weitere Schüttgüter zum jeweiligen Einsatzort. Die Transporte stimmen wir passend zum Baustellenablauf ab.",
            "Von unserem Standort in Salzkotten ist RN Transporte deutschlandweit für Kunden im Einsatz.",
        ],
        "service_type": "Kies- und Schüttguttransport",
    },
]

base_template = services_html
main_match = re.search(r'<main>.*?</main>', base_template, re.S)
if not main_match:
    raise SystemExit("RN SEO service template main not found")

for item in services:
    url = SITE_URL + item["filename"]
    image_url = SITE_URL + item["image"]
    related = []
    for other in services:
        if other["filename"] != item["filename"]:
            related.append(f'<a href="{other["filename"]}">{other["name"]}</a>')
    related.append('<a href="leistungen.html">Alle Leistungen</a>')

    paragraphs = ''.join(f'<p>{p}</p>' for p in item["paragraphs"])
    main = f'''<main>
<section class="page-hero"><div class="wrap page-hero-grid"><div class="eyebrow">Leistung</div><div><h1>{item["hero"]}</h1><p>{item["intro"]}</p></div></div></section>
<section class="seo-service-page"><div class="wrap seo-service-grid">
  <div class="seo-service-media"><img src="{item["image"]}" alt="{item["image_alt"]}" decoding="async" fetchpriority="high"></div>
  <div class="seo-service-copy"><span class="seo-service-kicker">RN Transporte · Salzkotten</span><h2>{item["section"]}</h2>{paragraphs}
    <div class="seo-service-meta"><span><strong>Standort</strong>Salzkotten</span><span><strong>Einsatzgebiet</strong>Deutschlandweit</span></div>
    <div class="seo-service-actions"><a class="seo-primary" href="kontakt.html">Projekt anfragen →</a><a class="seo-secondary" href="leistungen.html">Leistungen ansehen</a></div>
  </div>
</div></section>
<section class="seo-related"><div class="wrap seo-related-inner"><span class="seo-related-label">Weitere Leistungen</span><div class="seo-related-links">{''.join(related)}</div></div></section>
</main>'''

    page = re.sub(r'<main>.*?</main>', main, base_template, count=1, flags=re.S)
    page = replace_meta(page, r'<title>.*?</title>', f'<title>{item["title"]}</title>', f'{item["name"]} title')
    page = replace_meta(page, r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{item["description"]}">', f'{item["name"]} description')
    page = replace_meta(page, r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{item["title"]}">', f'{item["name"]} OG title')
    page = replace_meta(page, r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{item["description"]}">', f'{item["name"]} OG description')
    page = replace_meta(page, r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{item["title"]}">', f'{item["name"]} Twitter title')
    page = replace_meta(page, r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{item["description"]}">', f'{item["name"]} Twitter description')
    page = replace_meta(page, r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', f'{item["name"]} canonical')
    page = replace_meta(page, r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', f'{item["name"]} OG URL')
    page = replace_meta(page, r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{image_url}">', f'{item["name"]} OG image')
    page = replace_meta(page, r'<meta property="og:image:alt" content="[^"]*">', f'<meta property="og:image:alt" content="{item["image_alt"]}">', f'{item["name"]} OG image alt')
    page = replace_meta(page, r'<meta name="twitter:image" content="[^"]*">', f'<meta name="twitter:image" content="{image_url}">', f'{item["name"]} Twitter image')

    structured = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Service",
                "@id": url + "#service",
                "name": item["name"],
                "serviceType": item["service_type"],
                "url": url,
                "description": item["description"],
                "provider": {"@id": SITE_URL + "#organization"},
                "areaServed": {"@type": "Country", "name": "Deutschland"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Startseite", "item": SITE_URL},
                    {"@type": "ListItem", "position": 2, "name": "Leistungen", "item": SITE_URL + "leistungen.html"},
                    {"@type": "ListItem", "position": 3, "name": item["name"], "item": url},
                ],
            },
        ],
    }
    page = page.replace("</head>", service_page_style + "\n" + jsonld(structured) + "\n</head>", 1)
    Path(item["filename"]).write_text(page, encoding="utf-8")


# ---------- JobPosting structured data ----------
career_path = Path("karriere.html")
career_html = career_path.read_text(encoding="utf-8")
if 'id="pumpenfahrer"' in career_html or 'id="berufskraftfahrer"' in career_html:
    raise SystemExit("RN SEO career job IDs already present")
career_html = career_html.replace('<article class="job-card">', '<article class="job-card" id="pumpenfahrer">', 1)
career_html = career_html.replace('<article class="job-card">', '<article class="job-card" id="berufskraftfahrer">', 1)

job_org = {
    "@type": "Organization",
    "name": "RN Torwesten Transporte UG (haftungsbeschränkt)",
    "sameAs": SITE_URL,
    "logo": SITE_URL + "assets/logo.webp",
}
job_location = {
    "@type": "Place",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Lohweg 55a",
        "addressLocality": "Salzkotten",
        "postalCode": "33154",
        "addressCountry": "DE",
    },
}
job_data = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "JobPosting",
            "title": "Pumpenfahrer / Betonpumpenmaschinist (m/w/d)",
            "description": "Betonpumpen auf Baustellen bedienen, sicheren Aufbau gewährleisten und den Einsatz vor Ort koordinieren. Technisches Verständnis und zuverlässige Arbeitsweise sind erforderlich; Erfahrung mit Betonpumpen ist ideal. Ganzjährige Beschäftigung und Fortbildungsmöglichkeiten.",
            "datePosted": TODAY,
            "employmentType": "FULL_TIME",
            "hiringOrganization": job_org,
            "jobLocation": job_location,
            "url": SITE_URL + "karriere.html#pumpenfahrer",
        },
        {
            "@type": "JobPosting",
            "title": "Berufskraftfahrer (m/w/d) – Fahrmischer / Kipper / Sattelzug",
            "description": "Beton- und Baustofftransporte mit Fahrmischer, Kipper oder Sattelzug. Erforderlich sind Führerschein CE mit gültiger Schlüsselzahl 95 sowie eine motivierte und verantwortungsbewusste Arbeitsweise. Ganzjährige Beschäftigung und Fortbildungsmöglichkeiten.",
            "datePosted": TODAY,
            "employmentType": "FULL_TIME",
            "hiringOrganization": job_org,
            "jobLocation": job_location,
            "url": SITE_URL + "karriere.html#berufskraftfahrer",
        },
    ],
}
career_html = career_html.replace("</head>", jsonld(job_data) + "\n</head>", 1)
career_path.write_text(career_html, encoding="utf-8")


# ---------- Sitemap ----------
sitemap_path = Path("sitemap.xml")
sitemap = sitemap_path.read_text(encoding="utf-8")
entries = []
for item in services:
    loc = SITE_URL + item["filename"]
    if loc in sitemap:
        raise SystemExit(f"RN SEO sitemap URL already present: {loc}")
    entries.append(f'''  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>\n''')
if "</urlset>" not in sitemap:
    raise SystemExit("RN SEO sitemap closing tag not found")
sitemap = sitemap.replace("</urlset>", ''.join(entries) + "</urlset>", 1)
sitemap_path.write_text(sitemap, encoding="utf-8")


# ---------- Self verification ----------
services_final = services_path.read_text(encoding="utf-8")
if services_final.count('class="service-detail-link"') != 3:
    raise SystemExit("RN SEO service hub links verification failed")
if services_title not in services_final or services_desc not in services_final:
    raise SystemExit("RN SEO services metadata verification failed")

for item in services:
    text = Path(item["filename"]).read_text(encoding="utf-8")
    checks = (
        item["title"],
        item["description"],
        f'href="{SITE_URL + item["filename"]}"',
        '"@type":"Service"',
        '"@type":"BreadcrumbList"',
        'id="rn-seo-service-page"',
        'Projekt anfragen →',
    )
    for check in checks:
        if check not in text:
            raise SystemExit(f"RN SEO verification failed for {item['filename']}: {check}")

career_final = career_path.read_text(encoding="utf-8")
for check in ('id="pumpenfahrer"', 'id="berufskraftfahrer"', '"@type":"JobPosting"', '"employmentType":"FULL_TIME"'):
    if check not in career_final:
        raise SystemExit(f"RN SEO career verification failed: {check}")

sitemap_final = sitemap_path.read_text(encoding="utf-8")
for item in services:
    if SITE_URL + item["filename"] not in sitemap_final:
        raise SystemExit(f"RN SEO sitemap verification failed: {item['filename']}")
