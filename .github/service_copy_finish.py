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


# Sharpen the career page in the same tone: concrete work, clear expectations
# and confirmed employer facts instead of generic recruiting phrases.
career_path = Path("karriere.html")
career = career_path.read_text(encoding="utf-8")

career_hero = "Arbeiten im Fahrbetrieb und auf der Baustelle."
career_intro = (
    "Betonpumpe, Fahrmischer, Kipper oder Sattelzug: Wir suchen Menschen, die zuverlässig arbeiten, "
    "Verantwortung übernehmen und wissen, worauf es im täglichen Einsatz ankommt."
)
career = replace_once(
    career,
    r'(<div class="eyebrow">Karriere</div><div><h1>).*?(</h1><p>).*?(</p></div></div></section>)',
    rf'\1{career_hero}\2{career_intro}\3',
    "career hero",
    flags=re.S,
)

career_head = (
    '<div class="career-copy"><strong>Was im Alltag zählt.</strong>'
    'Klare Absprachen, ein sicherer Umgang mit Fahrzeug und Technik und Kollegen, die sich aufeinander verlassen können. '
    'Wer sauber arbeitet und Verantwortung übernimmt, passt zu uns.</div><div class="career-note">'
)
career = replace_once(
    career,
    r'<div class="career-copy"><strong>.*?</strong>.*?</div><div class="career-note">',
    career_head,
    "career introduction",
    flags=re.S,
)

pump_text = (
    "Du bedienst unsere Betonpumpen auf Baustellen, bereitest den Einsatz sicher vor und stimmst dich vor Ort mit "
    "Baustelle und Betonversorgung ab. Technisches Verständnis und ein verantwortungsvoller Umgang mit Maschine und "
    "Fahrzeug gehören dabei dazu."
)
career = replace_once(
    career,
    r'(<article class="job-card" id="pumpenfahrer"><h3>Pumpenfahrer / Betonpumpenmaschinist \(m/w/d\)</h3><p>).*?(</p>)',
    rf'\1{pump_text}\2',
    "pump driver copy",
    flags=re.S,
)

driver_text = (
    "Du bist mit Fahrmischer, Kipper oder Sattelzug unterwegs und übernimmst Beton- und Baustofftransporte. Dabei zählen "
    "ein sicherer Umgang mit dem Fahrzeug, zuverlässige Abläufe und die direkte Abstimmung beim Einsatz."
)
career = replace_once(
    career,
    r'(<article class="job-card" id="berufskraftfahrer"><h3>Berufskraftfahrer \(m/w/d\) – Fahrmischer / Kipper / Sattelzug</h3><p>).*?(</p>)',
    rf'\1{driver_text}\2',
    "professional driver copy",
    flags=re.S,
)
career = career.replace(
    "<li>Motivierte und verantwortungsbewusste Arbeitsweise</li>",
    "<li>Verantwortungsbewusste und zuverlässige Arbeitsweise</li>",
    1,
)

benefits = (
    '<div class="career-benefits">'
    '<span><strong>Unbefristet</strong> in Vollzeit</span>'
    '<span><strong>Ganzjährig</strong> beschäftigt</span>'
    '<span><strong>Kurze Wege</strong> im Unternehmen</span>'
    '<span><strong>Fortbildung</strong> möglich</span>'
    '</div>'
)
career = replace_once(
    career,
    r'<div class="career-benefits">.*?</div>',
    benefits,
    "career benefits",
    flags=re.S,
)

# Keep the JobPosting descriptions aligned with the visible page copy.
career = career.replace(
    "Betonpumpen auf Baustellen bedienen, sicheren Aufbau gewährleisten und den Einsatz vor Ort koordinieren. Technisches Verständnis und zuverlässige Arbeitsweise sind erforderlich; Erfahrung mit Betonpumpen ist ideal. Ganzjährige Beschäftigung und Fortbildungsmöglichkeiten.",
    "Betonpumpen auf Baustellen bedienen, den Einsatz sicher vorbereiten und sich vor Ort mit Baustelle und Betonversorgung abstimmen. Technisches Verständnis und ein verantwortungsvoller Umgang mit Maschine und Fahrzeug sind wichtig. Ganzjährige Beschäftigung und Fortbildungsmöglichkeiten.",
    1,
)
career = career.replace(
    "Beton- und Baustofftransporte mit Fahrmischer, Kipper oder Sattelzug. Erforderlich sind Führerschein CE mit gültiger Schlüsselzahl 95 sowie eine motivierte und verantwortungsbewusste Arbeitsweise. Ganzjährige Beschäftigung und Fortbildungsmöglichkeiten.",
    "Beton- und Baustofftransporte mit Fahrmischer, Kipper oder Sattelzug. Erforderlich sind Führerschein CE mit gültiger Schlüsselzahl 95 sowie eine verantwortungsbewusste und zuverlässige Arbeitsweise. Ganzjährige Beschäftigung und Fortbildungsmöglichkeiten.",
    1,
)

for marker in (
    career_hero,
    "Was im Alltag zählt.",
    pump_text,
    driver_text,
    "<strong>Unbefristet</strong> in Vollzeit",
    '"@type":"JobPosting"',
):
    if marker not in career:
        raise SystemExit(f"RN career copy verification failed: {marker}")
if "Faire Vergütung" in career or "über dem Durchschnitt" in career:
    raise SystemExit("RN unconfirmed career salary claim remains")

career_path.write_text(career, encoding="utf-8")

print("RN service and career copy finish passed")
