from datetime import date
from pathlib import Path
import re

SITE_URL = "https://dennis-glaser-coder.github.io/rn-transporte/"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"Expected {label} not found")
    return text.replace(old, new, 1)


def extract(pattern: str, text: str, label: str) -> str:
    match = re.search(pattern, text, re.S)
    if not match:
        raise SystemExit(f"Expected {label} not found")
    return match.group(0)


source = Path("index.html").read_text(encoding="utf-8")
s = source

company_old = '<h2>RN Transporte</h2><p>Inhabergeführtes Transportunternehmen aus Salzkotten-Niederntudorf mit Schwerpunkt auf Betonlogistik und Baustellentransporten.</p>'
company_new = '<h2>RN Transporte – zuverlässig. leistungsstark. deutschlandweit im Einsatz.</h2><div class="company-copy"><p class="company-lead">Seit 2010 steht RN Transporte aus Salzkotten für zuverlässige Transport- und Betonlogistik. Als inhabergeführtes Unternehmen sind wir kontinuierlich gewachsen und haben uns mit Erfahrung, Flexibilität und persönlichem Einsatz als verlässlicher Partner für unsere Kunden etabliert.</p><p>Unser Leistungsspektrum umfasst den Transport von Frischbeton mit Fahrmischern, Baustofftransporte mit Sattelkippern, Holztransporte sowie das fachgerechte Fördern und Pumpen von Beton mit unseren Betonpumpen.</p><p>Mit einem leistungsfähigen Fuhrpark, erfahrenen Mitarbeitern und kurzen Entscheidungswegen sorgen wir dafür, dass unsere Aufträge zuverlässig, termingerecht und professionell umgesetzt werden. Dabei legen wir besonderen Wert auf persönliche Betreuung, hohe Einsatzbereitschaft und flexible Lösungen.</p><p class="company-closing">Heute sind wir <strong>deutschlandweit</strong> für unsere Kunden im Einsatz und stehen für eine partnerschaftliche Zusammenarbeit, auf die man sich verlassen kann – vom einzelnen Transportauftrag bis hin zu umfangreichen Projekten.</p></div>'

