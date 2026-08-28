from pathlib import Path

path = Path("unternehmen.html")
html = path.read_text(encoding="utf-8")

# Introduce the full company name once in the company copy, then keep the
# shorter public-facing RN Transporte name throughout the rest of the site.
old_name_intro = "Seit 2010 steht RN Transporte aus Salzkotten für zuverlässige Transport- und Betonlogistik."
new_name_intro = "RN Torwesten Transporte wurde 2010 in Salzkotten gegründet. Seitdem steht RN Transporte für zuverlässige Transport- und Betonlogistik."
if old_name_intro not in html:
    raise SystemExit("RN company full-name introduction not found")
html = html.replace(old_name_intro, new_name_intro, 1)

opening = '<section class="company company-page"><div class="wrap company-grid">'
replacement = '''<section class="company company-page company-editorial">
<div class="wrap company-stage-media">
  <img src="assets/leistungen/Baustelleneinsatz.png" alt="RN Transporte im Baustelleneinsatz" loading="lazy" decoding="async" fetchpriority="low">
</div>
<div class="wrap company-grid">'''
if opening not in html:
    raise SystemExit("RN company page section not found")
html = html.replace(opening, replacement, 1)

meta = '<div class="company-meta"><span><strong>Standort</strong> Salzkotten</span><span><strong>Einsatzgebiet</strong> Deutschlandweit</span></div>'
cta = '''<div class="company-page-cta">
  <p>Sie möchten mit RN Transporte zusammenarbeiten?</p>
  <a href="kontakt.html">Kontakt aufnehmen →</a>
</div>'''
if meta not in html:
    raise SystemExit("RN company metadata not found")
html = html.replace(meta, meta + cta, 1)

style = r'''<style id="rn-company-editorial-style">
.company-page.company-editorial{background:#fff;padding:46px 0 104px}
.company-stage-media{position:relative;max-width:1180px;aspect-ratio:2.2/1;margin-bottom:72px;overflow:hidden;background:#f1f2f2}
.company-stage-media img{display:block;width:100%;height:100%;object-fit:cover;object-position:center 58%;filter:saturate(.86) contrast(.98) brightness(.98)}
.company-stage-media:after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,rgba(255,255,255,0) 80%,rgba(255,255,255,.18) 92%,rgba(255,255,255,.52) 100%)}
.company-editorial .company-grid{grid-template-columns:minmax(150px,.28fr) minmax(0,1.72fr);gap:72px;align-items:start}
.company-editorial .company-main{max-width:980px}
.company-editorial .company-main h2{max-width:900px}
.company-editorial .company-meta{margin-top:38px;padding-top:22px;border-top:1px solid #dfe1e2}
.company-page-cta{display:flex;align-items:center;justify-content:space-between;gap:32px;margin-top:40px;padding-top:24px;border-top:1px solid #dfe1e2}
.company-page-cta p{margin:0;color:#676b6f;font-size:14px;line-height:1.6}
.company-page-cta a{color:var(--red);font-size:13px;font-weight:720;white-space:nowrap;transition:opacity .18s ease}
@media(hover:hover){.company-page-cta a:hover{opacity:.65}}
@media(max-width:900px){
  .company-page.company-editorial{padding:24px 0 72px}
  .company-stage-media{aspect-ratio:16/10;margin-bottom:42px}
  .company-stage-media img{object-position:center 56%}
  .company-stage-media:after{background:linear-gradient(180deg,rgba(255,255,255,0) 84%,rgba(255,255,255,.14) 94%,rgba(255,255,255,.38) 100%)}
  .company-editorial .company-grid{grid-template-columns:1fr;gap:18px}
  .company-editorial .company-meta{margin-top:30px}
  .company-page-cta{align-items:flex-start;flex-direction:column;gap:14px;margin-top:30px;padding-top:22px}
}
</style>'''
if 'id="rn-company-editorial-style"' not in html:
    html = html.replace("</head>", style + "\n</head>", 1)

path.write_text(html, encoding="utf-8")
