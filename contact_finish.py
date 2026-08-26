from pathlib import Path

path = Path("kontakt.html")
html = path.read_text(encoding="utf-8")

# The page hero already explains the purpose. Remove the repeated second intro
# so the user reaches the actual contact options immediately.
html = html.replace('<h2>Wir sprechen über Ihren Einsatz.</h2>', '', 1)
html = html.replace('<p class="contact-copy">Kurze Wege und direkte Abstimmung: RN Transporte erreichen Sie telefonisch, per WhatsApp oder E-Mail.</p>', '', 1)

# Premium inline SVG actions: no emoji, no external icon dependency.
phone_icon = '''<svg class="contact-action-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 3.8 9 3.2l2 4.7-1.7 1.3c1 2.1 2.6 3.8 4.7 4.8l1.4-1.8 4.7 2-.6 2.5c-.3 1.4-1.6 2.3-3 2.1C9.9 17.9 5 13 4.1 6.8c-.2-1.4.7-2.7 2.5-3Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
whatsapp_icon = '''<svg class="contact-action-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 11.7a8 8 0 0 1-11.8 7L4 20l1.3-4.1A8 8 0 1 1 20 11.7Z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/><path d="M8.6 7.7c.2-.3.4-.3.7-.3h.5c.2 0 .4.1.5.4l.8 1.9c.1.3.1.5-.1.7l-.7.8c.8 1.6 1.9 2.7 3.5 3.5l.8-.9c.2-.2.4-.3.7-.1l1.8.8c.3.1.4.3.4.6 0 .8-.4 1.5-1.1 1.9-.6.3-1.4.5-2.3.2-1.8-.5-3.6-1.6-5-3-1.4-1.4-2.5-3.2-3-5-.2-.6 0-1.1.5-1.5Z" fill="none" stroke="currentColor" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
mail_icon = '''<svg class="contact-action-icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5.5" width="17" height="13" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="m4.5 7 7.5 5.7L19.5 7" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>'''

call_old = '<a href="tel:+491737275165">Anrufen</a>'
call_new = f'<a class="contact-call-action" href="tel:+491737275165"><span class="contact-action-label">{phone_icon}<span>Anrufen</span></span><span class="contact-action-arrow" aria-hidden="true">→</span></a>'
whatsapp_old = '<a class="contact-whatsapp" href="https://wa.me/491737275165?text=Hallo%20RN%20Torwesten%20Transporte%2C%20ich%20habe%20eine%20Anfrage." target="_blank" rel="noopener">WhatsApp →</a>'
whatsapp_new = f'<a class="contact-whatsapp" href="https://wa.me/491737275165?text=Hallo%20RN%20Torwesten%20Transporte%2C%20ich%20habe%20eine%20Anfrage." target="_blank" rel="noopener"><span class="contact-action-label">{whatsapp_icon}<span>WhatsApp</span></span><span class="contact-action-arrow" aria-hidden="true">→</span></a>'
mail_old = '<a class="contact-mail-action" href="mailto:ntorwesten@web.de">E-Mail →</a>'
mail_new = f'<a class="contact-mail-action" href="mailto:ntorwesten@web.de"><span class="contact-action-label">{mail_icon}<span>E-Mail</span></span><span class="contact-action-arrow" aria-hidden="true">→</span></a>'

for old, new, label in (
    (call_old, call_new, "call action"),
    (whatsapp_old, whatsapp_new, "WhatsApp action"),
    (mail_old, mail_new, "email action"),
):
    if old not in html:
        raise SystemExit(f"RN {label} markup not found")
    html = html.replace(old, new, 1)

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
  gap:14px!important;
  min-height:54px!important;
  padding:0 17px!important;
  border:1px solid #d4d6d5!important;
  background:#fff!important;
  color:#202326!important;
  font-size:11px!important;
  font-weight:760!important;
  letter-spacing:.045em!important;
  text-transform:uppercase!important;
  transition:background .2s ease,border-color .2s ease,color .2s ease,box-shadow .2s ease!important;
}
.contact-action-label{display:inline-flex;align-items:center;gap:11px;min-width:0}
.contact-action-icon{display:block;width:19px;height:19px;flex:0 0 19px;color:currentColor}
.contact-action-arrow{font-size:15px;line-height:1;opacity:.72;transition:transform .2s ease,opacity .2s ease}
.contact-links .contact-call-action{
  border-color:var(--red)!important;
  background:var(--red)!important;
  color:#fff!important;
}
.contact-links .contact-whatsapp{
  border-color:#b9dcc5!important;
  background:#fbfefc!important;
  color:#202326!important;
  box-shadow:inset 3px 0 0 #25d366!important;
}
.contact-links .contact-whatsapp .contact-action-icon{color:#20b858!important}
.contact-links .contact-mail-action .contact-action-icon{color:#50555a!important}
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
  .contact-links a:hover .contact-action-arrow{transform:translateX(3px);opacity:1}
  .contact-links .contact-call-action:hover{background:var(--red-dark)!important;border-color:var(--red-dark)!important;opacity:1!important}
  .contact-links .contact-whatsapp:hover{background:#f3fbf5!important;border-color:#8fcfa3!important;color:#171a1c!important;opacity:1!important}
  .contact-links .contact-mail-action:hover{background:#202326!important;border-color:#202326!important;color:#fff!important;opacity:1!important}
  .contact-links .contact-mail-action:hover .contact-action-icon{color:#fff!important}
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
  .contact-links .contact-call-action{grid-column:1/-1!important}
  .contact-links a{min-height:52px!important;padding:0 15px!important}
  .contact-address{margin-top:30px!important;padding-top:22px!important}
}

@media(max-width:390px){
  .contact-number{font-size:33px!important}
  .contact-links{grid-template-columns:1fr!important}
  .contact-links .contact-call-action{grid-column:auto!important}
}
</style>'''

if 'id="rn-contact-final"' in html:
    raise SystemExit("RN final contact style already present")
if 'Wir sprechen über Ihren Einsatz.' in html:
    raise SystemExit("Duplicate contact heading still present")
if 'Kurze Wege und direkte Abstimmung:' in html:
    raise SystemExit("Duplicate contact copy still present")
if html.count('class="contact-action-icon"') != 3:
    raise SystemExit("RN contact action icons not inserted exactly three times")

html = html.replace("</head>", style + "\n</head>", 1)
path.write_text(html, encoding="utf-8")
