from datetime import date
from pathlib import Path
from urllib.parse import quote
import html, json, re

SITE='https://rn-transporte.de/'
POSTED='2026-09-11'
TODAY=date.today().isoformat()
career_path=Path('karriere.html')
career=career_path.read_text(encoding='utf-8')

career,n=re.subn(r'\s*<script type="application/ld\+json">(?:(?!</script>).)*"@type":"JobPosting"(?:(?!</script>).)*</script>','',career,count=1,flags=re.S)
if n!=1: raise SystemExit('career JobPosting graph missing')

style='''<style id="rn-job-pages">.job-detail-link{display:inline-flex;margin:14px 0 4px;color:#25282b;font-size:11px;font-weight:780;text-transform:uppercase;border-bottom:1px solid #c7c9ca;padding-bottom:5px}.rn-job-hero{padding:70px 0 58px;border-bottom:1px solid #e2e3e3}.rn-job-hero .wrap,.rn-job-grid{display:grid;grid-template-columns:.42fr 1.58fr;gap:64px}.rn-job-kicker{font-size:10px;font-weight:780;letter-spacing:.15em;text-transform:uppercase;color:#777}.rn-job-hero h1{margin:0;font-size:clamp(42px,5vw,70px);line-height:1;letter-spacing:-.05em;font-weight:520}.rn-job-hero p{max-width:720px;color:#62676b;line-height:1.7}.rn-job-facts{display:flex;flex-wrap:wrap;gap:8px;margin-top:24px}.rn-job-facts span{padding:8px 10px;background:#f1f1ef;font-size:10px;font-weight:760;text-transform:uppercase}.rn-job-content{padding:72px 0 94px}.rn-job-grid{grid-template-columns:minmax(0,1.1fr) minmax(300px,.7fr);align-items:start}.rn-job-copy h2{margin:0 0 16px;font-size:30px}.rn-job-copy h2:not(:first-child){margin-top:42px}.rn-job-copy li{color:#5e6367;line-height:1.7;margin:7px 0}.rn-job-side{position:sticky;top:100px;padding:28px;background:#1d2023;color:#fff}.rn-job-side h2{margin:0}.rn-job-side p{color:#c2c4c6;line-height:1.6}.rn-job-apply{display:flex;justify-content:space-between;align-items:center;margin-top:22px;min-height:52px;padding:0 16px;background:var(--red);color:#fff;font-weight:780}.rn-job-phone{display:block;margin-top:15px;color:#fff}.rn-job-back{display:inline-block;margin-top:28px;color:#555}.rn-job-media{margin-top:38px}.rn-job-media img{width:100%;aspect-ratio:16/9;object-fit:cover}@media(max-width:900px){.rn-job-hero .wrap,.rn-job-grid{grid-template-columns:1fr;gap:26px}.rn-job-hero{padding:52px 0 46px}.rn-job-hero h1{font-size:42px}.rn-job-content{padding:52px 0 70px}.rn-job-side{position:static}}</style>'''
career=career.replace('</head>',style+'\n</head>',1)

links={
'<h3>Pumpenfahrer / Betonpumpenmaschinist (m/w/d)</h3>':'<h3>Pumpenfahrer / Betonpumpenmaschinist (m/w/d)</h3><a class="job-detail-link" href="pumpenfahrer-betonpumpenmaschinist.html">Stelle im Detail ansehen →</a>',
'<h3>Berufskraftfahrer (m/w/d) – Fahrmischer / Kipper / Sattelzug</h3>':'<h3>Berufskraftfahrer (m/w/d) – Fahrmischer / Kipper / Sattelzug</h3><a class="job-detail-link" href="berufskraftfahrer-fahrmischer-kipper.html">Stelle im Detail ansehen →</a>'}
for old,new in links.items():
    if old not in career: raise SystemExit('career job heading missing')
    career=career.replace(old,new,1)
career_path.write_text(career,encoding='utf-8')

