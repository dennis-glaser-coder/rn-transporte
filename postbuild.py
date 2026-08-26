from pathlib import Path
import re

CONTACT_EMAIL = "ntorwesten@web.de"
ASSET_VERSION = "89"

# Homepage copy refinement.
page = Path("index.html")
html = page.read_text(encoding="utf-8")
html = html.replace("Direkt zum passenden Bereich.", "Alles Wichtige auf einen Blick.")
for number in ("01", "02", "03", "04"):
    html = html.replace(f"<span>{number}</span>", "")
page.write_text(html, encoding="utf-8")

# Keep homepage card spacing clean after removing the numbers.
css_path = Path("assets/premium.css")
css = css_path.read_text(encoding="utf-8")
css = css.replace(
    ".home-link-card h3{margin:48px 0 0;color:var(--ink);",
    ".home-link-card h3{margin:0;color:var(--ink);",
)
css = css.replace(
    ".home-link-card h3{margin-top:32px;font-size:27px}",
    ".home-link-card h3{margin-top:0;font-size:27px}",
)
css_path.write_text(css, encoding="utf-8")

# Calm editorial services page: two real images, no placeholder for Kiestransporte.
service_markup = '''
<section class="service-editorial" aria-label="Leistungen im Überblick">
  <div class="wrap service-editorial-list">
    <article class="service-feature">
      <div class="service-visual service-visual-fade-right">
        <img src="assets/leistungen/betonpumpendienst.png" alt="RN Transporte Betonpumpendienst im Einsatz" loading="lazy" decoding="async" fetchpriority="low">
      </div>
      <div class="service-feature-copy">
        <h2>Betonpumpendienst</h2>
        <p>Fördern und Einbringen von Beton direkt am Einsatzort.</p>
      </div>
    </article>

    <article class="service-feature service-feature-reverse">
      <div class="service-feature-copy">
        <h2>Frischbetontransporte</h2>
        <p>Frischbetontransporte mit Fahrmischern zwischen Betonwerk und Baustelle.</p>
      </div>
      <div class="service-visual service-visual-fade-left">
        <img src="assets/leistungen/frischbetontransport.png" alt="RN Transporte Fahrmischer beim Frischbetontransport" loading="lazy" decoding="async" fetchpriority="low">
      </div>
    </article>

    <article class="service-text-row">
      <h2>Kiestransporte</h2>
      <p>Transport von Kies und Schüttgütern zum jeweiligen Einsatzort.</p>
    </article>

    <div class="page-cta service-page-cta">
      <p>Sie möchten einen Einsatz oder Transport abstimmen?</p>
      <a href="kontakt.html">Projekt anfragen →</a>
    </div>
  </div>
</section>
'''

services_path = Path("leistungen.html")
services_html = services_path.read_text(encoding="utf-8")
services_html, replaced = re.subn(
    r'<section class="services page-services">.*?</section>',
    service_markup.strip(),
    services_html,
    count=1,
    flags=re.S,
)
if replaced != 1:
    raise SystemExit("RN service editorial replacement failed")

