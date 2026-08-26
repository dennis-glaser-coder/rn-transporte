from datetime import date
from pathlib import Path


SITE_URL = "https://dennis-glaser-coder.github.io/rn-transporte/"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"Expected {label} not found")
    return text.replace(old, new, 1)


p = Path("index.html")
s = p.read_text(encoding="utf-8")

company_old = '<h2>RN Transporte</h2><p>Inhabergeführtes Transportunternehmen aus Salzkotten-Niederntudorf mit Schwerpunkt auf Betonlogistik und Baustellentransporten.</p>'
company_new = '<h2>RN Transporte – zuverlässig. leistungsstark. deutschlandweit im Einsatz.</h2><div class="company-copy"><p class="company-lead">Seit 2010 steht RN Transporte aus Salzkotten für zuverlässige Transport- und Betonlogistik. Als inhabergeführtes Unternehmen sind wir kontinuierlich gewachsen und haben uns mit Erfahrung, Flexibilität und persönlichem Einsatz als verlässlicher Partner für unsere Kunden etabliert.</p><p>Unser Leistungsspektrum umfasst den Transport von Frischbeton mit Fahrmischern, Baustofftransporte mit Sattelkippern, Holztransporte sowie das fachgerechte Fördern und Pumpen von Beton mit unseren Betonpumpen.</p><p>Mit einem leistungsfähigen Fuhrpark, erfahrenen Mitarbeitern und kurzen Entscheidungswegen sorgen wir dafür, dass unsere Aufträge zuverlässig, termingerecht und professionell umgesetzt werden. Dabei legen wir besonderen Wert auf persönliche Betreuung, hohe Einsatzbereitschaft und flexible Lösungen.</p><p class="company-closing">Heute sind wir <strong>deutschlandweit</strong> für unsere Kunden im Einsatz und stehen für eine partnerschaftliche Zusammenarbeit, auf die man sich verlassen kann – vom einzelnen Transportauftrag bis hin zu umfangreichen Projekten.</p></div>'

seo_head = '''
<link rel="canonical" href="__SITE_URL__">
<link rel="preload" as="image" href="rn_hero_final.png" fetchpriority="high">
<meta property="og:url" content="__SITE_URL__">
<meta property="og:image" content="__SITE_URL__rn_hero_final.png">
<meta property="og:image:alt" content="RN Transporte im Betonpumpen- und Baustelleneinsatz">
<meta name="twitter:image" content="__SITE_URL__rn_hero_final.png">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": ["LocalBusiness", "Organization"],
  "@id": "__SITE_URL__#organization",
  "name": "RN Transporte",
  "legalName": "RN Torwesten Transporte UG (haftungsbeschränkt)",
  "url": "__SITE_URL__",
  "logo": "__SITE_URL__assets/logo.webp",
  "image": "__SITE_URL__rn_hero_final.png",
  "description": "Betonpumpendienst, Frischbeton-, Baustoff-, Kies- und Holztransporte aus Salzkotten. Bundesweit im Einsatz.",
  "foundingDate": "2010",
  "telephone": "+49 173 72 75 165",
  "email": "ntorwesten@web.de",
  "vatID": "DE270004353",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Lohweg 55a",
    "postalCode": "33154",
    "addressLocality": "Salzkotten",
    "addressCountry": "DE"
  },
  "areaServed": {
    "@type": "Country",
    "name": "Deutschland"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+49 173 72 75 165",
    "contactType": "customer service",
    "availableLanguage": "de"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Leistungen",
    "itemListElement": [
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Betonpumpendienst"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Frischbetontransporte"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Kies- und Baustofftransporte"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Holztransporte"}}
    ]
  }
}
</script>
'''.replace("__SITE_URL__", SITE_URL)