jobs=[
 dict(file='pumpenfahrer-betonpumpenmaschinist.html',code='RN-PUMP-2026-01',title='Pumpenfahrer / Betonpumpenmaschinist (m/w/d)',seo='Pumpenfahrer / Betonpumpenmaschinist (m/w/d) | RN Transporte',intro='Verstärke RN Transporte im Betonpumpendienst – Vollzeit, unbefristet und mit direkter Bewerbung.',facts=['Vollzeit','unbefristet','Salzkotten','C/CE','ganzjährig'],img='assets/leistungen/betonpumpendienst.png',wa='Hallo RN Transporte, ich interessiere mich für die Stelle als Pumpenfahrer / Betonpumpenmaschinist.',tasks=['Betonpumpen auf Baustellen sicher bedienen und aufbauen.','Einsätze vor Ort mit Baustelle und Team abstimmen.','Fahrzeug und Technik zuverlässig im Blick behalten.'],req=['Führerschein C/CE.','Technisches Verständnis und zuverlässige Arbeitsweise.','Erfahrung mit Betonpumpen ist ideal; Einarbeitung nach Absprache möglich.'],benefits=['Vollzeit und unbefristete Beschäftigung.','Ganzjährige Arbeit.','Familiäres, inhabergeführtes Unternehmen mit kurzen Wegen.','Fortbildungsmöglichkeiten.']),
 dict(file='berufskraftfahrer-fahrmischer-kipper.html',code='RN-DRIVER-2026-01',title='Berufskraftfahrer (m/w/d) – Fahrmischer / Kipper / Sattelzug',seo='Berufskraftfahrer C/CE – Fahrmischer & Kipper (m/w/d) | RN Transporte',intro='RN Transporte sucht Verstärkung für Fahrmischer, Kipper und Sattelzug – Vollzeit und unbefristet.',facts=['Vollzeit','unbefristet','Salzkotten','C/CE + 95','Fahrmischer / Kipper'],img='assets/leistungen/frischbetontransport.png',wa='Hallo RN Transporte, ich interessiere mich für die Stelle als Berufskraftfahrer C/CE.',tasks=['Frischbeton- und Baustofftransporte zuverlässig durchführen.','Fahrmischer, Kipper oder Sattelzug sicher führen.','Einsätze direkt mit Team, Betonwerk und Baustelle abstimmen.'],req=['Führerschein C/CE mit gültiger Schlüsselzahl 95.','Verantwortungsbewusste und zuverlässige Arbeitsweise.','Erfahrung mit Fahrmischer oder Kipper ist willkommen.'],benefits=['Vollzeit und unbefristete Beschäftigung.','Ganzjährige Arbeit.','Familiäres, inhabergeführtes Unternehmen.','Kurze Entscheidungswege und Fortbildungsmöglichkeiten.'])]

def sub1(text,pat,repl):
    out,n=re.subn(pat,repl,text,count=1,flags=re.S)
    if n!=1: raise SystemExit('job template replacement failed')
    return out

