from pathlib import Path

path = Path("kontakt.html")
html = path.read_text(encoding="utf-8")

# The page hero already explains the purpose. Remove the repeated second intro
# so the user reaches the actual contact options immediately.
html = html.replace('<h2>Wir sprechen über Ihren Einsatz.</h2>', '', 1)
html = html.replace('<p class="contact-copy">Kurze Wege und direkte Abstimmung: RN Transporte erreichen Sie telefonisch, per WhatsApp oder E-Mail.</p>', '', 1)

style = r'''<style id="rn-contact-final">
/* Final contact composition: strong dark page intro, then direct light contact area. */
.contact-page{
  background:#fff!important;
  color:var(--ink)!important;
  padding:76px 0 92px!important;
  box-shadow:inset 0 1px #e3e4e2!important;
}
.contact-page:before{display:none!important}
.contact-grid{
  grid-template-columns:minmax(170px,.38fr) minmax(0,1.62fr)!important;
  gap:72px!important;
  align-items:start!important;
}
.contact-grid>.eyebrow{color:#74797e!important;padding-top:10px!important}
.contact-main{max-width:860px!important}
.contact-number{
  margin:0!important;
  color:#191b1e!important;
  font-size:clamp(34px,3.6vw,50px)!important;
  line-height:1!important;
  letter-spacing:-.04em!important;
  font-weight:560!important;
}
.contact-email{
  margin-top:14px!important;
  color:#292d31!important;
  font-size:clamp(18px,1.6vw,22px)!important;
  font-weight:540!important;
}
.contact-links{
  display:grid!important;
  grid-template-columns:repeat(3,minmax(0,1fr))!important;
  gap:10px!important;
  margin-top:34px!important;
  padding-top:28px!important;
  border-top:1px solid #dedfdd!important;
}
.contact-links a{
  display:flex!important;
  align-items:center!important;
  justify-content:space-between!important;
  min-height:52px!important;
  padding:0 17px!important;
  border:1px solid #d4d6d5!important;
  background:#fff!important;
  color:#202326!important;
  font-size:11px!important;
  font-weight:760!important;
  letter-spacing:.045em!important;
  text-transform:uppercase!important;
  transition:background .2s ease,border-color .2s ease,color .2s ease!important;
}
.contact-links a:first-child{
  border-color:var(--red)!important;
  background:var(--red)!important;
  color:#fff!important;
}
.contact-links a:after{font-size:15px;line-height:1}
.contact-links a:first-child:after{content:"→"}
.contact-address{
  display:grid!important;
  gap:6px!important;
  margin-top:40px!important;
  padding-top:25px!important;
  border-top:1px solid #dedfdd!important;
  color:#6b6f73!important;
  font-size:13px!important;
  line-height:1.55!important;
}
.contact-address strong{color:#24272a!important;font-weight:670!important}

@media(hover:hover){
  .contact-links a:not(:first-child):hover{background:#202326!important;border-color:#202326!important;color:#fff!important;opacity:1!important}
  .contact-links a:first-child:hover{background:var(--red-dark)!important;border-color:var(--red-dark)!important;opacity:1!important}
  .contact-number:hover,.contact-email:hover{opacity:.65!important}
}

@media(max-width:900px){
  .contact-page{padding:48px 0 64px!important}
  .contact-grid{grid-template-columns:1fr!important;gap:24px!important}
  .contact-grid>.eyebrow{padding-top:0!important}
  .contact-main{max-width:none!important}
  .contact-number{font-size:36px!important}
  .contact-email{margin-top:11px!important;font-size:18px!important}
  .contact-links{
    grid-template-columns:1fr 1fr!important;
    gap:9px!important;
    margin-top:28px!important;
    padding-top:24px!important;
  }
  .contact-links a:first-child{grid-column:1/-1!important}
  .contact-links a{min-height:50px!important;padding:0 15px!important}
  .contact-address{margin-top:30px!important;padding-top:22px!important}
}

@media(max-width:390px){
  .contact-number{font-size:33px!important}
  .contact-links{grid-template-columns:1fr!important}
  .contact-links a:first-child{grid-column:auto!important}
}
</style>'''

if 'id="rn-contact-final"' in html:
    raise SystemExit("RN final contact style already present")
if 'Wir sprechen über Ihren Einsatz.' in html:
    raise SystemExit("Duplicate contact heading still present")
if 'Kurze Wege und direkte Abstimmung:' in html:
    raise SystemExit("Duplicate contact copy still present")

html = html.replace("</head>", style + "\n</head>", 1)
path.write_text(html, encoding="utf-8")
