from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"Expected {label} not found")
    return text.replace(old, new, 1)


p = Path("index.html")
s = p.read_text(encoding="utf-8")

company_old = '<h2>RN Transporte</h2><p>Inhabergeführtes Transportunternehmen aus Salzkotten-Niederntudorf mit Schwerpunkt auf Betonlogistik und Baustellentransporten.</p>'
company_new = '<h2>RN Transporte – zuverlässig. leistungsstark. deutschlandweit im Einsatz.</h2><div class="company-copy"><p>Seit 2010 steht RN Transporte aus Salzkotten für zuverlässige Transport- und Betonlogistik. Als inhabergeführtes Unternehmen sind wir kontinuierlich gewachsen und haben uns mit Erfahrung, Flexibilität und persönlichem Einsatz als verlässlicher Partner für unsere Kunden etabliert.</p><p>Unser Leistungsspektrum umfasst den Transport von Frischbeton mit Fahrmischern, Baustofftransporte mit Sattelkippern, Holztransporte sowie das fachgerechte Fördern und Pumpen von Beton mit unseren Betonpumpen.</p><p>Mit einem leistungsfähigen Fuhrpark, erfahrenen Mitarbeitern und kurzen Entscheidungswegen sorgen wir dafür, dass unsere Aufträge zuverlässig, termingerecht und professionell umgesetzt werden. Dabei legen wir besonderen Wert auf persönliche Betreuung, hohe Einsatzbereitschaft und flexible Lösungen.</p><p>Heute sind wir <strong>deutschlandweit</strong> für unsere Kunden im Einsatz und stehen für eine partnerschaftliche Zusammenarbeit, auf die man sich verlassen kann – vom einzelnen Transportauftrag bis hin zu umfangreichen Projekten.</p></div>'

replacements = [
    ('</head>', '<link rel="stylesheet" href="assets/premium.css">\n</head>', 'premium stylesheet hook'),
    ('src="assets/logo.svg"', 'src="assets/logo.webp"', 'real logo image'),
    ('<a class="phone" href="tel:+491737275165">0173 72 75 165</a>', '<a class="header-cta" href="#kontakt">Projekt anfragen</a>', 'header phone replacement'),
    ('<div class="hero-place">Salzkotten-Niederntudorf</div>', '<div class="hero-place">Salzkotten-Niederntudorf · Deutschlandweit</div>', 'hero location'),
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
    "company": 'Seit 2010 steht RN Transporte' in s and 'Holztransporte' in s,
    "career": 'Karriere bei RN Transporte' in s,
    "driver licence": '<span>C/CE</span>' in s,
    "contact": 'Projekt oder Einsatz anfragen.' in s,
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
.company-copy{margin-top:28px;display:grid;gap:16px;max-width:790px}
.company-copy p{margin:0;color:#5e6266;font-size:15.5px;line-height:1.74}
.company-copy strong{color:var(--ink);font-weight:680}
@media(max-width:900px){.service h2{margin-top:0!important}.company-copy{margin-top:22px;gap:14px}.company-copy p{font-size:15px;line-height:1.68}}
'''
css_path.write_text(css, encoding="utf-8")

for legal_name in ("impressum.html", "datenschutz.html"):
    lp = Path(legal_name)
    legal = lp.read_text(encoding="utf-8")
    legal = replace_once(legal, 'src="assets/logo.svg"', 'src="assets/logo.webp"', f'{legal_name} real logo')
    legal = legal.replace('.logo{width:228px}', '.logo{width:228px;height:auto;object-fit:contain}', 1)
    legal = legal.replace('.logo{width:200px}', '.logo{width:200px;height:auto;object-fit:contain}', 1)
    lp.write_text(legal, encoding="utf-8")
