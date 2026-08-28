from pathlib import Path
from datetime import date
import re
import subprocess
import sys

try:
    from PIL import Image
except ImportError:
    vendor = Path("/tmp/rn-pillow")
    subprocess.run([sys.executable, "-m", "pip", "install", "--disable-pip-version-check", "--target", str(vendor), "Pillow"], check=True)
    sys.path.insert(0, str(vendor))
    from PIL import Image

SITE_URL = "https://dennis-glaser-coder.github.io/rn-transporte/"
REF_URL = SITE_URL + "referenzen.html"

# Add Referenzen to the main navigation of all generated pages.
main_pages = ("index.html", "leistungen.html", "unternehmen.html", "karriere.html", "kontakt.html")
for filename in main_pages:
    path = Path(filename)
    html = path.read_text(encoding="utf-8")
    if 'href="referenzen.html"' not in html:
        html, count = re.subn(
            r'(<a href="leistungen\.html"[^>]*>Leistungen</a>)',
            r'\1<a href="referenzen.html">Referenzen</a>',
            html,
            count=1,
        )
        if count != 1:
            raise SystemExit(f"RN references nav insertion failed: {filename}")
    path.write_text(html, encoding="utf-8")

# Use the already generated/refined services page as the structural shell so
# header, footer, mobile menu and shared premium styling remain identical.
template = Path("leistungen.html").read_text(encoding="utf-8")

# Remove service-only inline styles from the copied shell.
template = re.sub(r'\s*<style id="rn-service-editorial-style">.*?</style>', '', template, flags=re.S)
template = re.sub(r'\s*<style id="rn-kies-image-style">.*?</style>', '', template, flags=re.S)

# Correct active navigation state.
template = template.replace(
    '<a href="leistungen.html" class="active" aria-current="page">Leistungen</a>',
    '<a href="leistungen.html">Leistungen</a>',
    1,
)
template = template.replace(
    '<a href="referenzen.html">Referenzen</a>',
    '<a href="referenzen.html" class="active" aria-current="page">Referenzen</a>',
    1,
)

# Page-specific metadata.
title = "Referenzen | RN Transporte Salzkotten"
description = "Baustelleneinsätze und Referenzbilder von RN Transporte aus dem täglichen Einsatz."
template = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', template, count=1, flags=re.S)
template = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{description}">', template, count=1)
template = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', template, count=1)
template = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{description}">', template, count=1)
template = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{title}">', template, count=1)
template = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{description}">', template, count=1)
template = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="{REF_URL}">', template, count=1)
template = re.sub(r'<meta property="og:url" content="[^"]+">', f'<meta property="og:url" content="{REF_URL}">', template, count=1)

# Keep the uploaded PNGs untouched and generate lightweight WebP copies for the public gallery.
reference_sources = [
    ("assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_31_47.png", "assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_31_47.webp"),
    ("assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_31_59.png", "assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_31_59.webp"),
    ("assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_32_07.png", "assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_32_07.webp"),
    ("assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_32_16.png", "assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_32_16.webp"),
    ("assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_32_24.png", "assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_32_24.webp"),
    ("assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_32_33.png", "assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_32_33.webp"),
    ("assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_32_39.png", "assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_32_39.webp"),
    ("assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_32_46.png", "assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_32_46.webp"),
]

for source_path, output_path in reference_sources:
    source = Path(source_path)
    if not source.is_file():
        raise SystemExit(f"Missing reference image: {source_path}")
    with Image.open(source) as image:
        image = image.convert("RGB")
        image.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
        image.save(output_path, "WEBP", quality=82, method=6)

gallery_markup = "\n".join(
    f'<div class="reference-photo"><img src="{output_path}" alt="RN Transporte Baustelleneinsatz" loading="lazy" decoding="async" fetchpriority="low"></div>'
    for _, output_path in reference_sources
)

references_main = f'''
<section class="page-hero reference-hero"><div class="wrap page-hero-grid">
  <div class="eyebrow">Referenzen</div>
  <div><h1>Baustelleneinsätze.</h1></div>
</div></section>

<section class="references-page" aria-label="Baustelleneinsätze von RN Transporte">
  <div class="wrap">
    <div class="reference-photo-grid">
      {gallery_markup}
    </div>
  </div>
</section>
'''.strip()

template, count = re.subn(r'<main>.*?</main>', f'<main>\n{references_main}\n</main>', template, count=1, flags=re.S)
if count != 1:
    raise SystemExit("RN references main replacement failed")

references_style = r'''<style id="rn-references-style">
.reference-hero{padding-bottom:42px}
.references-page{padding:0 0 104px;background:#fff}
.reference-photo-grid{columns:2 430px;column-gap:24px}
.reference-photo{margin:0 0 24px;break-inside:avoid;overflow:hidden;background:#f1f2f2}
.reference-photo img{display:block;width:100%;height:auto;transition:transform .45s ease}
@media(hover:hover){.reference-photo:hover img{transform:scale(1.01)}}
@media(max-width:900px){
  .reference-hero{padding-bottom:28px}
  .references-page{padding:0 0 74px}
  .reference-photo-grid{columns:1;margin:0 -16px}
  .reference-photo{margin-bottom:12px}
}
</style>'''

template = template.replace("</head>", references_style + "\n</head>", 1)
Path("referenzen.html").write_text(template, encoding="utf-8")

# Add the new page to the sitemap without disturbing the generated entries.
sitemap_path = Path("sitemap.xml")
sitemap = sitemap_path.read_text(encoding="utf-8")
if REF_URL not in sitemap:
    entry = f"  <url>\n    <loc>{REF_URL}</loc>\n    <lastmod>{date.today().isoformat()}</lastmod>\n  </url>\n"
    sitemap = sitemap.replace("</urlset>", entry + "</urlset>", 1)
    sitemap_path.write_text(sitemap, encoding="utf-8")