seo_head = '''
<link rel="preload" as="image" href="rn_hero_final.png" fetchpriority="high">
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
  "areaServed": {"@type": "Country", "name": "Deutschland"},
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
    ('<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">', '<link rel="icon" href="assets/favicon-rn.svg" type="image/svg+xml">', 'favicon'),
    ('</head>', seo_head + '<link rel="stylesheet" href="assets/premium.css">\n</head>', 'premium stylesheet and SEO hook'),
    ('src="assets/logo.svg"', 'src="assets/logo.webp"', 'real logo image'),
    ('<div class="hero-place">Salzkotten-Niederntudorf</div>', '<div class="hero-place">Salzkotten · bundesweit im Einsatz</div>', 'hero location'),
    ('<h1 class="hero-title">Betonpumpendienst, Frischbetontransporte und Kiestransporte.</h1>', '<h1 class="hero-title">Betonlogistik und Transport. Zuverlässig im Einsatz.</h1><p class="hero-sub">Betonpumpendienst, Frischbeton- und Kiestransporte für Baustellen und Betonwerke.</p><div class="hero-cta-row"><a class="hero-cta" href="kontakt.html">Projekt anfragen</a></div>', 'premium hero copy'),
    (company_old, company_new, 'company copy'),
]
for old, new, label in replacements:
    s = replace_once(s, old, new, label)

base_head = extract(r'<head>.*?</head>', s, 'head')
hero = extract(r'<section class="hero" id="start">.*?</section>', s, 'hero')
base_head = re.sub(r'\n?<link rel="canonical" href="[^"]+">', '', base_head)
base_head = re.sub(r'\n?<meta property="og:url" content="[^"]+">', '', base_head)

NAV_ITEMS = [
    ("index.html", "Startseite", "start"),
    ("leistungen.html", "Leistungen", "leistungen"),
    ("unternehmen.html", "Unternehmen", "unternehmen"),
    ("karriere.html", "Karriere", "karriere"),
    ("kontakt.html", "Kontakt", "kontakt"),
]


def header(active: str) -> str:
    links = []
    for href, label, key in NAV_ITEMS:
        current = ' class="active" aria-current="page"' if key == active else ''
        links.append(f'<a href="{href}"{current}>{label}</a>')
    links.append('<a class="mobile-project-link" href="kontakt.html">Projekt anfragen</a>')
    return (
        '<header id="header"><div class="wrap head">'
        '<a class="brand-link" href="index.html" aria-label="RN Torwesten Transporte Startseite">'
        '<img class="logo" src="assets/logo.webp" alt="RN Torwesten Transporte"></a>'
        f'<nav class="nav" id="main-nav" aria-label="Hauptnavigation">{"".join(links)}</nav>'
        '<a class="header-cta" href="kontakt.html">Projekt anfragen</a>'
        '<button class="menu" id="menu" type="button" aria-label="Menü öffnen" aria-controls="main-nav" aria-expanded="false">'
        '<span class="menu-word">MENÜ</span><span class="menu-bars" aria-hidden="true"><i></i><i></i><i></i></span>'
        '</button></div></header>'
    )


def footer() -> str:
    return (
        '<footer><div class="wrap foot"><span>RN Torwesten Transporte · Salzkotten</span>'
        '<div class="foot-links"><a href="karriere.html">Karriere</a><a href="impressum.html">Impressum</a>'
        '<a href="datenschutz.html">Datenschutz</a></div></div></footer>'
    )


MENU_SCRIPT = '''<script>
const h=document.getElementById('header');
const m=document.getElementById('menu');
const nav=document.getElementById('main-nav');
const closeMenu=()=>{h.classList.remove('open');document.body.classList.remove('menu-open');m.setAttribute('aria-expanded','false');m.setAttribute('aria-label','Menü öffnen');};
m.addEventListener('click',()=>{const open=h.classList.toggle('open');document.body.classList.toggle('menu-open',open);m.setAttribute('aria-expanded',String(open));m.setAttribute('aria-label',open?'Menü schließen':'Menü öffnen');});
nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeMenu();});
window.addEventListener('resize',()=>{if(window.innerWidth>900)closeMenu();});
</script>'''


def page_head(filename: str, title: str, description: str) -> str:
    h = base_head
    h = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', h, count=1, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{description}">', h, count=1)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{description}">', h, count=1)
    h = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{title}">', h, count=1)
    h = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{description}">', h, count=1)
    url = SITE_URL if filename == "index.html" else SITE_URL + filename
    h = h.replace('</head>', f'<link rel="canonical" href="{url}">\n<meta property="og:url" content="{url}">\n</head>')
    return h


def page(filename: str, active: str, title: str, description: str, main: str, body_class: str = "") -> str:
    body_attr = f' class="{body_class}"' if body_class else ''
    return (
        '<!doctype html>\n<html lang="de">\n'
        + page_head(filename, title, description)
        + f'\n<body{body_attr}>\n'
        + header(active)
        + '\n<main>\n'
        + main
        + '\n</main>\n'
        + footer()
        + '\n'
        + MENU_SCRIPT
        + '\n</body>\n</html>\n'
    )


def page_intro(eyebrow: str, heading: str, text: str) -> str:
    return (
        '<section class="page-hero"><div class="wrap page-hero-grid">'
        f'<div class="eyebrow">{eyebrow}</div><div><h1>{heading}</h1><p>{text}</p></div>'
        '</div></section>'
    )


home_links = '''
<section class="home-overview" aria-label="Bereiche der Website"><div class="wrap">
  <div class="home-overview-head"><div class="eyebrow">RN Transporte</div><h2>Direkt zum passenden Bereich.</h2></div>
  <div class="home-link-grid">
    <a class="home-link-card" href="leistungen.html"><span>01</span><h3>Leistungen</h3><p>Betonpumpendienst, Frischbeton- und Kiestransporte.</p><b>Leistungen ansehen →</b></a>
    <a class="home-link-card" href="unternehmen.html"><span>02</span><h3>Unternehmen</h3><p>Erfahrung, Fuhrpark und zuverlässige Transportlogistik seit 2010.</p><b>Unternehmen ansehen →</b></a>
    <a class="home-link-card" href="karriere.html"><span>03</span><h3>Karriere</h3><p>Offene Stellen für Pumpenfahrer und Berufskraftfahrer.</p><b>Zu den Stellen →</b></a>
    <a class="home-link-card home-link-card-dark" href="kontakt.html"><span>04</span><h3>Kontakt</h3><p>Projekt, Einsatz oder Transportbedarf direkt mit RN besprechen.</p><b>Kontakt aufnehmen →</b></a>
  </div>