for j in jobs:
    p=career
    desc=f"{j['title']} bei RN Transporte in Salzkotten. Vollzeit, unbefristet und direkte Bewerbung per WhatsApp oder Telefon."
    url=SITE+j['file']
    p=sub1(p,r'<title>.*?</title>',f'<title>{html.escape(j["seo"])}</title>')
    p=sub1(p,r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{html.escape(desc,quote=True)}">')
    p=sub1(p,r'<meta property="og:title" content="[^"]*">',f'<meta property="og:title" content="{html.escape(j["seo"],quote=True)}">')
    p=sub1(p,r'<meta property="og:description" content="[^"]*">',f'<meta property="og:description" content="{html.escape(desc,quote=True)}">')
    p=sub1(p,r'<meta name="twitter:title" content="[^"]*">',f'<meta name="twitter:title" content="{html.escape(j["seo"],quote=True)}">')
    p=sub1(p,r'<meta name="twitter:description" content="[^"]*">',f'<meta name="twitter:description" content="{html.escape(desc,quote=True)}">')
    p=sub1(p,r'<link rel="canonical" href="[^"]+">',f'<link rel="canonical" href="{url}">')
    p=sub1(p,r'<meta property="og:url" content="[^"]+">',f'<meta property="og:url" content="{url}">')
    facts=''.join(f'<span>{html.escape(x)}</span>' for x in j['facts'])
    li=lambda xs:''.join(f'<li>{html.escape(x)}</li>' for x in xs)
    wa='https://wa.me/491737275165?text='+quote(j['wa'])
    main=f'''<main><section class="rn-job-hero"><div class="wrap"><div class="rn-job-kicker">Karriere bei RN Transporte</div><div><h1>{html.escape(j['title'])}</h1><p>{html.escape(j['intro'])}</p><div class="rn-job-facts">{facts}</div></div></div></section><section class="rn-job-content"><div class="wrap rn-job-grid"><div class="rn-job-copy"><h2>Deine Aufgaben</h2><ul>{li(j['tasks'])}</ul><h2>Das bringst du mit</h2><ul>{li(j['req'])}</ul><h2>Das bekommst du bei RN</h2><ul>{li(j['benefits'])}</ul><div class="rn-job-media"><img src="{j['img']}" alt="RN Transporte im Einsatz" loading="lazy"></div><a class="rn-job-back" href="karriere.html">← Alle Stellen bei RN Transporte</a></div><aside class="rn-job-side"><h2>Direkt bewerben.</h2><p>Kein kompliziertes Bewerbungsportal. Schreib kurz per WhatsApp oder ruf direkt an.</p><a class="rn-job-apply" href="{wa}" target="_blank" rel="noopener"><span>Per WhatsApp bewerben</span><span>→</span></a><a class="rn-job-phone" href="tel:+491737275165">0173 72 75 165</a></aside></div></section></main>'''
    p=sub1(p,r'<main>.*?</main>',main)
    schema={'@context':'https://schema.org','@type':'JobPosting','identifier':{'@type':'PropertyValue','name':'RN Transporte','value':j['code']},'title':j['title'],'description':f"<p>{desc}</p><p>Aufgaben: {' '.join(j['tasks'])}</p><p>Anforderungen: {' '.join(j['req'])}</p><p>Wir bieten: {' '.join(j['benefits'])}</p>",'datePosted':POSTED,'employmentType':'FULL_TIME','directApply':True,'hiringOrganization':{'@type':'Organization','name':'RN Transporte','sameAs':SITE,'logo':SITE+'assets/logo.webp'},'jobLocation':{'@type':'Place','address':{'@type':'PostalAddress','streetAddress':'Lohweg 55a','addressLocality':'Salzkotten','addressRegion':'Nordrhein-Westfalen','postalCode':'33154','addressCountry':'DE'}},'url':url}
    p=p.replace('</head>','<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False,separators=(',',':'))+'</script>\n</head>',1)
    Path(j['file']).write_text(p,encoding='utf-8')

s=Path('sitemap.xml').read_text(encoding='utf-8')
entries=[]
for j in jobs:
    u=SITE+j['file']
    if f'<loc>{u}</loc>' not in s: entries.append(f'  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>')
if entries: s=s.replace('</urlset>','\n'+'\n'.join(entries)+'\n</urlset>',1)
Path('sitemap.xml').write_text(s,encoding='utf-8')

if '"@type":"JobPosting"' in career_path.read_text(encoding='utf-8'): raise SystemExit('career hub still has JobPosting')
for j in jobs:
    t=Path(j['file']).read_text(encoding='utf-8')
    for x in ('"@type":"JobPosting"','"employmentType":"FULL_TIME"','"directApply":true','"addressLocality":"Salzkotten"','Per WhatsApp bewerben',SITE+j['file'],'src="/rn-analytics.js?v=1"'):
        if x not in t: raise SystemExit(f'job verification failed: {j["file"]} {x}')
print('RN dedicated job pages applied')
