from pathlib import Path
from datetime import date
import re
import subprocess
import sys

try:
    from PIL import Image, ImageOps
except ImportError:
    vendor = Path("/tmp/rn-pillow")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--disable-pip-version-check", "--target", str(vendor), "Pillow"],
        check=True,
    )
    sys.path.insert(0, str(vendor))
    from PIL import Image, ImageOps

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

# Keep the uploaded originals untouched and generate lightweight WebP copies
# for the public gallery. EXIF orientation is applied before resizing so phone
# photos display correctly. Width/height are written into the HTML to avoid
# layout shifts while the images load.
reference_sources = [
    "assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_31_59.png",
    "assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_32_07.png",
    "assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_32_16.png",
    "assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_32_24.png",
    "assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_32_33.png",
    "assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_32_39.png",
    "assets/referenzen/ChatGPT Image 28. Aug. 2026, 08_32_46.png",
    "assets/referenzen/7e5c5e11-acb7-47c6-abb1-0507f30b8405.jpeg",
    "assets/referenzen/IMG_0894.png",
]

reference_outputs = []
for source_path in reference_sources:
    source = Path(source_path)
    if not source.is_file():
        raise SystemExit(f"Missing reference image: {source_path}")

    output = source.with_suffix(".webp")
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGB")
        image.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
        width, height = image.size
        image.save(output, "WEBP", quality=80, method=6)

    reference_outputs.append((output.as_posix(), width, height))

gallery_items = []
for index, (output_path, width, height) in enumerate(reference_outputs):
    # The first two images are initially visible on desktop. Load those
    # immediately; everything below the fold stays lazy-loaded.
    loading = "eager" if index < 2 else "lazy"
    priority = "high" if index == 0 else ("auto" if index == 1 else "low")
    gallery_items.append(
        f'''<button class="reference-photo" type="button" data-lightbox-src="{output_path}" aria-label="Baustelleneinsatz vergrößern">
      <img src="{output_path}" alt="RN Transporte Baustelleneinsatz" width="{width}" height="{height}" loading="{loading}" decoding="async" fetchpriority="{priority}">
    </button>'''
    )

gallery_markup = "\n".join(gallery_items)

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

<div class="reference-lightbox" id="reference-lightbox" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Vergrößerte Referenzansicht">
  <button class="reference-lightbox-close" type="button" aria-label="Ansicht schließen">×</button>
  <button class="reference-lightbox-nav reference-lightbox-prev" type="button" aria-label="Vorheriges Bild">‹</button>
  <div class="reference-lightbox-stage"><img src="" alt="RN Transporte Baustelleneinsatz vergrößert"></div>
  <button class="reference-lightbox-nav reference-lightbox-next" type="button" aria-label="Nächstes Bild">›</button>
