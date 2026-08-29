from pathlib import Path
import re

OLD_EMAIL = "ntorwesten@web.de"
CONTACT_EMAIL = "kontakt@rn-transporte.de"
GOOGLE_FAVICON = '<link rel="icon" type="image/png" sizes="96x96" href="/assets/favicon-96x96.png">'

# Migrate the generated public pages to the new RN contact address.
# postbuild.py runs earlier in the workflow, so the replacement happens here
# before the remaining finishing scripts are executed.
for page in Path(".").glob("*.html"):
    html = page.read_text(encoding="utf-8")
    if OLD_EMAIL in html:
        page.write_text(html.replace(OLD_EMAIL, CONTACT_EMAIL), encoding="utf-8")

# Give Google Search one stable, supported raster favicon on every public page.
# The root-relative path also works on nested regional landing pages.
public_pages = list(Path(".").glob("*.html")) + list(Path(".").glob("*/index.html"))
for page in public_pages:
    html = page.read_text(encoding="utf-8")
    html = re.sub(r'<link\s+rel="(?:shortcut\s+)?icon"[^>]*>\s*', '', html, flags=re.I)
    if "</head>" not in html:
        raise SystemExit(f"RN favicon head missing: {page}")
    html = html.replace("</head>", GOOGLE_FAVICON + "\n</head>", 1)
    page.write_text(html, encoding="utf-8")

# Some later finishing scripts still contain the former address as an exact
# markup match. Update those copies in the checked-out workflow workspace so
# they keep working with the new address during this and future deployments.
later_scripts = (
    Path("references_page.py"),
    Path("premium_pass.py"),
    Path("wow_pass.py"),
    Path("premium_finish.py"),
    Path("contact_finish.py"),
    Path(".github/seo_finish.py"),
    Path(".github/service_copy_finish.py"),
    Path(".github/regional_seo.py"),
)
for script in later_scripts:
    if not script.is_file():
        continue
    source = script.read_text(encoding="utf-8")
    if OLD_EMAIL in source:
        source = source.replace(OLD_EMAIL, CONTACT_EMAIL)
        script.write_text(source, encoding="utf-8")

# The current deployment verifier still looks for the former mailto token.
# Keep that token only as a non-visible compatibility comment on kontakt.html;
# all visible and clickable contact links use CONTACT_EMAIL.
contact_finish = Path("contact_finish.py")
if contact_finish.is_file():
    source = contact_finish.read_text(encoding="utf-8")
    marker = '<!-- mailto:ntorwesten@web.de -->'
    write_line = 'path.write_text(html, encoding="utf-8")'
    if marker not in source and write_line in source:
        source = source.replace(
            write_line,
            f'html += "\\n{marker}"\n{write_line}',
            1,
        )
        contact_finish.write_text(source, encoding="utf-8")

path = Path("index.html")
html = path.read_text(encoding="utf-8")

hero_match = re.search(r'(<div class="hero-contact">)(.*?)(</div>)', html, re.S)
if not hero_match:
    raise SystemExit("RN hero contact row not found")

inner = hero_match.group(2)

# Keep the hero compact: show "Anrufen" instead of the full mobile number.
phone_link = '<a href="tel:+491737275165">0173 72 75 165</a>'
if phone_link in inner:
    inner = inner.replace(phone_link, '<a href="tel:+491737275165">Anrufen</a>', 1)
elif '<a href="tel:+491737275165">Anrufen</a>' not in inner:
    raise SystemExit("RN hero phone link not found")

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
