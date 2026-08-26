from pathlib import Path

path = Path("leistungen.html")
html = path.read_text(encoding="utf-8")

old = '''<article class="service-text-row">
      <h2>Kiestransporte</h2>
      <p>Transport von Kies und Schüttgütern zum jeweiligen Einsatzort.</p>
    </article>'''

new = '''<article class="service-feature service-feature-last">
      <div class="service-visual service-visual-fade-right">
        <img src="assets/leistungen/Kiestransporte.png" alt="RN Transporte Kiestransport im Einsatz" loading="lazy" decoding="async" fetchpriority="low">
      </div>
      <div class="service-feature-copy">
        <h2>Kiestransporte</h2>
        <p>Transport von Kies und Schüttgütern zum jeweiligen Einsatzort.</p>
      </div>
    </article>

    <article class="service-text-row service-text-row-wood" id="holztransporte">
      <h2>Holztransporte</h2>
      <p>Transport von Holz mit passender Fahrzeugtechnik – zuverlässig abgestimmt vom Ladeort bis zum Ziel.</p>
    </article>'''

if old not in html:
    raise SystemExit("RN Kiestransporte text block not found")
html = html.replace(old, new, 1)

style = r'''<style id="rn-kies-image-style">
.service-feature-last{margin-bottom:0;padding-bottom:58px;border-bottom:1px solid #e4e5e6}
.service-text-row-wood{border-top:0}
@media(max-width:900px){.service-feature-last{margin-bottom:0;padding-bottom:0}.service-text-row-wood{margin-top:0}}
</style>'''
if 'id="rn-kies-image-style"' not in html:
    html = html.replace("</head>", style + "\n</head>", 1)

path.write_text(html, encoding="utf-8")
