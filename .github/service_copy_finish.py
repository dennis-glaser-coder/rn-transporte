from pathlib import Path
import re


def replace_once(text: str, pattern: str, replacement: str, label: str, flags=0) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f"RN service copy target missing: {label}")
    return updated


# Keep the services overview concise, but make the value of each service clearer.
hub_path = Path("leistungen.html")
hub = hub_path.read_text(encoding="utf-8")
hub_copy = {
    "Betonpumpendienst": "Pumpeneinsätze sauber vorbereitet und auf den Baustellenablauf abgestimmt.",
    "Frischbetontransporte": "Fahrmischertransporte mit klarer Abstimmung zwischen Betonwerk und Baustelle.",
    "Kiestransporte": "Kies und Schüttgüter mit Sattelkippern – abgestimmt auf Bedarf, Zeitfenster und Einsatzort.",
}
for heading, paragraph in hub_copy.items():
    hub = replace_once(
        hub,
        rf'(<h2>{re.escape(heading)}</h2>\s*<p>).*?(</p>)',
        rf'\1{paragraph}\2',
        f"hub {heading}",
        flags=re.S,
    )
hub_path.write_text(hub, encoding="utf-8")


# Visible copy on the three service detail pages. Brand references stay in
# metadata/schema; the page itself focuses on capability, planning and outcome.
service_copy = {
    "betonpumpendienst.html": {
        "hero": "Betonpumpendienst für planbare Baustelleneinsätze.",
        "intro": "Von der Vorbereitung bis zur Betonage stimmen wir Pumpeneinsatz, Anlieferung und Baustellenablauf aufeinander ab.",
        "kicker": "Betonpumpendienst · Baustellenlogistik",
        "section": "Zuverlässig geplant. Präzise im Einsatz.",
        "paragraphs": [
            "Bei einem Pumpeneinsatz müssen Aufstellfläche, Reichweite, Betonversorgung und Ablauf zusammenpassen. Deshalb klären wir die Anforderungen vorab und stimmen den Einsatz direkt mit der Baustelle ab.",
            "Ob Bodenplatte, Decke, Wand oder schwer zugänglicher Bereich: Entscheidend ist ein sauber vorbereiteter Ablauf, damit Betonage und Pumpeneinsatz ohne unnötige Standzeiten ineinandergreifen.",
        ],
    },
    "frischbetontransporte.html": {
        "hero": "Frischbetontransporte mit verlässlichem Timing.",
        "intro": "Fahrmischer, Betonwerk und Baustelle müssen ineinandergreifen – dafür sorgen klare Zeitfenster und direkte Abstimmung.",
        "kicker": "Frischbeton · Transportlogistik",
        "section": "Verlässlich zwischen Werk und Baustelle.",
        "paragraphs": [
            "Frischbeton ist zeitkritisch. Deshalb planen wir Transporte so, dass Beladung, Fahrzeit und Verarbeitung auf der Baustelle möglichst sauber zusammenpassen.",
            "Direkte Kommunikation mit Betonwerk und Einsatzort schafft klare Abläufe – im regionalen Kerngebiet ebenso wie bei überregionalen Einsätzen.",
        ],
    },
    "kiestransporte.html": {
        "hero": "Kies- und Schüttguttransporte passend zum Baustellenablauf.",
        "intro": "Sattelkipper, klare Disposition und eine Anlieferung, die sich nach Bedarf, Zeitfenster und Einsatzort richtet.",
        "kicker": "Kies & Schüttgut · Transportlogistik",
        "section": "Flexibel disponiert. Zuverlässig geliefert.",
        "paragraphs": [
            "Wir transportieren Kies, Baustoffe und weitere Schüttgüter mit Sattelkippern zum jeweiligen Einsatzort. Mengen, Zeitfenster und Anlieferung stimmen wir passend zum Bedarf der Baustelle ab.",
            "So bleibt die Materialversorgung planbar – bei regionalen Baustellen ebenso wie bei überregionalen Transporten.",
        ],
    },
}

for filename, copy in service_copy.items():
    path = Path(filename)
    html = path.read_text(encoding="utf-8")

    html = replace_once(
        html,
        r'(<div class="eyebrow">Leistung</div><div><h1>).*?(</h1><p>).*?(</p></div></div></section>)',
        rf'\1{copy["hero"]}\2{copy["intro"]}\3',
        f"hero {filename}",
        flags=re.S,
    )
    html = replace_once(
        html,
        r'(<span class="seo-service-kicker">).*?(</span>)',
        rf'\1{copy["kicker"]}\2',
        f"kicker {filename}",
        flags=re.S,
    )
    html = replace_once(
        html,
        r'(<div class="seo-service-copy"><span class="seo-service-kicker">.*?</span><h2>).*?(</h2>)',
        rf'\1{copy["section"]}\2',
        f"section {filename}",
        flags=re.S,
    )

    paragraph_html = "".join(f'<p>{paragraph}</p>' for paragraph in copy["paragraphs"])
    html = replace_once(
        html,
        r'(<div class="seo-service-copy"><span class="seo-service-kicker">.*?</span><h2>.*?</h2>).*?(\s*<div class="seo-service-meta">)',
        rf'\1{paragraph_html}\2',
        f"body {filename}",
        flags=re.S,
    )
    if "Projekt anfragen →" not in html:
        raise SystemExit(f"RN service CTA missing: {filename}")
    html = html.replace("Projekt anfragen →", "Einsatz anfragen →", 1)

    # Guard against the old visible brand-first copy returning later.
    if '<span class="seo-service-kicker">RN Transporte · Salzkotten</span>' in html:
        raise SystemExit(f"RN old service kicker remains: {filename}")
    for marker in (copy["hero"], copy["section"], copy["paragraphs"][0], "Einsatz anfragen →"):
        if marker not in html:
            raise SystemExit(f"RN service copy verification failed in {filename}: {marker}")

    path.write_text(html, encoding="utf-8")

print("RN service copy finish passed")