service_style = r'''<style id="rn-service-editorial-style">
.service-editorial{padding:58px 0 100px;background:#fff}
.service-editorial-list{max-width:1180px}
.service-feature{display:grid;grid-template-columns:minmax(0,1.12fr) minmax(320px,.88fr);align-items:center;min-height:390px;margin-bottom:86px}
.service-feature-reverse{grid-template-columns:minmax(320px,.88fr) minmax(0,1.12fr)}
.service-visual{position:relative;min-width:0;aspect-ratio:16/9;overflow:hidden;background:#f1f2f2}
.service-visual img{display:block;width:100%;height:100%;object-fit:cover;object-position:center 62%;filter:saturate(.84) contrast(.98) brightness(.98)}
.service-feature-reverse .service-visual img{object-position:center 66%}
.service-visual:after{content:"";position:absolute;inset:0;pointer-events:none}
.service-visual-fade-right:after{background:linear-gradient(90deg,rgba(255,255,255,0) 82%,rgba(255,255,255,.20) 92%,#fff 100%)}
.service-visual-fade-left:after{background:linear-gradient(270deg,rgba(255,255,255,0) 82%,rgba(255,255,255,.20) 92%,#fff 100%)}
.service-feature-copy{position:relative;z-index:2;padding:36px 0 36px 42px;background:#fff}
.service-feature-reverse .service-feature-copy{padding:36px 42px 36px 0}
.service-feature-copy h2,.service-text-row h2{margin:0;color:var(--ink);font-size:clamp(30px,3.1vw,46px);line-height:1.06;letter-spacing:-.045em;font-weight:530}
.service-feature-copy p{margin:15px 0 0;max-width:430px;color:#686c70;font-size:15px;line-height:1.72}
.service-text-row{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center;padding:58px 0 68px;border-top:1px solid #e4e5e6;border-bottom:1px solid #e4e5e6}
.service-text-row p{margin:0;max-width:520px;color:#686c70;font-size:15px;line-height:1.72}
.service-page-cta{margin-top:42px}
@media(max-width:900px){
  .service-editorial{padding:24px 0 70px}
  .service-feature,.service-feature-reverse{grid-template-columns:1fr;min-height:0;padding:0;margin-bottom:48px;border-bottom:1px solid #e4e5e6}
  .service-feature-reverse .service-feature-copy{order:2}
  .service-feature-reverse .service-visual{order:1}
  .service-visual{aspect-ratio:16/9;margin:0 -24px;width:calc(100% + 48px)}
  .service-visual img,.service-feature-reverse .service-visual img{object-position:center 64%}
  .service-visual-fade-right:after,.service-visual-fade-left:after{background:linear-gradient(180deg,rgba(255,255,255,0) 82%,rgba(255,255,255,.18) 92%,#fff 100%)}
  .service-feature-copy,.service-feature-reverse .service-feature-copy{padding:22px 0 38px}
  .service-feature-copy h2,.service-text-row h2{font-size:31px}
  .service-feature-copy p{margin-top:11px}
  .service-text-row{grid-template-columns:1fr;gap:13px;padding:40px 0}
  .service-page-cta{margin-top:34px}
}
</style>'''
services_html = services_html.replace("</head>", service_style + "\n</head>", 1)
services_path.write_text(services_html, encoding="utf-8")

# Contact email. CONTACT_EMAIL is intentionally a single variable so the
# future rn-transporte.de mailbox can be swapped without touching the layout.
contact_path = Path("kontakt.html")
contact_html = contact_path.read_text(encoding="utf-8")
contact_html = contact_html.replace(
    "Betonpumpendienst oder Transportbedarf? Rufen Sie direkt an oder senden Sie Ihre Anfrage per WhatsApp.",
    "Betonpumpendienst oder Transportbedarf? Rufen Sie an, schreiben Sie per WhatsApp oder senden Sie eine E-Mail.",
)
contact_html = contact_html.replace(
    "Kurze Wege und direkte Abstimmung: RN Transporte erreichen Sie telefonisch oder per WhatsApp.",
    "Kurze Wege und direkte Abstimmung: RN Transporte erreichen Sie telefonisch, per WhatsApp oder E-Mail.",
)
phone_markup = '<a class="contact-number" href="tel:+491737275165">0173 72 75 165</a>'
if phone_markup not in contact_html:
    raise SystemExit("RN contact phone markup not found")
contact_html = contact_html.replace(
    phone_markup,
    phone_markup + f'<a class="contact-email" href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>',
    1,
)
links_old = '<div class="contact-links"><a href="tel:+491737275165">Anrufen</a><a class="contact-whatsapp" href="https://wa.me/491737275165?text=Hallo%20RN%20Torwesten%20Transporte%2C%20ich%20habe%20eine%20Anfrage." target="_blank" rel="noopener">WhatsApp →</a></div>'
links_new = f'<div class="contact-links"><a href="tel:+491737275165">Anrufen</a><a class="contact-whatsapp" href="https://wa.me/491737275165?text=Hallo%20RN%20Torwesten%20Transporte%2C%20ich%20habe%20eine%20Anfrage." target="_blank" rel="noopener">WhatsApp →</a><a class="contact-mail-action" href="mailto:{CONTACT_EMAIL}">E-Mail →</a></div>'
if links_old not in contact_html:
    raise SystemExit("RN contact links markup not found")
contact_html = contact_html.replace(links_old, links_new, 1)