replacements = [
    ('<title>RN Torwesten Transporte | Betonlogistik & Transporte</title>', '<title>Betonpumpendienst & Transporte | RN Transporte Salzkotten</title>', 'SEO title'),
    ('<meta name="description" content="RN Torwesten Transporte aus Salzkotten-Niederntudorf: Betonpumpendienst, Frischbetontransporte und Kiestransporte. Deutschlandweit im Einsatz.">', '<meta name="description" content="RN Transporte aus Salzkotten: Betonpumpendienst, Frischbeton-, Baustoff-, Kies- und Holztransporte. Bundesweit im Einsatz – jetzt Projekt anfragen.">', 'SEO description'),
    ('<meta property="og:title" content="RN Torwesten Transporte">', '<meta property="og:title" content="Betonpumpendienst & Transporte | RN Transporte">', 'Open Graph title'),
    ('<meta property="og:description" content="Betonpumpendienst, Frischbetontransporte und Kiestransporte aus Salzkotten-Niederntudorf. Deutschlandweit im Einsatz.">', '<meta property="og:description" content="Betonpumpendienst, Frischbeton-, Baustoff-, Kies- und Holztransporte aus Salzkotten. Bundesweit im Einsatz.">', 'Open Graph description'),
    ('<meta name="twitter:card" content="summary">', '<meta name="twitter:card" content="summary_large_image">', 'Twitter card'),
    ('<meta name="twitter:title" content="RN Torwesten Transporte">', '<meta name="twitter:title" content="Betonpumpendienst & Transporte | RN Transporte">', 'Twitter title'),
    ('<meta name="twitter:description" content="Betonpumpendienst, Frischbetontransporte und Kiestransporte aus Salzkotten-Niederntudorf. Deutschlandweit im Einsatz.">', '<meta name="twitter:description" content="Betonpumpendienst, Frischbeton-, Baustoff-, Kies- und Holztransporte aus Salzkotten. Bundesweit im Einsatz.">', 'Twitter description'),
    ('<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">', '<link rel="icon" href="assets/favicon.svg?v=rn-brand-2" type="image/svg+xml">', 'favicon cache bust'),
    ('</head>', seo_head + '<link rel="stylesheet" href="assets/premium.css">\n</head>', 'premium stylesheet and SEO hook'),
    ('src="assets/logo.svg"', 'src="assets/logo.webp"', 'real logo image'),
    ('<a class="phone" href="tel:+491737275165">0173 72 75 165</a>', '<a class="header-cta" href="#kontakt">Projekt anfragen</a>', 'header phone replacement'),
    ('<div class="hero-place">Salzkotten-Niederntudorf</div>', '<div class="hero-place">Salzkotten · bundesweit im Einsatz</div>', 'hero location'),
    ('<h1 class="hero-title">Betonpumpendienst, Frischbetontransporte und Kiestransporte.</h1>', '<h1 class="hero-title">Betonlogistik und Transport. Zuverlässig im Einsatz.</h1><p class="hero-sub">Betonpumpendienst, Frischbeton- und Kiestransporte für Baustellen und Betonwerke.</p><div class="hero-cta-row"><a class="hero-cta" href="#kontakt">Projekt anfragen</a></div>', 'premium hero copy'),
    (company_old, company_new, 'company copy'),
    ('<strong>Karriere bei RN</strong>', '<strong>Karriere bei RN Transporte</strong>', 'career title'),
    ('<div class="job-facts"><span>Fahrmischer</span><span>Kipper</span><span>Sattelzug</span></div>', '<div class="job-facts"><span>Fahrmischer</span><span>Kipper</span><span>Sattelzug</span><span>C/CE</span></div>', 'driver licence fact'),
    ('<div class="job-kicker">Stelle 01</div>', '', 'career label 01'),
    ('<div class="job-kicker">Stelle 02</div>', '', 'career label 02'),
    ('<h2>Einsatz besprechen.</h2>', '<h2>Projekt oder Einsatz anfragen.</h2><p class="contact-copy">Betonpumpendienst oder Transportbedarf? Rufen Sie direkt an oder senden Sie uns Ihre Anfrage per WhatsApp.</p>', 'premium contact copy'),
]

for old, new, label in replacements:
    s = replace_once(s, old, new, label)

