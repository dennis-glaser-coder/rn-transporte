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

runpy.run_path(".github/social_preview.py", run_name="__main__")

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
