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
    inner += f'<a class="hero-email" href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>'
    html = html[:hero_match.start()] + hero_match.group(1) + inner + hero_match.group(3) + html[hero_match.end():]

hero_email_style = r'''<style id="rn-hero-email-style">
.hero-contact{flex-wrap:wrap;row-gap:12px}
.hero-email{color:rgba(255,255,255,.88);font-size:12px;font-weight:560;letter-spacing:-.005em;white-space:nowrap;transition:opacity .18s ease}
@media(hover:hover){.hero-email:hover{opacity:.68}}
@media(max-width:900px){.hero-contact{gap:12px 18px}.hero-email{font-size:11px}}
</style>'''
if 'id="rn-hero-email-style"' not in html:
    html = html.replace("</head>", hero_email_style + "\n</head>", 1)

path.write_text(html, encoding="utf-8")
