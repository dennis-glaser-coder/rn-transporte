from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")

home_style = r'''<style id="rn-home-finetune">
@media(min-width:1181px){
  .home-overview{padding:72px 0 92px!important}
  .home-overview-head{gap:56px!important;margin-bottom:34px!important}
  .home-overview-head .eyebrow{padding-top:8px}
  .home-link-card{min-height:238px!important;padding:28px 30px 25px!important}
  .home-link-card b{padding-top:22px!important}

  /* Keep every editorial row on the exact same three-column grid. */
  body .home-overview .home-link-card{
    grid-template-columns:31% minmax(0,1fr) 250px!important;
    gap:44px!important;
  }
  body .home-overview .home-link-card:hover{
    padding-left:4px!important;
    padding-right:4px!important;
  }
  body .home-overview .home-link-card:last-child h3:after{
    display:none!important;
    content:none!important;
  }
}
@media(min-width:901px) and (max-width:1180px){
  .home-overview{padding:72px 0 92px!important}
  .home-overview-head{gap:44px!important;margin-bottom:34px!important}
  .home-overview-head .eyebrow{padding-top:8px}
  .home-link-card{min-height:220px!important;padding:28px 24px 25px!important}
  .home-link-card b{padding-top:22px!important}

  body .home-overview .home-link-card{
    grid-template-columns:32% minmax(0,1fr) 190px!important;
    gap:28px!important;
  }
  body .home-overview .home-link-card:hover{
    padding-left:4px!important;
    padding-right:4px!important;
  }
  body .home-overview .home-link-card:last-child h3:after{
    display:none!important;
    content:none!important;
  }
}
@media(max-width:900px){
  .home-overview{padding:52px 0 64px!important}
  .home-overview-head{margin-bottom:26px!important}
  .home-link-card{min-height:190px!important;padding:23px 22px!important}
  .home-link-card b{padding-top:22px!important}
}
</style>'''

if 'id="rn-home-finetune"' not in html:
    html = html.replace("</head>", home_style + "\n</head>", 1)

path.write_text(html, encoding="utf-8")
