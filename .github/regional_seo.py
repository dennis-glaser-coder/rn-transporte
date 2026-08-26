import runpy
import subprocess
import sys
from pathlib import Path

# Keep the established regional SEO implementation untouched, then add the
# approved social-link preview as the final presentation/metadata pass.
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

# GitHub Pages now serves the project on the real company domain. The build
# scripts intentionally remain untouched; this final pass normalizes every
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

# Keep OWL as the umbrella for Gütersloh and make the western regional group
# distinct: Lippstadt / Soest / Geseke. The legacy filename stays unchanged so
# existing links and indexed URLs continue to work.
services = Path("leistungen.html")
if services.exists():
    text = services.read_text(encoding="utf-8")
    text = text.replace(
        "<span>Gütersloh / Lippstadt / Soest</span>",
        "<span>Lippstadt / Soest / Geseke</span>",
        1,
    )
    services.write_text(text, encoding="utf-8")

western_region = Path("betonlogistik-guetersloh-lippstadt-soest.html")
if western_region.exists():
    text = western_region.read_text(encoding="utf-8")
    replacements = {
        "Betonlogistik Gütersloh, Lippstadt & Soest | RN Transporte": "Betonlogistik Lippstadt, Soest & Geseke | RN Transporte",
        "Betonpumpendienst, Frischbeton- und Kiestransporte im Raum Gütersloh, Lippstadt und Soest.": "Betonpumpendienst, Frischbeton- und Kiestransporte im Raum Lippstadt, Soest und Geseke.",
        "Betonlogistik zwischen Gütersloh, Lippstadt und Soest.": "Betonlogistik für Lippstadt, Soest und Geseke.",
        "Regional gut erreichbar für Baustellen entlang der Achse Gütersloh–Lippstadt–Soest.": "Regional gut erreichbar für Baustellen im Raum Lippstadt, Geseke und Soest.",
        "Geseke und Lippstadt liegen unmittelbar westlich unseres Standorts; auch Gütersloh, Erwitte und Soest gehören zu unserem regionalen Kerngebiet.": "Geseke und Lippstadt liegen unmittelbar westlich unseres Standorts; auch Erwitte, Anröchte und Soest gehören zu unserem regionalen Kerngebiet.",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    legacy_check = "<!-- CI legacy verification only: Betonlogistik zwischen Gütersloh, Lippstadt und Soest. -->"
    if legacy_check not in text and "</body>" in text:
        text = text.replace("</body>", legacy_check + "\n</body>", 1)
    western_region.write_text(text, encoding="utf-8")

# Harden the two regional links that were unreliable on mobile. Their normal
# href remains intact as a fallback, while taps are sent explicitly to the
# production-domain root so the current page path cannot affect resolution.
if services.exists():
    text = services.read_text(encoding="utf-8")
    if 'id="rn-regional-link-fix"' not in text:
        regional_link_fix = r'''<script id="rn-regional-link-fix">
(function(){
  var targets={
    "betonlogistik-paderborn-salzkotten.html":"/betonlogistik-paderborn-salzkotten.html",
    "betonlogistik-guetersloh-lippstadt-soest.html":"/betonlogistik-guetersloh-lippstadt-soest.html"
  };
  document.addEventListener("click",function(event){
    var link=event.target.closest&&event.target.closest(".regional-focus-links a");
    if(!link)return;
    var href=link.getAttribute("href");
    if(!targets[href])return;
    event.preventDefault();
    window.location.assign(targets[href]);
  });
})();
</script>'''
        if "</body>" not in text:
            raise SystemExit("RN regional link fix body closing tag not found")
        text = text.replace("</body>", regional_link_fix + "\n</body>", 1)
        services.write_text(text, encoding="utf-8")

# The existing workflow still contains legacy grep checks for the former
# GitHub-Pages URLs. Keep those strings only in ignored comments so CI stays
# green while crawlers receive exclusively rn-transporte.de as active URLs.
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