</div></section>
'''

services_main = page_intro(
    "Leistungen",
    "Betonlogistik und Transporte für den täglichen Einsatz.",
    "Zuverlässige Leistungen für Baustellen und Betonwerke – klar organisiert und flexibel im Einsatz.",
) + '''
<section class="services page-services"><div class="wrap"><div class="service-grid">
  <article class="service"><h2>Betonpumpendienst</h2><p>Fördern und Einbringen von Beton direkt am Einsatzort.</p></article>
  <article class="service"><h2>Frischbetontransporte</h2><p>Frischbetontransporte mit Fahrmischern zwischen Betonwerk und Baustelle.</p></article>
  <article class="service"><h2>Kiestransporte</h2><p>Transport von Kies und Schüttgütern zum jeweiligen Einsatzort.</p></article>
</div><div class="page-cta"><p>Sie möchten einen Einsatz oder Transport abstimmen?</p><a href="kontakt.html">Projekt anfragen →</a></div></div></section>
'''

company_main = page_intro(
    "Unternehmen",
    "Seit 2010 zuverlässig im Einsatz.",
    "RN Transporte aus Salzkotten steht für persönliche Betreuung, kurze Entscheidungswege und professionelle Umsetzung.",
) + f'''
<section class="company company-page"><div class="wrap company-grid"><div class="eyebrow">RN Transporte</div><div class="company-main">{company_new}<div class="company-meta"><span><strong>Standort</strong> Salzkotten</span><span><strong>Einsatzgebiet</strong> Deutschlandweit</span></div></div></div></section>
'''

career_main = page_intro(
    "Karriere",
    "Mit RN unterwegs.",
    "Wir suchen motivierte Verstärkung für unseren Fuhrpark – mit kurzen Wegen und einem familiären Arbeitsumfeld.",
) + '''
<section class="career-page"><div class="wrap"><div class="career career-standalone" id="karriere">
  <div class="career-head"><div class="career-copy"><strong>Karriere bei RN Transporte</strong>Wir suchen motivierte Verstärkung für unseren Fuhrpark. Kurze Wege, ein familiäres Umfeld und ein Chef, der selbst täglich im Einsatz ist.</div><div class="career-note">Vollzeit · unbefristet</div></div>
  <div class="job-grid">
    <article class="job-card"><h3>Pumpenfahrer / Betonpumpenmaschinist (m/w/d)</h3><p>Du bedienst unsere Betonpumpen auf Baustellen, sorgst für einen sicheren Aufbau und koordinierst den Einsatz direkt vor Ort.</p><div class="job-facts"><span>Betonpumpen</span><span>Baustelleneinsatz</span><span>C/CE</span></div><ul><li>Technisches Verständnis und zuverlässige Arbeitsweise</li><li>Erfahrung mit Betonpumpen ist ideal; Einarbeitung nach Absprache</li><li>Ganzjährige Beschäftigung und Fortbildungsmöglichkeiten</li></ul><a class="job-apply" href="https://wa.me/491737275165?text=Hallo%20RN%20Torwesten%20Transporte%2C%20ich%20interessiere%20mich%20f%C3%BCr%20die%20Stelle%20als%20Pumpenfahrer%20%2F%20Betonpumpenmaschinist." target="_blank" rel="noopener"><span>Direkt per WhatsApp bewerben</span><span>→</span></a></article>
    <article class="job-card"><h3>Berufskraftfahrer (m/w/d) – Fahrmischer / Kipper / Sattelzug</h3><p>Du übernimmst Beton- und Baustofftransporte, hältst dein Fahrzeug im Blick und stimmst dich bei den Einsätzen direkt mit dem Team ab.</p><div class="job-facts"><span>Fahrmischer</span><span>Kipper</span><span>Sattelzug</span><span>C/CE</span></div><ul><li>Führerschein CE mit gültiger Schlüsselzahl 95</li><li>Motivierte und verantwortungsbewusste Arbeitsweise</li><li>Ganzjährige Beschäftigung und Fortbildungsmöglichkeiten</li></ul><a class="job-apply" href="https://wa.me/491737275165?text=Hallo%20RN%20Torwesten%20Transporte%2C%20ich%20interessiere%20mich%20f%C3%BCr%20die%20Stelle%20als%20Berufskraftfahrer." target="_blank" rel="noopener"><span>Direkt per WhatsApp bewerben</span><span>→</span></a></article>
  </div>
  <div class="career-benefits"><span><strong>Familiär</strong> und inhabergeführt</span><span><strong>Ganzjährig</strong> beschäftigt</span><span><strong>Faire Vergütung</strong> über dem Durchschnitt</span><span><strong>Fortbildung</strong> möglich</span></div>
