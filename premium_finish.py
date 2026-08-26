from pathlib import Path

MAIN_PAGES = (
    "index.html",
    "leistungen.html",
    "referenzen.html",
    "unternehmen.html",
    "karriere.html",
    "kontakt.html",
)

finish_style = r'''<style id="rn-premium-finish">
/* Final visible RN premium layer: stronger composition, still restrained */

/* Homepage: distinctive brand signature without adding content */
.home-link-card{isolation:isolate}
.home-link-card>*{position:relative;z-index:2}
.home-link-card-dark{position:relative;overflow:hidden!important;background:linear-gradient(135deg,#1a1c1e 0%,#24272a 100%)!important}
.home-link-card-dark:after{content:"RN";position:absolute;right:-12px;bottom:-38px;z-index:0;color:rgba(255,255,255,.035);font-size:clamp(120px,15vw,220px);line-height:.8;letter-spacing:-.11em;font-weight:760;pointer-events:none}
.home-link-card-dark:before{z-index:3!important}
.home-link-card:nth-child(1){background:linear-gradient(135deg,#fff 0%,#fbfbfa 100%)!important}
.home-link-card:nth-child(1) h3{font-size:clamp(35px,3.5vw,49px)!important;max-width:560px}
.home-link-card:nth-child(1) p{font-size:15px!important;line-height:1.7!important}
.home-link-card:nth-child(2),.home-link-card:nth-child(3){background:#f8f8f6!important}
.home-overview-head .eyebrow{align-self:start;margin-top:10px}

/* Services: one deliberate full-width material change instead of three white rows */
.service-editorial{overflow:hidden}
.service-feature-reverse{position:relative!important;padding-top:78px!important;padding-bottom:78px!important;margin-top:4px!important;margin-bottom:94px!important;background:#f1f1ee!important;box-shadow:0 0 0 100vmax #f1f1ee!important;clip-path:inset(0 -100vmax)!important}
.service-feature-reverse:after{content:"";position:absolute;left:0;top:0;width:84px;height:2px;background:var(--red)}
.service-feature-reverse .service-visual{box-shadow:0 24px 58px rgba(22,24,26,.055)!important}
.service-feature-copy h2{font-size:clamp(34px,3.6vw,50px)!important;line-height:.98!important;letter-spacing:-.052em!important;font-weight:520!important}
.service-feature-copy p{font-size:15px!important;line-height:1.72!important;max-width:440px}

/* Existing closing CTAs become true premium closing moments */
.service-page-cta,.references-cta{position:relative!important;display:grid!important;grid-template-columns:minmax(0,1.5fr) auto!important;align-items:center!important;gap:44px!important;margin-top:96px!important;padding:60px 0!important;background:#191b1d!important;color:#fff!important;border:0!important;box-shadow:0 0 0 100vmax #191b1d!important;clip-path:inset(0 -100vmax)!important}
.service-page-cta:before,.references-cta:before{content:"";position:absolute;left:0;top:0;width:96px;height:3px;background:var(--red)}
.service-page-cta p,.references-cta p{margin:0!important;max-width:760px;color:#fff!important;font-size:clamp(28px,3.25vw,46px)!important;line-height:1.02!important;letter-spacing:-.052em!important;font-weight:500!important;text-wrap:balance}
.service-page-cta a,.references-cta a{display:inline-flex!important;align-items:center!important;justify-content:center!important;min-height:52px!important;padding:0 22px!important;border:1px solid rgba(255,255,255,.24)!important;color:#fff!important;background:rgba(255,255,255,.035)!important;font-size:12px!important;letter-spacing:.025em!important;white-space:nowrap;transition:background .2s ease,border-color .2s ease,transform .2s ease!important}

/* Company CTA: premium panel inside the editorial text column */
.company-page-cta{position:relative!important;margin-top:54px!important;padding:32px 34px!important;background:#1b1d1f!important;border:0!important;overflow:hidden}
.company-page-cta:before{content:"";position:absolute;left:0;top:0;width:64px;height:3px;background:var(--red)}
.company-page-cta p{position:relative;z-index:1;color:#d2d4d6!important;font-size:15px!important}
.company-page-cta a{position:relative;z-index:1;display:inline-flex;align-items:center;min-height:42px;padding:0 15px;border:1px solid rgba(255,255,255,.18);color:#fff!important;background:rgba(255,255,255,.035);font-size:11px!important;text-transform:uppercase;letter-spacing:.055em!important}

/* References: more gallery / magazine, less card grid */
.reference-media{position:relative;background:#e9e9e6!important}
.reference-item figcaption{position:relative;padding-top:22px!important}
.reference-item figcaption:before{content:"";display:block;width:36px;height:1px;margin-bottom:15px;background:#b9bcbe}
.reference-item h2{color:#1d2022!important}
.references-cta{margin-bottom:-104px!important}
.references-page{padding-bottom:104px!important}

/* Career: larger white field, stronger job hierarchy */
.career-page{padding-bottom:112px!important}
.job-card{position:relative;overflow:hidden!important}
.job-card h3{font-size:clamp(28px,2.75vw,38px)!important;line-height:1.04!important;letter-spacing:-.045em!important}
.job-card:after{content:"";position:absolute;right:-46px;bottom:-46px;width:120px;height:120px;border:1px solid rgba(27,29,31,.055);border-radius:50%;pointer-events:none}
.job-apply{font-size:12px!important;letter-spacing:.03em!important;text-transform:uppercase}

/* Contact: more architectural spacing, less generic dark block */
.contact-page{padding-top:108px!important;padding-bottom:118px!important}
.contact-main h2{font-size:clamp(42px,5vw,68px)!important;line-height:.97!important;letter-spacing:-.058em!important;font-weight:500!important}
.contact-number{margin-top:20px!important;font-size:clamp(30px,3.1vw,42px)!important}
.contact-address{padding-top:28px!important;border-top:1px solid rgba(255,255,255,.1)}

/* Footer: quiet, generous and deliberate */
footer{background:#121416!important;padding-top:16px!important;padding-bottom:16px!important}
.foot{min-height:66px!important}
.foot>span:first-child{letter-spacing:.02em}

/* Homepage editorial directory: no more card-grid appearance */
.home-overview{background:#f3f3f0!important;padding-top:96px!important;padding-bottom:116px!important}
.home-overview-head{margin-bottom:58px!important}
.home-link-grid{display:block!important;background:transparent!important;border-top:1px solid #c9cbca!important;box-shadow:none!important}
.home-link-card,.home-link-card:nth-child(n),.home-link-card-dark{display:grid!important;grid-template-columns:minmax(230px,.62fr) minmax(0,1fr) auto!important;align-items:center!important;gap:44px!important;min-height:0!important;margin:0!important;padding:38px 4px!important;background:transparent!important;border:0!important;border-bottom:1px solid #c9cbca!important;box-shadow:none!important;color:var(--ink)!important;overflow:visible!important;transition:padding .24s ease,background .24s ease!important}
.home-link-card:before{display:none!important}
.home-link-card-dark:after{display:none!important}
.home-link-card h3,.home-link-card:nth-child(1) h3{margin:0!important;max-width:none!important;color:var(--ink)!important;font-size:clamp(36px,3.35vw,50px)!important;line-height:.96!important;letter-spacing:-.052em!important;font-weight:510!important;transition:transform .24s ease!important}
.home-link-card p,.home-link-card:nth-child(1) p,.home-link-card-dark p{margin:0!important;max-width:560px!important;color:#6a6e72!important;font-size:14px!important;line-height:1.65!important}
.home-link-card b,.home-link-card-dark b{display:inline-flex!important;align-items:center!important;justify-content:flex-end!important;margin:0!important;color:#25282b!important;font-size:10px!important;line-height:1!important;letter-spacing:.07em!important;text-transform:uppercase!important;white-space:nowrap!important;opacity:1!important;transition:color .2s ease,transform .2s ease!important}
.home-link-card b:after{content:"";display:block;width:36px;height:1px;margin-left:14px;background:#9b9ea1;transition:width .24s ease,background .24s ease}
.home-link-card:last-child{border-bottom-color:#aeb0af!important}
.home-link-card:last-child h3{position:relative}
.home-link-card:last-child h3:after{content:"";position:absolute;left:0;bottom:-13px;width:42px;height:2px;background:var(--red)}

@media(hover:hover){
  .service-page-cta a:hover,.references-cta a:hover{background:#fff!important;border-color:#fff!important;color:#17191b!important;transform:translateY(-1px)}
  .company-page-cta a:hover{background:#fff;color:#17191b!important;border-color:#fff}
  .home-link-card:hover{padding-left:18px!important;padding-right:18px!important;background:rgba(255,255,255,.62)!important;transform:none!important;box-shadow:none!important}
  .home-link-card:hover h3{transform:translateX(3px)!important}
  .home-link-card:hover b{color:var(--red)!important;transform:none!important}
  .home-link-card:hover b:after{width:50px;background:var(--red)}
}

@media(max-width:900px){
  .home-link-card-dark:after{right:-4px;bottom:-20px;font-size:125px}
  .home-link-card:nth-child(1) h3{font-size:34px!important}
  .service-feature-reverse{padding-top:48px!important;padding-bottom:50px!important;margin-top:0!important;margin-bottom:54px!important}
  .service-feature-reverse:after{width:56px}
  .service-feature-copy h2{font-size:34px!important}
  .service-feature-copy p{font-size:14px!important}
  .service-page-cta,.references-cta{grid-template-columns:1fr!important;gap:28px!important;margin-top:64px!important;padding:48px 0!important}
  .service-page-cta:before,.references-cta:before{width:64px}
  .service-page-cta p,.references-cta p{font-size:31px!important;line-height:1.04!important}
  .service-page-cta a,.references-cta a{width:max-content!important;min-height:48px!important;padding:0 18px!important}
  .company-page-cta{padding:28px 24px!important}
  .references-cta{margin-bottom:-74px!important}
  .references-page{padding-bottom:74px!important}
  .career-page{padding-bottom:78px!important}
  .contact-page{padding-top:72px!important;padding-bottom:82px!important}
  .contact-main h2{font-size:42px!important}
  footer{padding-top:10px!important;padding-bottom:10px!important}
  .foot{min-height:54px!important}

  /* Mobile homepage directory: compact editorial rows, whole row remains the touch target. */
  .home-overview{padding-top:58px!important;padding-bottom:62px!important}
  .home-overview-head{margin-bottom:30px!important}
  .home-link-grid{border-top-color:#bfc1c0!important}
  .home-link-card,.home-link-card:nth-child(n),.home-link-card-dark{
    grid-template-columns:minmax(0,1fr) 44px!important;
    grid-template-areas:"title action" "copy action"!important;
    column-gap:18px!important;
    row-gap:9px!important;
    align-items:center!important;
    padding:24px 0!important;
    background:transparent!important;
    -webkit-tap-highlight-color:transparent;
  }
  .home-link-card h3,.home-link-card:nth-child(1) h3{
    grid-area:title;
    font-size:32px!important;
    line-height:.98!important;
  }
  .home-link-card p,.home-link-card:nth-child(1) p,.home-link-card-dark p{
    grid-area:copy;
    max-width:100%!important;
    padding-right:6px;
    font-size:13px!important;
    line-height:1.55!important;
  }
  .home-link-card b,.home-link-card-dark b{
    grid-area:action;
    align-self:center!important;
    justify-self:end!important;
    display:flex!important;
    width:42px!important;
    height:42px!important;
    margin:0!important;
    padding:0!important;
    justify-content:center!important;
    border:1px solid #c6c8c7;
    border-radius:50%;
    color:#24272a!important;
    font-size:0!important;
    letter-spacing:0!important;
    background:rgba(255,255,255,.28);
  }
  .home-link-card b:before,.home-link-card-dark b:before{
    content:"→";
    font-size:18px;
    line-height:1;
    font-weight:520;
    transform:translateY(-1px);
  }
  .home-link-card b:after,.home-link-card-dark b:after{display:none!important}
  .home-link-card:last-child h3:after{display:none!important}
  .home-link-card:active b{background:#24272a;color:#fff!important;border-color:#24272a}
}

@media(max-width:560px){
  .service-page-cta p,.references-cta p{font-size:28px!important}
  .company-page-cta{align-items:flex-start!important}
  .contact-main h2{font-size:38px!important}
  .home-overview{padding-top:54px!important;padding-bottom:58px!important}
  .home-link-card,.home-link-card:nth-child(n),.home-link-card-dark{padding:22px 0!important}
  .home-link-card h3,.home-link-card:nth-child(1) h3{font-size:31px!important}
}
</style>'''

for filename in MAIN_PAGES:
    path = Path(filename)
    html = path.read_text(encoding="utf-8")
    if 'id="rn-premium-finish"' in html:
        raise SystemExit(f"RN premium finish already present: {filename}")
    html = html.replace("</head>", finish_style + "\n</head>", 1)
    if 'id="rn-premium-finish"' not in html:
        raise SystemExit(f"RN premium finish insertion failed: {filename}")
    path.write_text(html, encoding="utf-8")
