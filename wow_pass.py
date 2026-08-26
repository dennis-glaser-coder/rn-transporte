from pathlib import Path

MAIN_PAGES = (
    "index.html",
    "leistungen.html",
    "referenzen.html",
    "unternehmen.html",
    "karriere.html",
    "kontakt.html",
)

wow_style = r'''<style id="rn-wow-pass">
/* RN visible premium direction: graphite first, RN red only as an accent */

/* Red is now a signal, not a text color */
.eyebrow{position:relative!important;padding-left:28px!important;color:#74797e!important}
.eyebrow:before{content:"";position:absolute;left:0;top:50%;width:17px;height:2px;background:var(--red);transform:translateY(-50%)}
.home-link-card b,.service-page-cta a,.references-cta a,.company-page-cta a{color:var(--ink)!important}

/* Strong premium signature on every inner page */
.page-hero{position:relative!important;overflow:hidden!important;background:radial-gradient(circle at 88% 4%,rgba(183,23,36,.18),transparent 26%),linear-gradient(135deg,#181a1c 0%,#222528 58%,#191b1d 100%)!important;border-bottom:0!important;box-shadow:inset 0 -1px rgba(255,255,255,.055)!important}
.page-hero:after{content:"";position:absolute;right:-8%;bottom:-52%;width:42%;aspect-ratio:1;border:1px solid rgba(255,255,255,.045);border-radius:50%;pointer-events:none}
.page-hero .eyebrow{color:#b9bdc0!important}
.page-hero h1{color:#fff!important;font-size:clamp(46px,5.45vw,78px)!important;line-height:.96!important;letter-spacing:-.061em!important}
.page-hero p{color:#b7bbbe!important;font-size:16px!important}
.page-hero-grid>div:last-child{position:relative;padding-left:42px;border-left:1px solid rgba(255,255,255,.12)}

/* Homepage: leave hero untouched, make the next section visibly editorial */
.home-overview{position:relative!important;background:#f1f1ee!important;padding-top:94px!important;padding-bottom:112px!important;box-shadow:inset 0 1px #e0e1df}
.home-overview:before{content:"";position:absolute;left:0;top:0;width:clamp(80px,12vw,190px);height:3px;background:var(--red)}
.home-overview-head{grid-template-columns:minmax(150px,.34fr) minmax(0,1.66fr)!important;gap:72px!important;margin-bottom:50px!important}
.home-overview-head h2{font-size:clamp(40px,4.4vw,63px)!important;line-height:.98!important;letter-spacing:-.058em!important;font-weight:500!important;max-width:820px!important}
.home-link-grid{display:grid!important;grid-template-columns:repeat(12,minmax(0,1fr))!important;gap:1px!important;background:#d8d9d7!important;border:0!important;box-shadow:0 28px 70px rgba(22,24,26,.055)!important}
.home-link-card{border:0!important;background:#fff!important;min-height:286px!important;padding:34px 36px!important}
.home-link-card:nth-child(1){grid-column:1/span 7}
.home-link-card:nth-child(2){grid-column:8/span 5}
.home-link-card:nth-child(3){grid-column:1/span 5;min-height:250px!important}
.home-link-card:nth-child(4){grid-column:6/span 7;min-height:250px!important;background:#1d2022!important}
.home-link-card h3{font-size:clamp(30px,3vw,42px)!important;line-height:1!important;letter-spacing:-.047em!important;font-weight:520!important}
.home-link-card p{max-width:520px!important;color:#696e72!important}
.home-link-card-dark p{color:#adb1b4!important}
.home-link-card b{font-size:11px!important;letter-spacing:.055em!important;text-transform:uppercase}
.home-link-card:before{height:3px!important}

/* Services and content blocks: less red copy, more material contrast */
.service-feature-copy .eyebrow,.company-editorial>.wrap>.eyebrow,.contact-grid>.eyebrow{color:#74797e!important}
.service-page-cta,.references-cta,.company-page-cta{background:#f0f0ed!important;border-left:3px solid var(--red)!important;box-shadow:none!important}
.service-page-cta a:hover,.references-cta a:hover,.company-page-cta a:hover{color:var(--red)!important}
.service-visual,.reference-media,.company-stage-media{outline:1px solid rgba(20,22,24,.055);outline-offset:-1px}

/* References: make the editorial layout feel more intentional */
.references-page{background:#f5f5f2!important;padding-top:92px!important}
.reference-item figcaption{padding-top:20px!important}
.reference-item h2{font-size:clamp(28px,2.7vw,39px)!important;letter-spacing:-.045em!important}
.reference-item p{font-size:13px!important;letter-spacing:.005em!important}
.reference-item:nth-child(2),.reference-item:nth-child(4){position:relative}
.reference-item:nth-child(2):before,.reference-item:nth-child(4):before{content:"";position:absolute;left:-24px;top:-34px;width:1px;height:74px;background:linear-gradient(var(--red),rgba(183,23,36,0))}

/* Company / career: calmer, more expensive-looking hierarchy */
.company-editorial .company-main h2,.career-copy strong{color:#202326!important}
.company-meta strong,.career-benefits strong{color:#202326!important}
.job-card{border-color:#d9dbdc!important;box-shadow:0 18px 46px rgba(20,22,24,.032)}
.job-card:before{background:var(--red)!important;width:54px!important}
.job-apply{color:#202326!important}

/* Contact: white type, red only in the ambient glow */
.contact-grid>.eyebrow{color:#aeb2b5!important}
.contact-grid>.eyebrow:before{background:var(--red)!important}
.contact-links a,.contact-email{color:#fff!important}

/* Active navigation is graphite with a red underline rather than red lettering */
.nav a.active{color:var(--ink)!important}
.nav a.active:after{background:var(--red)!important}

@media(hover:hover){
  .home-link-card:hover b{color:var(--red)!important}
  .nav a:hover{color:var(--ink)!important}
}

@media(max-width:900px){
  .page-hero{padding:64px 0 60px!important}
  .page-hero:after{right:-30%;bottom:-28%;width:75%}
  .page-hero-grid>div:last-child{padding-left:0;border-left:0}
  .page-hero h1{font-size:clamp(42px,11vw,56px)!important;line-height:.98!important}
  .page-hero p{font-size:15px!important}
  .eyebrow{padding-left:24px!important}
  .eyebrow:before{width:14px}
  .home-overview{padding-top:72px!important;padding-bottom:82px!important}
  .home-overview-head{grid-template-columns:1fr!important;gap:17px!important;margin-bottom:34px!important}
  .home-overview-head h2{font-size:clamp(36px,9.6vw,47px)!important}
  .home-link-grid{grid-template-columns:1fr!important;gap:1px!important}
  .home-link-card:nth-child(n){grid-column:1/-1!important;min-height:218px!important;padding:28px 25px!important}
  .home-link-card h3{font-size:31px!important}
  .references-page{padding-top:54px!important}
  .reference-item:nth-child(2):before,.reference-item:nth-child(4):before{display:none}
  header.open .nav a.active{color:var(--ink)!important;border-left:2px solid var(--red)!important;padding-left:14px!important}
}
</style>'''

for filename in MAIN_PAGES:
    path = Path(filename)
    html = path.read_text(encoding="utf-8")
    if 'id="rn-wow-pass"' in html:
        raise SystemExit(f"RN wow pass already present: {filename}")
    html = html.replace("</head>", wow_style + "\n</head>", 1)
    if 'id="rn-wow-pass"' not in html:
        raise SystemExit(f"RN wow pass insertion failed: {filename}")
    path.write_text(html, encoding="utf-8")