</div></div></section>
'''

contact_main = page_intro(
    "Kontakt",
    "Projekt oder Einsatz anfragen.",
    "Betonpumpendienst oder Transportbedarf? Rufen Sie direkt an oder senden Sie Ihre Anfrage per WhatsApp.",
) + '''
<section class="contact contact-page"><div class="wrap contact-grid"><div class="eyebrow">Direkter Kontakt</div><div class="contact-main"><h2>Wir sprechen über Ihren Einsatz.</h2><p class="contact-copy">Kurze Wege und direkte Abstimmung: RN Transporte erreichen Sie telefonisch oder per WhatsApp.</p><a class="contact-number" href="tel:+491737275165">0173 72 75 165</a><div class="contact-links"><a href="tel:+491737275165">Anrufen</a><a class="contact-whatsapp" href="https://wa.me/491737275165?text=Hallo%20RN%20Torwesten%20Transporte%2C%20ich%20habe%20eine%20Anfrage." target="_blank" rel="noopener">WhatsApp →</a></div><div class="contact-address"><strong>RN Torwesten Transporte UG (haftungsbeschränkt)</strong><span>Lohweg 55a · 33154 Salzkotten</span></div></div></div></section>
'''

hero = hero.replace('href="#kontakt"', 'href="kontakt.html"')

pages = {
    "index.html": page(
        "index.html", "start", "Betonpumpendienst & Transporte | RN Transporte Salzkotten",
        "RN Transporte aus Salzkotten: Betonpumpendienst, Frischbeton- und Kiestransporte. Bundesweit im Einsatz.",
        hero + home_links, "home-page",
    ),
    "leistungen.html": page(
        "leistungen.html", "leistungen", "Leistungen | RN Transporte Salzkotten",
        "Betonpumpendienst, Frischbetontransporte und Kiestransporte von RN Transporte aus Salzkotten.",
        services_main,
    ),
    "unternehmen.html": page(
        "unternehmen.html", "unternehmen", "Unternehmen | RN Transporte Salzkotten",
        "RN Transporte aus Salzkotten: inhabergeführt, seit 2010 im Bereich Transport- und Betonlogistik tätig.",
        company_main,
    ),
    "karriere.html": page(
        "karriere.html", "karriere", "Karriere | RN Transporte Salzkotten",
        "Karriere bei RN Transporte: Stellen für Pumpenfahrer, Betonpumpenmaschinisten und Berufskraftfahrer.",
        career_main,
    ),
    "kontakt.html": page(
        "kontakt.html", "kontakt", "Kontakt | RN Transporte Salzkotten",
        "Kontakt zu RN Transporte in Salzkotten für Betonpumpendienst und Transportanfragen.",
        contact_main,
    ),
}

for filename, html in pages.items():
    Path(filename).write_text(html, encoding="utf-8")

css_path = Path("assets/premium.css")
css = css_path.read_text(encoding="utf-8")
css += '''

