from pathlib import Path

path = Path("leistungen.html")
html = path.read_text(encoding="utf-8")

style = r'''<style id="rn-mobile-overflow-fix">
@media(max-width:900px){
  html,body{max-width:100%;overflow-x:hidden!important}
  .service-editorial,.service-editorial-list,.service-feature{max-width:100%;min-width:0}
  .service-visual{margin-left:-16px!important;margin-right:-16px!important;width:calc(100% + 32px)!important;max-width:none!important}
}
</style>'''

if 'id="rn-mobile-overflow-fix"' in html:
    raise SystemExit("RN mobile overflow fix already present")

html = html.replace("</head>", style + "\n</head>", 1)

if 'margin-left:-16px!important' not in html or 'width:calc(100% + 32px)!important' not in html:
    raise SystemExit("RN mobile overflow fix insertion failed")

path.write_text(html, encoding="utf-8")