contact_style = r'''<style id="rn-contact-email-style">
.contact-email{display:block;width:max-content;max-width:100%;margin-top:13px;color:#fff;font-size:clamp(18px,1.55vw,23px);font-weight:550;letter-spacing:-.018em;overflow-wrap:anywhere;transition:opacity .18s ease}
.contact-links{flex-wrap:wrap}
.contact-mail-action{color:#fff;font-size:13px;font-weight:700}
@media(hover:hover){.contact-email:hover,.contact-mail-action:hover{opacity:.68}}
@media(max-width:900px){.contact-email{margin-top:11px;font-size:18px}.contact-links{gap:18px 24px}}
</style>'''
contact_html = contact_html.replace("</head>", contact_style + "\n</head>", 1)
contact_path.write_text(contact_html, encoding="utf-8")

# Cache-proof mobile navigation. This lives inside every page so an old Safari
# cache of premium.css can no longer break the menu.
mobile_fix = r'''<style id="rn-mobile-menu-fix">
@media(max-width:900px){
  body.menu-open{overflow:hidden!important}
  header{z-index:1000!important;overflow:visible!important}
  header.open{z-index:1000!important;background:#fff!important;-webkit-backdrop-filter:none!important;backdrop-filter:none!important}
  .head{grid-template-columns:1fr auto!important}
  .header-cta{display:none!important}
  .menu{display:flex!important;align-items:center!important;justify-content:flex-end!important;gap:9px!important;width:auto!important;height:44px!important;padding:6px 0 6px 10px!important;border:0!important;background:transparent!important;color:var(--ink)!important}
  .menu span{margin:0!important;background:none!important;height:auto!important}
  .menu-word{display:block!important;font-size:11px!important;font-weight:780!important;letter-spacing:.11em!important;line-height:1!important;transform:none!important;opacity:1!important}
  .menu-bars{display:flex!important;width:22px!important;height:18px!important;flex-direction:column!important;justify-content:space-between!important;transform:none!important;opacity:1!important}
  .menu-bars i{display:block!important;width:22px!important;height:2px!important;margin:0!important;background:var(--ink)!important;transform-origin:center!important;transition:transform .22s ease,opacity .18s ease!important}
  header.open .menu .menu-word{transform:none!important;opacity:1!important}
  header.open .menu .menu-bars{transform:none!important;opacity:1!important}
  header.open .menu-bars i:nth-child(1){transform:translateY(8px) rotate(45deg)!important}
  header.open .menu-bars i:nth-child(2){opacity:0!important}
  header.open .menu-bars i:nth-child(3){transform:translateY(-8px) rotate(-45deg)!important}
  .nav{display:none!important}
  header.open .nav{display:flex!important;position:absolute!important;top:74px!important;left:0!important;right:0!important;width:100vw!important;height:calc(100vh - 74px)!important;height:calc(100dvh - 74px)!important;z-index:9999!important;flex-direction:column!important;justify-content:flex-start!important;gap:0!important;padding:26px 24px calc(28px + env(safe-area-inset-bottom))!important;background:#fff!important;border-top:1px solid #ededed!important;border-bottom:0!important;box-shadow:none!important;overflow-y:auto!important;-webkit-overflow-scrolling:touch!important}
  header.open .nav a{display:block!important;padding:18px 0!important;border-bottom:1px solid #ededed!important;color:var(--ink)!important;font-size:22px!important;line-height:1.2!important;font-weight:570!important;letter-spacing:-.025em!important}
  header.open .nav a.active{color:var(--red)!important}
  header.open .nav .mobile-project-link{display:flex!important;align-items:center!important;justify-content:space-between!important;margin-top:24px!important;padding:17px 18px!important;border:0!important;background:var(--red)!important;color:#fff!important;font-size:14px!important;font-weight:760!important;letter-spacing:0!important}
  header.open .nav .mobile-project-link:after{content:"→";font-size:18px}
}
</style>'''

for filename in ("index.html", "leistungen.html", "unternehmen.html", "karriere.html", "kontakt.html"):
    path = Path(filename)
    html = path.read_text(encoding="utf-8")
    html = html.replace('href="assets/premium.css"', f'href="assets/premium.css?v={ASSET_VERSION}"')
    html = html.replace("</head>", mobile_fix + "\n</head>", 1)
    path.write_text(html, encoding="utf-8")