checks = {
    "final hero": 'src="rn_hero_final.png"' in s,
    "real logo": 'src="assets/logo.webp"' in s,
    "premium stylesheet": 'href="assets/premium.css"' in s,
    "favicon cache bust": 'assets/favicon.svg?v=rn-brand-2' in s,
    "canonical": f'<link rel="canonical" href="{SITE_URL}">' in s,
    "structured data": 'application/ld+json' in s and 'RN Torwesten Transporte UG (haftungsbeschränkt)' in s,
    "social image": f'<meta property="og:image" content="{SITE_URL}rn_hero_final.png">' in s,
    "company": 'Seit 2010 steht RN Transporte' in s and 'Holztransporte' in s,
    "company editorial layout": 'class="company-lead"' in s and 'class="company-closing"' in s,
    "career": 'Karriere bei RN Transporte' in s,
    "driver licence": '<span>C/CE</span>' in s,
    "contact": 'Projekt oder Einsatz anfragen.' in s,
    "hero location": 'Salzkotten · bundesweit im Einsatz' in s,
    "header phone removed": 'class="phone"' not in s,
    "header project CTA": '<a class="header-cta" href="#kontakt">Projekt anfragen</a>' in s,
    "job labels removed": 'Stelle 01' not in s and 'Stelle 02' not in s,
}
for label, ok in checks.items():
    if not ok:
        raise SystemExit(f"RN check failed: {label}")

p.write_text(s, encoding="utf-8")

css_path = Path("assets/premium.css")
css = css_path.read_text(encoding="utf-8")
css += '''

/* RN refinement: clean premium hierarchy */
@media(min-width:1161px){.head{grid-template-columns:250px 1fr auto}}
.service:before{display:none!important;content:none!important}
.service h2{margin-top:0!important}
.company-main{max-width:980px}
.company-main h2{max-width:900px}
.company-copy{margin-top:34px;padding-top:30px;border-top:1px solid #d6d8d9;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:56px;row-gap:22px;max-width:920px}
.company-copy p{margin:0;color:#5e6266;font-size:15px;line-height:1.74}
.company-copy .company-lead{grid-column:1/-1;max-width:790px;color:#2f3337;font-size:18px;line-height:1.62;letter-spacing:-.012em}
.company-copy .company-closing{grid-column:1/-1;margin-top:4px;padding-top:22px;border-top:1px solid #d6d8d9;max-width:840px}
.company-copy strong{color:var(--ink);font-weight:680}
.company-meta{margin-top:38px}
@media(max-width:900px){.service h2{margin-top:0!important}.company-main{max-width:none}.company-main h2{max-width:none}.company-copy{margin-top:24px;padding-top:23px;grid-template-columns:1fr;gap:16px;max-width:none}.company-copy .company-lead,.company-copy .company-closing{grid-column:auto;max-width:none}.company-copy .company-lead{font-size:17px;line-height:1.6}.company-copy .company-closing{margin-top:2px;padding-top:18px}.company-copy p{font-size:15px;line-height:1.68}.company-meta{margin-top:28px}}
'''
css_path.write_text(css, encoding="utf-8")

legal_urls = {
    "impressum.html": f"{SITE_URL}impressum.html",
    "datenschutz.html": f"{SITE_URL}datenschutz.html",
}

for legal_name, legal_url in legal_urls.items():
    lp = Path(legal_name)
    legal = lp.read_text(encoding="utf-8")
    legal = replace_once(legal, '<meta name="robots" content="index,follow">', f'<meta name="robots" content="noindex,follow"><link rel="canonical" href="{legal_url}">', f'{legal_name} indexing rule')
    legal = replace_once(legal, '<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">', '<link rel="icon" href="assets/favicon.svg?v=rn-brand-2" type="image/svg+xml">', f'{legal_name} favicon cache bust')
    legal = replace_once(legal, 'src="assets/logo.svg"', 'src="assets/logo.webp"', f'{legal_name} real logo')
    legal = legal.replace('.logo{width:228px}', '.logo{width:228px;height:auto;object-fit:contain}', 1)
    legal = legal.replace('.logo{width:200px}', '.logo{width:200px;height:auto;object-fit:contain}', 1)
    if 'noindex,follow' not in legal or f'rel="canonical" href="{legal_url}"' not in legal or 'assets/favicon.svg?v=rn-brand-2' not in legal:
        raise SystemExit(f"RN legal SEO check failed: {legal_name}")
    lp.write_text(legal, encoding="utf-8")

Path("robots.txt").write_text(
    f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n",
    encoding="utf-8",
)

lastmod = date.today().isoformat()
Path("sitemap.xml").write_text(
    f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{SITE_URL}</loc>
    <lastmod>{lastmod}</lastmod>
  </url>
</urlset>
''',
    encoding="utf-8",
)
