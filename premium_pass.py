from pathlib import Path

MAIN_PAGES = (
    "index.html",
    "leistungen.html",
    "referenzen.html",
    "unternehmen.html",
    "karriere.html",
    "kontakt.html",
)

premium_style = r'''<style id="rn-premium-pass">
/* RN premium pass: refinement only, no structural redesign */
html{scroll-behavior:smooth}
body{font-synthesis:none;text-rendering:optimizeLegibility}
a:focus-visible,button:focus-visible{outline:2px solid var(--red);outline-offset:4px}

/* Header: quieter proportions and sharper interaction */
header{height:86px!important;border-bottom-color:rgba(25,27,30,.085)!important;box-shadow:0 8px 28px rgba(20,22,24,.018)}
.head{gap:24px!important}
.logo{width:212px!important}
.nav{gap:29px!important;font-weight:675!important;letter-spacing:.005em!important}
.nav a{padding-top:34px!important;padding-bottom:32px!important;transition:color .2s ease,opacity .2s ease}
.nav a:after{height:2px!important;bottom:23px!important}
.header-cta{min-height:44px!important;padding:0 18px!important;gap:12px;border:1px solid rgba(255,255,255,.08);letter-spacing:.005em!important;box-shadow:0 8px 24px rgba(20,22,24,.07)}
.header-cta:after{content:"→";font-size:15px;line-height:1;transition:transform .2s ease}

/* Shared editorial hierarchy */
.eyebrow{font-size:10px!important;letter-spacing:.195em!important;font-weight:780!important}
.page-hero{padding:88px 0 78px!important;background:linear-gradient(180deg,#fff 0%,#fbfbfa 100%)!important;border-bottom-color:#e4e5e6!important}
.page-hero-grid{grid-template-columns:minmax(150px,.42fr) minmax(0,1.58fr)!important;gap:72px!important}
.page-hero .eyebrow{padding-top:10px}
.page-hero h1{text-wrap:balance;max-width:860px!important;font-weight:500!important;letter-spacing:-.057em!important}
.page-hero p{max-width:640px!important;color:#64686c!important;line-height:1.72!important}

/* Homepage: retain layout, add depth and precision */
.home-overview-head{margin-bottom:40px!important}
.home-overview-head h2{text-wrap:balance;max-width:760px}
.home-link-grid{box-shadow:0 22px 60px rgba(22,24,26,.035)}
.home-link-card{position:relative;overflow:hidden;transition:background .24s ease,transform .24s ease,box-shadow .24s ease!important}
.home-link-card:before{content:"";position:absolute;left:0;top:-1px;width:100%;height:2px;background:var(--red);transform:scaleX(0);transform-origin:left;transition:transform .28s ease}
.home-link-card h3{transition:transform .24s ease}
.home-link-card b{letter-spacing:.01em;transition:transform .2s ease,opacity .2s ease}

/* Services: calmer image presentation and stronger closing line */
.service-editorial{padding-top:66px!important}
.service-feature{margin-bottom:96px!important}
.service-visual{box-shadow:0 20px 54px rgba(24,26,28,.045)}
.service-feature-copy h2{text-wrap:balance}
.service-feature-copy p{color:#62666a!important}
.service-page-cta,.references-cta,.company-page-cta{position:relative;background:#f7f7f5!important;border:0!important;border-left:2px solid var(--red)!important;padding:25px 28px!important;margin-top:56px!important}
.service-page-cta a,.references-cta a,.company-page-cta a{font-weight:760!important;letter-spacing:.005em}

/* References: editorial rhythm instead of a standard gallery */
.references-page{padding-top:76px!important;background:linear-gradient(180deg,#fff 0%,#fbfbfa 100%)!important}
.references-grid{display:grid!important;grid-template-columns:repeat(12,minmax(0,1fr))!important;gap:84px 24px!important;align-items:start}
.reference-item{min-width:0}
.reference-item:nth-child(1){grid-column:1/span 7}
.reference-item:nth-child(2){grid-column:8/span 5;margin-top:72px}
.reference-item:nth-child(3){grid-column:1/span 5}
.reference-item:nth-child(4){grid-column:6/span 7;margin-top:38px}
.reference-item:nth-child(1) .reference-media,.reference-item:nth-child(4) .reference-media{aspect-ratio:16/10!important}
.reference-item:nth-child(2) .reference-media,.reference-item:nth-child(3) .reference-media{aspect-ratio:4/3!important}
.reference-media{box-shadow:0 20px 52px rgba(24,26,28,.04)}
.reference-item figcaption{grid-template-columns:1fr!important;gap:7px!important;padding-top:17px!important;border-top:0!important}
.reference-item h2{text-wrap:balance;font-weight:545!important}
.reference-item p{max-width:420px;color:#6b6f73!important}

/* Company: more breathing room around the single strong image */
.company-page.company-editorial{padding-top:50px!important}
.company-stage-media{margin-bottom:78px!important;box-shadow:0 24px 58px rgba(24,26,28,.04)}
.company-editorial .company-grid{gap:82px!important}
.company-editorial .company-main h2{text-wrap:balance}
.company-copy .company-lead{color:#292d31!important}

/* Career: make the two jobs feel deliberately designed, not templated */
.career-page{background:linear-gradient(180deg,#f6f6f4 0%,#fbfbfa 58%,#fff 100%)!important;padding-top:82px!important}
.career-head{padding-bottom:28px;border-bottom:1px solid #dfe1e2}
.career-copy strong{font-weight:560!important;letter-spacing:-.03em!important}
.job-grid{gap:26px!important;margin-top:30px!important}
.job-card{display:flex!important;flex-direction:column;background:#fff!important;border:1px solid #dedfe0!important;padding:32px 32px 30px!important;min-height:430px!important;transition:transform .24s ease,box-shadow .24s ease,border-color .24s ease}
.job-card:before{left:-1px!important;top:-1px!important;width:72px!important;height:2px!important}
.job-card h3{text-wrap:balance;font-weight:560!important}
.job-card p{color:#62666a!important}
.job-card ul{border-top-color:#e5e6e7!important}
.job-apply{margin-top:auto!important;padding-top:28px!important;border-top:1px solid #ececed;color:var(--ink)!important;font-weight:720!important}
.job-apply span:last-child{transition:transform .2s ease}
.career-benefits{display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr));gap:0!important;margin-top:42px!important;padding:22px 0!important;border-top:1px solid #dfe1e2;border-bottom:1px solid #dfe1e2}
.career-benefits span{padding:0 22px;color:#666a6e;font-size:12px;line-height:1.55}
.career-benefits span:first-child{padding-left:0}
.career-benefits span+span{border-left:1px solid #dfe1e2}
.career-benefits strong{display:block;margin-bottom:3px;color:var(--ink);font-weight:720}

/* Contact: stronger final destination without adding content */
.contact-page{position:relative;overflow:hidden;background:radial-gradient(circle at 82% 8%,rgba(183,23,36,.12),transparent 34%),var(--dark)!important}
.contact-page:before{content:"";position:absolute;left:0;right:0;top:0;height:1px;background:rgba(255,255,255,.08)}
.contact-grid{position:relative;z-index:1}
.contact-main h2{text-wrap:balance;max-width:780px}
.contact-copy{max-width:570px!important}
.contact-number{display:block;width:max-content;font-size:clamp(27px,2.5vw,35px)!important;letter-spacing:-.025em!important;transition:opacity .2s ease}
.contact-email{letter-spacing:-.01em!important}
.contact-links{gap:18px 28px!important;margin-top:24px!important;padding-top:22px;border-top:1px solid rgba(255,255,255,.12)}
.contact-links a{transition:opacity .2s ease,transform .2s ease}
.contact-address{margin-top:34px!important}

/* Footer: cleaner ending */
footer{border-top:1px solid rgba(255,255,255,.055)}
.foot{align-items:center;min-height:58px}
.foot-links{gap:24px}
.foot a{transition:color .2s ease,opacity .2s ease}

/* Subtle reveal on scroll; disabled automatically for reduced motion */
.rn-reveal{opacity:0;transform:translateY(12px);transition:opacity .62s cubic-bezier(.22,.61,.36,1),transform .62s cubic-bezier(.22,.61,.36,1)}
.rn-reveal.rn-visible{opacity:1;transform:none}

@media(hover:hover){
  .header-cta:hover:after{transform:translateX(3px)}
  .home-link-card:hover{transform:translateY(-2px);box-shadow:0 24px 54px rgba(22,24,26,.055)}
  .home-link-card:hover:before{transform:scaleX(1)}
  .home-link-card:hover h3{transform:translateY(-1px)}
  .home-link-card:hover b{transform:translateX(3px)}
  .reference-item:hover .reference-media img{transform:scale(1.018)!important}
  .job-card:hover{transform:translateY(-2px);border-color:#d6d8da!important;box-shadow:0 22px 48px rgba(22,24,26,.055)}
  .job-apply:hover span:last-child{transform:translateX(3px)}
  .contact-number:hover,.contact-email:hover,.contact-links a:hover{opacity:.72}
  footer a:hover{color:#fff}
}

@media(min-width:901px) and (max-width:1180px){
  .logo{width:184px!important}
  .head{gap:16px!important}
  .nav{gap:16px!important;font-size:11px!important}
  .header-cta{padding:0 13px!important}
  .page-hero-grid{grid-template-columns:minmax(120px,.34fr) minmax(0,1.66fr)!important;gap:46px!important}
  .company-editorial .company-grid{gap:52px!important}
}

@media(max-width:900px){
  header{height:74px!important;box-shadow:none}
  .logo{width:188px!important}
  .page-hero{padding:56px 0 52px!important}
  .page-hero-grid{grid-template-columns:1fr!important;gap:16px!important}
  .page-hero .eyebrow{padding-top:0}
  .page-hero h1{letter-spacing:-.052em!important}
  .service-editorial{padding-top:28px!important}
  .service-feature{margin-bottom:50px!important}
  .service-visual{box-shadow:none}
  .service-page-cta,.references-cta,.company-page-cta{padding:22px 20px!important;margin-top:42px!important}
  .references-page{padding-top:48px!important}
  .references-grid{grid-template-columns:1fr!important;gap:46px!important}
  .reference-item:nth-child(n){grid-column:1/-1!important;margin-top:0!important}
  .reference-item:nth-child(n) .reference-media{aspect-ratio:16/10!important;box-shadow:none}
  .company-page.company-editorial{padding-top:24px!important}
  .company-stage-media{margin-bottom:44px!important;box-shadow:none}
  .company-editorial .company-grid{gap:18px!important}
  .career-page{padding-top:56px!important}
  .career-head{padding-bottom:22px}
  .job-grid{gap:22px!important}
  .job-card{min-height:0!important;padding:27px 24px 25px!important}
  .career-benefits{grid-template-columns:1fr 1fr!important;row-gap:18px!important;padding:20px 0!important}
  .career-benefits span{padding:0 16px!important}
  .career-benefits span:nth-child(odd){padding-left:0!important;border-left:0!important}
  .career-benefits span:nth-child(even){border-left:1px solid #dfe1e2!important}
  .contact-links{gap:18px 24px!important}
  .foot{min-height:0}
}

@media(max-width:560px){
  .career-benefits{grid-template-columns:1fr!important;gap:13px!important}
  .career-benefits span{padding:0!important;border-left:0!important}
}

@media(prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .rn-reveal{opacity:1!important;transform:none!important;transition:none!important}
  *{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important}
}
</style>'''