</div>
'''.strip()

template, count = re.subn(r'<main>.*?</main>', f'<main>\n{references_main}\n</main>', template, count=1, flags=re.S)
if count != 1:
    raise SystemExit("RN references main replacement failed")

references_style = r'''<style id="rn-references-style">
.reference-hero{padding-bottom:42px}
.references-page{padding:0 0 104px;background:#fff}
.reference-photo-grid{columns:2 430px;column-gap:24px}
.reference-photo{display:block;width:100%;padding:0;border:0;margin:0 0 24px;break-inside:avoid;overflow:hidden;background:#f1f2f2;cursor:zoom-in;text-align:left}
.reference-photo img{display:block;width:100%;height:auto;transition:transform .45s ease,filter .45s ease}
.reference-lightbox{position:fixed;inset:0;z-index:9999;display:flex;align-items:center;justify-content:center;background:rgba(12,14,16,.94);opacity:0;visibility:hidden;transition:opacity .22s ease,visibility .22s ease}
.reference-lightbox.is-open{opacity:1;visibility:visible}
.reference-lightbox-stage{display:flex;align-items:center;justify-content:center;width:min(88vw,1500px);height:88vh;padding:24px}
.reference-lightbox-stage img{display:block;max-width:100%;max-height:100%;object-fit:contain;box-shadow:0 24px 70px rgba(0,0,0,.28)}
.reference-lightbox-close,.reference-lightbox-nav{position:absolute;border:0;background:transparent;color:#fff;font-family:Arial,sans-serif;font-weight:300;cursor:pointer;opacity:.76;transition:opacity .2s ease,transform .2s ease}
.reference-lightbox-close{top:20px;right:24px;font-size:38px;line-height:1;padding:8px 12px}
.reference-lightbox-nav{top:50%;transform:translateY(-50%);font-size:56px;line-height:1;padding:22px 18px}
.reference-lightbox-prev{left:16px}.reference-lightbox-next{right:16px}
.reference-lightbox-close:hover,.reference-lightbox-nav:hover{opacity:1}
.reference-lightbox-nav:hover{transform:translateY(-50%) scale(1.04)}
body.reference-lightbox-open{overflow:hidden}
@media(hover:hover){.reference-photo:hover img{transform:scale(1.012);filter:brightness(.96)}}
@media(max-width:900px){
  .reference-hero{padding-bottom:28px}
  .references-page{padding:0 0 74px}
  .reference-photo-grid{columns:1;margin:0 -16px}
  .reference-photo{margin-bottom:12px}
  .reference-lightbox-stage{width:100vw;height:86vh;padding:54px 12px 28px}
  .reference-lightbox-close{top:10px;right:10px;font-size:34px}
  .reference-lightbox-nav{font-size:44px;padding:18px 10px}
  .reference-lightbox-prev{left:0}.reference-lightbox-next{right:0}
}
@media(prefers-reduced-motion:reduce){.reference-photo img,.reference-lightbox,.reference-lightbox-close,.reference-lightbox-nav{transition:none}}
</style>'''

template = template.replace("</head>", references_style + "\n</head>", 1)

lightbox_script = r'''<script id="rn-reference-lightbox">
(() => {
  const items = Array.from(document.querySelectorAll('.reference-photo[data-lightbox-src]'));
  const lightbox = document.getElementById('reference-lightbox');
  if (!items.length || !lightbox) return;

  const image = lightbox.querySelector('.reference-lightbox-stage img');
  const closeButton = lightbox.querySelector('.reference-lightbox-close');
  const prevButton = lightbox.querySelector('.reference-lightbox-prev');
  const nextButton = lightbox.querySelector('.reference-lightbox-next');
  let activeIndex = 0;
  let lastTrigger = null;

  const show = (index) => {
    activeIndex = (index + items.length) % items.length;
    image.src = items[activeIndex].dataset.lightboxSrc;
  };

  const open = (index, trigger) => {
    lastTrigger = trigger;
    show(index);
    lightbox.classList.add('is-open');
    lightbox.setAttribute('aria-hidden', 'false');
    document.body.classList.add('reference-lightbox-open');
    closeButton.focus();
  };

  const close = () => {
    lightbox.classList.remove('is-open');
    lightbox.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('reference-lightbox-open');
    image.removeAttribute('src');
    if (lastTrigger) lastTrigger.focus();
  };

  items.forEach((item, index) => item.addEventListener('click', () => open(index, item)));
  closeButton.addEventListener('click', close);
  prevButton.addEventListener('click', () => show(activeIndex - 1));
  nextButton.addEventListener('click', () => show(activeIndex + 1));
  lightbox.addEventListener('click', (event) => { if (event.target === lightbox) close(); });

  document.addEventListener('keydown', (event) => {
    if (!lightbox.classList.contains('is-open')) return;
    if (event.key === 'Escape') close();
    if (event.key === 'ArrowLeft') show(activeIndex - 1);
    if (event.key === 'ArrowRight') show(activeIndex + 1);
  });
})();
</script>'''

template = template.replace("</body>", lightbox_script + "\n</body>", 1)
Path("referenzen.html").write_text(template, encoding="utf-8")

# Add the new page to the sitemap without disturbing the generated entries.
sitemap_path = Path("sitemap.xml")
sitemap = sitemap_path.read_text(encoding="utf-8")
if REF_URL not in sitemap:
    entry = f"  <url>\n    <loc>{REF_URL}</loc>\n    <lastmod>{date.today().isoformat()}</lastmod>\n  </url>\n"
    sitemap = sitemap.replace("</urlset>", entry + "</urlset>", 1)
    sitemap_path.write_text(sitemap, encoding="utf-8")
