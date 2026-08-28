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
description = "Referenzen und Einblicke in Einsätze von RN Transporte: Betonpumpendienst, Frischbetontransporte und Kiestransporte."
template = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', template, count=1, flags=re.S)
template = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{description}">', template, count=1)
template = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', template, count=1)
template = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{description}">', template, count=1)
template = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{title}">', template, count=1)
template = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{description}">', template, count=1)
template = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="{REF_URL}">', template, count=1)
template = re.sub(r'<meta property="og:url" content="[^"]+">', f'<meta property="og:url" content="{REF_URL}">', template, count=1)

# The uploaded PNGs remain untouched in the repository. During the build we
# create lightweight WebP copies for the public gallery so the page stays fast.
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
    f'<div class="reference-photo"><img src="{output_path}" alt="RN Transporte im Einsatz" loading="lazy" decoding="async" fetchpriority="low"></div>'
    for _, output_path in reference_sources
)

references_main = f'''
<section class="page-hero"><div class="wrap page-hero-grid">
  <div class="eyebrow">Referenzen</div>
  <div><h1>Im Einsatz für unsere Kunden.</h1><p>Einblicke in den täglichen Einsatz von RN Transporte – von Betonpumpendienst und Frischbetonlogistik bis zu Kies- und Schüttguttransporten.</p></div>
</div></section>

<section class="references-page" aria-label="Ausgewählte Einsätze von RN Transporte">
  <div class="wrap">
    <div class="references-grid">
      <figure class="reference-item">
        <div class="reference-media"><img src="assets/leistungen/betonpumpendienst.png" alt="RN Transporte Betonpumpendienst im Baustelleneinsatz" loading="lazy" decoding="async" fetchpriority="low"></div>
        <figcaption><h2>Betonpumpendienst</h2><p>Betonförderung direkt am Einsatzort.</p></figcaption>
      </figure>

      <figure class="reference-item">
        <div class="reference-media"><img src="assets/leistungen/frischbetontransport.png" alt="RN Transporte Fahrmischer beim Frischbetontransport" loading="lazy" decoding="async" fetchpriority="low"></div>
        <figcaption><h2>Frischbetontransporte</h2><p>Fahrmischer zwischen Betonwerk und Baustelle.</p></figcaption>
      </figure>

      <figure class="reference-item">
        <div class="reference-media"><img src="assets/leistungen/Kiestransporte.png" alt="RN Transporte Kiestransport im Einsatz" loading="lazy" decoding="async" fetchpriority="low"></div>
        <figcaption><h2>Kiestransporte</h2><p>Kies und Schüttgüter zuverlässig zum Einsatzort.</p></figcaption>
      </figure>

      <figure class="reference-item">
        <div class="reference-media"><img src="assets/leistungen/Baustelleneinsatz.png" alt="RN Transporte im Baustelleneinsatz" loading="lazy" decoding="async" fetchpriority="low"></div>
        <figcaption><h2>Baustelleneinsatz</h2><p>Transport- und Betonlogistik im täglichen Einsatz.</p></figcaption>
      </figure>
    </div>

    <div class="reference-photo-grid" aria-label="Weitere Baustelleneinsätze">
      {gallery_markup}
    </div>

    <div class="page-cta references-cta">
      <p>Sie möchten Ihren nächsten Einsatz mit RN Transporte abstimmen?</p>
      <a href="kontakt.html">Projekt anfragen →</a>
    </div>
  </div>
</section>
'''.strip()

template, count = re.subn(r'<main>.*?</main>', f'<main>\n{references_main}\n</main>', template, count=1, flags=re.S)
if count != 1:
    raise SystemExit("RN references main replacement failed")

references_style = r'''<style id="rn-references-style">
.references-page{padding:72px 0 104px;background:#fff}
.references-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:64px 36px}
.reference-item{margin:0;min-width:0}
.reference-media{aspect-ratio:16/10;overflow:hidden;background:#f1f2f2}
.reference-media img{display:block;width:100%;height:100%;object-fit:cover;object-position:center;filter:saturate(.86) contrast(.99) brightness(.985);transition:transform .45s ease}
.reference-item figcaption{display:grid;grid-template-columns:minmax(0,1fr) minmax(180px,.62fr);gap:28px;padding:20px 0 0;border-top:1px solid #e0e1e2}
.reference-item h2{margin:0;color:var(--ink);font-size:clamp(24px,2.3vw,32px);line-height:1.08;letter-spacing:-.035em;font-weight:560}
.reference-item p{margin:2px 0 0;color:#707479;font-size:14px;line-height:1.62}
.reference-photo-grid{columns:3 320px;column-gap:18px;margin-top:72px}
.reference-photo{margin:0 0 18px;break-inside:avoid;overflow:hidden;background:#f1f2f2}
.reference-photo img{display:block;width:100%;height:auto;transition:transform .45s ease}
.references-cta{margin-top:72px}
@media(hover:hover){.reference-item:hover .reference-media img,.reference-photo:hover img{transform:scale(1.012)}}
@media(max-width:900px){
  .references-page{padding:46px 0 74px}
  .references-grid{grid-template-columns:1fr;gap:44px}
  .reference-media{margin:0 -16px;aspect-ratio:16/10}
  .reference-item figcaption{grid-template-columns:1fr;gap:8px;padding-top:16px}
  .reference-item h2{font-size:28px}
  .reference-item p{font-size:13px}
  .reference-photo-grid{columns:1;margin:44px -16px 0}
  .reference-photo{margin-bottom:12px}
  .references-cta{margin-top:50px}
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