motion_script = r'''<script id="rn-premium-motion">
(() => {
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const selectors = [
    '.page-hero-grid > *',
    '.home-overview-head > *',
    '.home-link-card',
    '.service-feature',
    '.reference-item',
    '.company-stage-media',
    '.company-grid',
    '.career-head',
    '.job-card',
    '.career-benefits',
    '.contact-grid'
  ].join(',');
  const items = Array.from(document.querySelectorAll(selectors));
  if (!items.length) return;
  items.forEach((el, index) => {
    el.classList.add('rn-reveal');
    el.style.transitionDelay = `${Math.min(index % 4, 3) * 45}ms`;
  });
  if (!('IntersectionObserver' in window)) {
    items.forEach(el => el.classList.add('rn-visible'));
    return;
  }
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('rn-visible');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -24px 0px' });
  items.forEach(el => observer.observe(el));
})();
</script>'''

for filename in MAIN_PAGES:
    path = Path(filename)
    html = path.read_text(encoding="utf-8")
    if 'id="rn-premium-pass"' in html:
        raise SystemExit(f"RN premium pass already present: {filename}")
    html = html.replace("</head>", premium_style + "\n</head>", 1)
    html = html.replace("</body>", motion_script + "\n</body>", 1)
    if 'id="rn-premium-pass"' not in html or 'id="rn-premium-motion"' not in html:
        raise SystemExit(f"RN premium pass insertion failed: {filename}")
    path.write_text(html, encoding="utf-8")

# Keep legal pages visually aligned without changing their content or structure.
legal_style = r'''<style id="rn-legal-premium">
header{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.97);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
.back{transition:color .2s ease,transform .2s ease}.title{font-weight:500!important;letter-spacing:-.05em!important}.lead{color:#666a6e}.block h2{letter-spacing:-.012em}.block{transition:background .2s ease}.legal{border-top-color:#dedfe0}.foot{align-items:center}
@media(hover:hover){.back:hover{color:var(--red);transform:translateX(-2px)}.block:hover{background:#fbfbfa}}
</style>'''
for filename in ("impressum.html", "datenschutz.html"):
    path = Path(filename)
    html = path.read_text(encoding="utf-8")
    html = html.replace("</head>", legal_style + "\n</head>", 1)
    path.write_text(html, encoding="utf-8")