/* RN refinement: clean premium hierarchy */
@media(min-width:1161px){.head{grid-template-columns:250px 1fr auto}}
.service:before{display:none!important;content:none!important}.service h2{margin-top:0!important}
.company-main{max-width:980px}.company-main h2{max-width:900px}
.company-copy{margin-top:34px;padding-top:30px;border-top:1px solid #d6d8d9;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:56px;row-gap:22px;max-width:920px}
.company-copy p{margin:0;color:#5e6266;font-size:15px;line-height:1.74}.company-copy .company-lead{grid-column:1/-1;max-width:790px;color:#2f3337;font-size:18px;line-height:1.62;letter-spacing:-.012em}.company-copy .company-closing{grid-column:1/-1;margin-top:4px;padding-top:22px;border-top:1px solid #d6d8d9;max-width:840px}.company-copy strong{color:var(--ink);font-weight:680}.company-meta{margin-top:38px}

/* Multi-page navigation */
.brand-link{display:flex;align-items:center}.nav a.active{color:var(--ink)}.nav a.active:after{right:0}.mobile-project-link{display:none!important}
.menu{align-items:center;justify-content:flex-end;gap:9px;width:auto!important;height:44px!important;padding:6px 0 6px 10px!important;color:var(--ink)}.menu-word{height:auto!important;margin:0!important;background:none!important;font-size:11px;font-weight:780;letter-spacing:.11em;line-height:1!important}.menu-bars{width:22px;height:18px!important;margin:0!important;background:none!important;display:flex!important;flex-direction:column;justify-content:space-between}.menu-bars i{display:block;width:22px;height:2px;background:var(--ink);transition:transform .22s ease,opacity .18s ease;transform-origin:center}.menu span{background:none}.menu i{margin:0}.menu-word:after{display:none}
header.open .menu-bars i:nth-child(1){transform:translateY(8px) rotate(45deg)}header.open .menu-bars i:nth-child(2){opacity:0}header.open .menu-bars i:nth-child(3){transform:translateY(-8px) rotate(-45deg)}

/* Homepage overview */
.home-overview{padding:100px 0 108px;background:#fff}.home-overview-head{display:grid;grid-template-columns:.48fr 1.52fr;gap:76px;align-items:start;margin-bottom:48px}.home-overview-head h2{margin:0;color:var(--ink);font-size:clamp(32px,3.5vw,49px);line-height:1.06;letter-spacing:-.045em;font-weight:520}.home-link-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));border-top:1px solid #dedfe0;border-left:1px solid #dedfe0}.home-link-card{min-height:280px;padding:30px 32px;display:flex;flex-direction:column;border-right:1px solid #dedfe0;border-bottom:1px solid #dedfe0;transition:background .2s ease}.home-link-card>span{font-size:10px;letter-spacing:.16em;color:#999da1;font-weight:750}.home-link-card h3{margin:48px 0 0;color:var(--ink);font-size:30px;letter-spacing:-.035em;font-weight:560}.home-link-card p{margin:12px 0 0;color:#707479;font-size:14px;line-height:1.65;max-width:440px}.home-link-card b{margin-top:auto;padding-top:30px;color:var(--red);font-size:12px}.home-link-card-dark{background:var(--dark);color:#fff}.home-link-card-dark h3{color:#fff}.home-link-card-dark p{color:#aeb1b4}.home-link-card-dark>span{color:#767b80}

/* Dedicated page headers */
.page-hero{padding:92px 0 82px;background:#fff;border-bottom:1px solid #e0e1e2}.page-hero-grid{display:grid;grid-template-columns:.48fr 1.52fr;gap:76px;align-items:start}.page-hero h1{margin:0;color:var(--ink);font-size:clamp(42px,5.2vw,72px);line-height:.99;letter-spacing:-.055em;font-weight:510;max-width:900px}.page-hero p{margin:22px 0 0;max-width:660px;color:#696d72;font-size:16px;line-height:1.7}.page-services{padding-top:82px}.page-cta{margin-top:48px;padding-top:28px;border-top:1px solid #dddfe0;display:flex;justify-content:space-between;align-items:center;gap:24px}.page-cta p{margin:0;color:#65696d}.page-cta a{color:var(--red);font-size:13px;font-weight:740}.company-page{padding-top:84px}.career-page{padding:78px 0 98px;background:var(--soft)}.career-standalone{margin:0;padding-top:0;border-top:0}.contact-page{margin-top:0}.contact-address{display:grid;gap:5px;margin-top:38px;padding-top:24px;border-top:1px solid rgba(255,255,255,.13);color:#aeb1b4;font-size:13px}.contact-address strong{color:#fff;font-size:12px}.contact-whatsapp{color:#fff;font-size:13px;font-weight:700}

@media(hover:hover){.home-link-card:hover{background:#fafafa}.home-link-card-dark:hover{background:#222529}.page-cta a:hover,.contact-whatsapp:hover{opacity:.7}}
@media(min-width:901px) and (max-width:1160px){.head{grid-template-columns:200px 1fr auto!important;gap:18px}.logo{width:185px!important}.nav{gap:17px!important;font-size:11px!important}.header-cta{padding:0 13px}.home-overview-head,.page-hero-grid{grid-template-columns:.38fr 1.62fr;gap:48px}}
@media(max-width:900px){body.menu-open{overflow:hidden}.head{grid-template-columns:1fr auto!important}.menu{display:flex!important}.header-cta{display:none!important}.nav{display:none!important}.nav a:after{display:none!important}header.open .nav{display:flex!important;position:fixed!important;top:74px!important;left:0!important;right:0!important;bottom:0!important;z-index:60!important;flex-direction:column!important;justify-content:flex-start!important;gap:0!important;padding:26px 24px calc(28px + env(safe-area-inset-bottom))!important;background:#fff!important;border-top:1px solid #ededed!important;box-shadow:none!important;overflow-y:auto}.nav a{display:block!important;padding:18px 0!important;border-bottom:1px solid #ededed!important;color:var(--ink)!important;font-size:22px!important;line-height:1.2!important;font-weight:570!important;letter-spacing:-.025em!important}.nav a.active{color:var(--red)!important}.nav .mobile-project-link{display:flex!important;align-items:center!important;justify-content:space-between!important;margin-top:24px!important;padding:17px 18px!important;border:0!important;background:var(--red)!important;color:#fff!important;font-size:14px!important;font-weight:760!important;letter-spacing:0!important}.nav .mobile-project-link:after{content:"→";font-size:18px}.menu-word{display:block!important}.home-overview{padding:68px 0 74px}.home-overview-head,.page-hero-grid{grid-template-columns:1fr;gap:18px}.home-overview-head{margin-bottom:32px}.home-overview-head h2{font-size:34px}.home-link-grid{grid-template-columns:1fr}.home-link-card{min-height:220px;padding:25px 24px}.home-link-card h3{margin-top:32px;font-size:27px}.page-hero{padding:58px 0 54px}.page-hero h1{font-size:43px}.page-hero p{font-size:15px;margin-top:17px}.page-services{padding-top:55px}.page-cta{align-items:flex-start;flex-direction:column}.company-page{padding-top:58px}.career-page{padding:54px 0 72px}.company-copy{margin-top:24px;padding-top:23px;grid-template-columns:1fr;gap:16px;max-width:none}.company-copy .company-lead,.company-copy .company-closing{grid-column:auto;max-width:none}.company-copy .company-lead{font-size:17px;line-height:1.6}.company-copy .company-closing{margin-top:2px;padding-top:18px}.company-copy p{font-size:15px;line-height:1.68}.company-meta{margin-top:28px}}
@media(max-width:390px){.menu-word{font-size:10px!important}.page-hero h1{font-size:39px}.home-overview-head h2{font-size:31px}}
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
    legal = replace_once(legal, '<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">', '<link rel="icon" href="assets/favicon-rn.svg" type="image/svg+xml">', f'{legal_name} favicon')
    legal = replace_once(legal, 'src="assets/logo.svg"', 'src="assets/logo.webp"', f'{legal_name} real logo')
    legal = legal.replace('.logo{width:228px}', '.logo{width:228px;height:auto;object-fit:contain}', 1)
    legal = legal.replace('.logo{width:200px}', '.logo{width:200px;height:auto;object-fit:contain}', 1)
    if 'noindex,follow' not in legal or f'rel="canonical" href="{legal_url}"' not in legal or 'assets/favicon-rn.svg' not in legal:
        raise SystemExit(f"RN legal check failed: {legal_name}")
    lp.write_text(legal, encoding="utf-8")

Path("robots.txt").write_text(
    f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n",
    encoding="utf-8",
)

lastmod = date.today().isoformat()
urls = [SITE_URL] + [SITE_URL + name for name in ("leistungen.html", "unternehmen.html", "karriere.html", "kontakt.html")]
entries = "\n".join(f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{lastmod}</lastmod>\n  </url>" for url in urls)
Path("sitemap.xml").write_text(
    f'''<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}\n</urlset>\n''',
    encoding="utf-8",
)

checks = {
    "home hero": 'src="rn_hero_final.png"' in pages["index.html"],
    "mobile menu label": '>MENÜ<' in pages["index.html"],
    "desktop navigation": 'href="leistungen.html"' in pages["index.html"] and 'href="unternehmen.html"' in pages["index.html"],
    "home no full company section": 'class="company company-page"' not in pages["index.html"],
    "services page": 'Betonpumpendienst' in pages["leistungen.html"] and 'Frischbetontransporte' in pages["leistungen.html"],
    "company page": 'Seit 2010 steht RN Transporte' in pages["unternehmen.html"],
    "career page": 'Pumpenfahrer / Betonpumpenmaschinist' in pages["karriere.html"] and '<span>C/CE</span>' in pages["karriere.html"],
    "contact page": '0173 72 75 165' in pages["kontakt.html"] and 'Lohweg 55a' in pages["kontakt.html"],
    "favicon": all('assets/favicon-rn.svg' in html for html in pages.values()),
}
for label, ok in checks.items():
    if not ok:
        raise SystemExit(f"RN multipage check failed: {label}")
