from pathlib import Path
import re

# Reuse the contact email from postbuild.py so it only needs to be changed in one place later.
postbuild = Path("postbuild.py").read_text(encoding="utf-8")
match = re.search(r'^CONTACT_EMAIL\s*=\s*"([^"]+)"', postbuild, re.M)
if not match:
    raise SystemExit("RN contact email configuration not found")
CONTACT_EMAIL = match.group(1)

path = Path("index.html")
html = path.read_text(encoding="utf-8")

hero_match = re.search(r'(<div class="hero-contact">)(.*?)(</div>)', html, re.S)
if not hero_match:
    raise SystemExit("RN hero contact row not found")

inner = hero_match.group(2)
if f'mailto:{CONTACT_EMAIL}' not in inner:
    mail_icon = (
        f'<a class="hero-email" href="mailto:{CONTACT_EMAIL}" aria-label="E-Mail schreiben">'
        '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<rect x="3" y="5" width="18" height="14" rx="1.5"></rect>'
        '<path d="m4 7 8 6 8-6"></path>'
        '</svg></a>'
    )
    inner += mail_icon
    html = html[:hero_match.start()] + hero_match.group(1) + inner + hero_match.group(3) + html[hero_match.end():]

hero_email_style = r'''<style id="rn-hero-email-style">
.hero-contact{flex-wrap:wrap;row-gap:12px}
.hero-email{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;margin:-9px;color:#fff;opacity:.94;transition:opacity .18s ease}
.hero-email svg{display:block}
@media(hover:hover){.hero-email:hover{opacity:.62}}
@media(max-width:900px){.hero-contact{gap:12px 18px}}
</style>'''
if 'id="rn-hero-email-style"' not in html:
    html = html.replace("</head>", hero_email_style + "\n</head>", 1)

path.write_text(html, encoding="utf-8")
