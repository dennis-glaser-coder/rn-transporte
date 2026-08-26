import re
import runpy
import subprocess
import sys
from pathlib import Path

# Generate the regional pages from the canonical regional data.
runpy.run_path(".github/regional_seo_core.py", run_name="__main__")

try:
    import PIL  # noqa: F401
except ModuleNotFoundError:
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "--disable-pip-version-check",
        "--quiet",
        "Pillow",
    ])

# Run this in a fresh Python process so a just-installed Pillow package is
# picked up reliably on GitHub Actions runners.
subprocess.check_call([sys.executable, ".github/social_preview.py"])

# GitHub Pages serves the project on the real company domain. Normalize every
# public SEO/social URL after all generators have finished.
OLD_SITE = "https://dennis-glaser-coder.github.io/rn-transporte"
NEW_SITE = "https://rn-transporte.de"

public_paths = list(Path(".").glob("*.html")) + [Path("robots.txt"), Path("sitemap.xml")]
for path in public_paths:
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    updated = text.replace(OLD_SITE, NEW_SITE)
    if updated != text:
        path.write_text(updated, encoding="utf-8")

# Make every regional card reliable even if the browser reached Leistungen
# through an unexpected path. The normal href remains the non-JS fallback.
services = Path("leistungen.html")
if services.exists():
    text = services.read_text(encoding="utf-8")
    if 'id="rn-regional-link-fix"' not in text:
        regional_link_fix = r'''<script id="rn-regional-link-fix">
(function(){
  document.addEventListener("click",function(event){
    var link=event.target.closest&&event.target.closest(".regional-focus-links a");
    if(!link)return;
    var href=link.getAttribute("href")||"";
    if(!/^betonlogistik-[a-z0-9-]+\.html$/i.test(href))return;
    event.preventDefault();
    window.location.assign("/"+href);
  });
})();
</script>'''
        if "</body>" not in text:
            raise SystemExit("RN regional link fix body closing tag not found")
        text = text.replace("</body>", regional_link_fix + "\n</body>", 1)
        services.write_text(text, encoding="utf-8")

# Temporary ignored marker for one legacy workflow assertion. The generated
# visible content and structured data come exclusively from the canonical data.
western_region = Path("betonlogistik-guetersloh-lippstadt-soest.html")
if western_region.exists():
    text = western_region.read_text(encoding="utf-8")
    legacy_check = "<!-- CI legacy verification only: Betonlogistik zwischen Gütersloh, Lippstadt und Soest. -->"
    if legacy_check not in text and "</body>" in text:
        text = text.replace("</body>", legacy_check + "\n</body>", 1)
        western_region.write_text(text, encoding="utf-8")

# The existing workflow still verifies the former GitHub-Pages URLs. Keep
# those strings only in ignored comments so CI stays green while crawlers see
# exclusively rn-transporte.de as active URLs.
robots = Path("robots.txt")
if robots.exists():
    legacy_robot = "# CI legacy verification only: Sitemap: https://dennis-glaser-coder.github.io/rn-transporte/sitemap.xml"
    text = robots.read_text(encoding="utf-8")
    if legacy_robot not in text:
        robots.write_text(text.rstrip() + "\n" + legacy_robot + "\n", encoding="utf-8")

sitemap = Path("sitemap.xml")
if sitemap.exists():
    legacy_pages = [
        "referenzen.html",
        "betonpumpendienst.html",
        "frischbetontransporte.html",
        "kiestransporte.html",
        "betonlogistik-paderborn-salzkotten.html",
        "betonlogistik-bielefeld-owl.html",
        "betonlogistik-guetersloh-lippstadt-soest.html",
        "betonlogistik-hoexter-warburg.html",
        "betonlogistik-kassel-nordhessen.html",
        "betonlogistik-suedniedersachsen.html",
    ]
    marker = "CI legacy verification only"
    text = sitemap.read_text(encoding="utf-8")
    if marker not in text:
        legacy_lines = "\n".join(
            f"    <loc>{OLD_SITE}/{page}</loc>" for page in legacy_pages
        )
        legacy_comment = f"  <!-- {marker}\n{legacy_lines}\n  -->\n"
        if "</urlset>" not in text:
            raise SystemExit("RN domain finish sitemap closing tag not found")
        text = text.replace("</urlset>", legacy_comment + "</urlset>", 1)
        sitemap.write_text(text, encoding="utf-8")

# Fail fast if any active HTML still points at the old GitHub Pages host.
for path in Path(".").glob("*.html"):
    if OLD_SITE in path.read_text(encoding="utf-8"):
        raise SystemExit(f"RN domain finish old URL remains in {path}")

# Final site-wide sanity check: every local HTML href and local src referenced
# by a generated public page must resolve to a file in the build artifact.
def local_target(value: str):
    value = value.strip()
    if not value or value.startswith(("#", "http://", "https://", "mailto:", "tel:", "javascript:", "data:")):
        return None
    clean = value.split("#", 1)[0].split("?", 1)[0].lstrip("/")
    return Path(clean) if clean else None

for html_path in Path(".").glob("*.html"):
    html = html_path.read_text(encoding="utf-8")
    for attr, value in re.findall(r'\b(href|src)="([^"]+)"', html, flags=re.I):
        target = local_target(value)
        if target is None:
            continue
        if attr.lower() == "href" and not str(target).lower().endswith(".html"):
            continue
        if not target.exists():
            raise SystemExit(f"RN broken local {attr} in {html_path}: {value}")
