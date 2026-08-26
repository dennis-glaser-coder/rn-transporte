from pathlib import Path
import os
import re
from PIL import Image, ImageDraw, ImageFont

SITE_URL = "https://dennis-glaser-coder.github.io/rn-transporte/"
PREVIEW_REL = "assets/rn-social-preview.jpg"
PREVIEW_URL = SITE_URL + PREVIEW_REL

W, H = 1200, 630
hero_path = Path("rn_hero_final.png")
logo_path = Path("assets/logo.webp")
out_path = Path(PREVIEW_REL)
out_path.parent.mkdir(parents=True, exist_ok=True)

if not hero_path.exists() or not logo_path.exists():
    raise SystemExit("RN social preview source assets missing")

# Original hero only: crop to 1200x630, no image regeneration or subject edits.
hero = Image.open(hero_path).convert("RGB")
target_ratio = W / H
src_ratio = hero.width / hero.height
if src_ratio > target_ratio:
    new_w = int(hero.height * target_ratio)
    left = (hero.width - new_w) // 2
    hero = hero.crop((left, 0, left + new_w, hero.height))
else:
    new_h = int(hero.width / target_ratio)
    top = max(0, min(hero.height - new_h, int((hero.height - new_h) * 0.35)))
    hero = hero.crop((0, top, hero.width, top + new_h))
hero = hero.resize((W, H), Image.Resampling.LANCZOS)
canvas = hero.convert("RGBA")

# Dark editorial gradient on the left for reliable preview readability.
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
px = overlay.load()
for x in range(W):
    t = x / W
    if t <= 0.18:
        alpha = 205
    elif t <= 0.72:
        u = (t - 0.18) / (0.72 - 0.18)
        alpha = int(205 * (1 - u) ** 1.55)
    else:
        alpha = 0
    for y in range(H):
        extra = int(24 * (y / H) ** 2)
        px[x, y] = (8, 10, 12, min(225, alpha + extra))
canvas = Image.alpha_composite(canvas, overlay)
draw = ImageDraw.Draw(canvas)

# Exact original RN logo, scaled proportionally only.
logo = Image.open(logo_path).convert("RGB")
logo_w = 390
logo_h = round(logo.height * logo_w / logo.width)
logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
panel_pad_x, panel_pad_y = 17, 13
panel_x, panel_y = 62, 54
panel_w, panel_h = logo_w + panel_pad_x * 2, logo_h + panel_pad_y * 2
draw.rounded_rectangle(
    (panel_x, panel_y, panel_x + panel_w, panel_y + panel_h),
    radius=3,
    fill=(255, 255, 255, 247),
)
canvas.paste(logo, (panel_x + panel_pad_x, panel_y + panel_pad_y))

bold_candidates = [
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
regular_candidates = [
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
bold_path = next((p for p in bold_candidates if os.path.exists(p)), None)
regular_path = next((p for p in regular_candidates if os.path.exists(p)), None)
if not bold_path or not regular_path:
    raise SystemExit("RN social preview fonts unavailable")

title_font = ImageFont.truetype(bold_path, 63)
sub_font = ImageFont.truetype(regular_path, 24)
small_font = ImageFont.truetype(bold_path, 13)
red = (183, 23, 36, 255)
left = 64

kicker_y = 236
draw.rectangle((left, kicker_y, left + 44, kicker_y + 3), fill=red)
draw.text((left + 60, kicker_y - 8), "RN TORWESTEN TRANSPORTE", font=small_font, fill=(240, 240, 240, 235))

title_y = 279
draw.text((left, title_y), "BETONLOGISTIK", font=title_font, fill=(255, 255, 255, 255))
draw.text((left, title_y + 67), "& TRANSPORT", font=title_font, fill=(255, 255, 255, 255))

draw.text(
    (left, 472),
    "Salzkotten  ·  regional stark  ·  bundesweit im Einsatz",
    font=sub_font,
    fill=(228, 230, 232, 245),
)
draw.rectangle((left, 538, left + 96, 541), fill=red)
canvas.convert("RGB").save(out_path, quality=91, optimize=True, progressive=True)

if Image.open(out_path).size != (W, H):
    raise SystemExit("RN social preview dimensions invalid")

PUBLIC_PAGES = [
    "index.html",
    "leistungen.html",
    "referenzen.html",
    "unternehmen.html",
    "karriere.html",
    "kontakt.html",
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

extra_meta = (
    f'<meta property="og:image:width" content="{W}">\n'
    f'<meta property="og:image:height" content="{H}">\n'
    '<meta property="og:image:type" content="image/jpeg">\n'
    '<meta property="og:image:alt" content="RN Torwesten Transporte – Betonlogistik und Transport">\n'
    '<meta name="twitter:image:alt" content="RN Torwesten Transporte – Betonlogistik und Transport">'
)

for filename in PUBLIC_PAGES:
    path = Path(filename)
    if not path.exists():
        raise SystemExit(f"RN social preview page missing: {filename}")
    html = path.read_text(encoding="utf-8")

    html, og_count = re.subn(
        r'<meta property="og:image" content="[^"]*">',
        f'<meta property="og:image" content="{PREVIEW_URL}">',
        html,
        count=1,
    )
    html, tw_count = re.subn(
        r'<meta name="twitter:image" content="[^"]*">',
        f'<meta name="twitter:image" content="{PREVIEW_URL}">',
        html,
        count=1,
    )
    if og_count != 1 or tw_count != 1:
        raise SystemExit(f"RN social image metadata not found exactly once: {filename}")

    # Replace any existing image-alt tag from the old hero and normalize metadata.
    html = re.sub(r'\n?<meta property="og:image:alt" content="[^"]*">', '', html)
    html = re.sub(r'\n?<meta property="og:image:width" content="[^"]*">', '', html)
    html = re.sub(r'\n?<meta property="og:image:height" content="[^"]*">', '', html)
    html = re.sub(r'\n?<meta property="og:image:type" content="[^"]*">', '', html)
    html = re.sub(r'\n?<meta name="twitter:image:alt" content="[^"]*">', '', html)
    marker = f'<meta property="og:image" content="{PREVIEW_URL}">'
    html = html.replace(marker, marker + "\n" + extra_meta, 1)

    if html.count(PREVIEW_URL) != 2:
        raise SystemExit(f"RN social preview URL count invalid: {filename}")
    path.write_text(html, encoding="utf-8")

print(f"RN social preview generated: {out_path} ({W}x{H})")
print(f"RN social preview metadata applied to {len(PUBLIC_PAGES)} public pages")
