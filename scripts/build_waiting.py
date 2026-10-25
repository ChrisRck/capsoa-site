#!/usr/bin/env python3
"""Publish only waiting pages; preserve the pre-existing legacy legal files."""
from pathlib import Path
import shutil
from build import ROOT, LANGS, LABELS
WORDS={
 'fr':('L’application arrive bientôt','Bientôt disponible',"Disponibilité de l'application"),
 'en':('The app is coming soon','Coming soon','App availability'),
 'es':('La aplicación llegará pronto','Próximamente','Disponibilidad de la aplicación'),
 'pt':('A aplicação estará disponível em breve','Em breve','Disponibilidade da aplicação')}
def build_waiting():
 backup=ROOT/'src/live-before-2026-10-24';out=ROOT/'public-waiting'
 out.mkdir(exist_ok=True)
 for f in backup.iterdir():
  if f.is_file():shutil.copyfile(f,out/f.name)
 (out/'assets').mkdir(exist_ok=True)
 for name in ['logo-capsoa.png','fond-tour-eiffel.png']:shutil.copyfile(backup/name,out/'assets'/name)
 for name in ['language.js','language.css']:shutil.copyfile(ROOT/'src'/name,out/'assets'/name)
 shutil.copyfile(ROOT/'src/assets/logo-capsoa-international.png',out/'assets/logo-capsoa-international.png')
 original=(backup/'index.html').read_text()
 for lang in LANGS:
  title,soon,availability=WORDS[lang]
  page=original.replace('lang="fr"',f'lang="{lang}"').replace('L’application arrive bientôt',title).replace('Bientôt disponible',soon).replace("Disponibilité de l'application",availability)
  descriptions={'fr':'Capsoa — L’application arrive bientôt sur App Store et Google Play.','en':'CAPSOA — The app is coming soon to the App Store and Google Play.','es':'CAPSOA — La aplicación llegará pronto a App Store y Google Play.','pt':'CAPSOA — A aplicação estará disponível em breve na App Store e no Google Play.'}
  import re
  page=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{descriptions[lang]}">',page)
  page=page.replace('./fond-tour-eiffel.png','/assets/fond-tour-eiffel.png').replace('./logo-capsoa.png','/assets/'+('logo-capsoa.png' if lang=='fr' else 'logo-capsoa-international.png'))
  if lang!='fr':
   page=page.replace('<header>', '<header class="international-brand">')
   page=page.replace('</header>', '<div class="brand-glint" aria-hidden="true"></div><p class="brand-tagline">Capture Today, Surprise Tomorrow</p></header>')
  nav=f'<nav class="language-switcher language-flags" aria-label="{LABELS[lang][0]}">'
  flags={'fr':'🇫🇷','en':'🇬🇧','es':'🇪🇸','pt':'🇵🇹'}
  nav+=''.join(f'<a href="/{l}/" lang="{l}" hreflang="{l}" data-language="{l}"'+(' aria-current="page"' if l==lang else '')+f' aria-label="{label}" title="{label}"><span aria-hidden="true">{flags[l]}</span></a>' for l,label in LANGS.items())+'</nav>'
  page=page.replace('<body>','<body>'+nav)
  page=page.replace('</head>','<link rel="stylesheet" href="/assets/language.css?v=20261025-transparent"><script defer src="/assets/language.js"></script></head>')
  (out/lang).mkdir(exist_ok=True);(out/lang/'index.html').write_text(page)
 (out/'index.html').write_text((out/'fr/index.html').read_text())
 # No translated legal document may accidentally be included in this deployment.
 for lang in LANGS:
  assert sorted(p.name for p in (out/lang).iterdir())==['index.html'], 'Unexpected future document in waiting build'
 for f in backup.glob('*.html'):
  if f.name!='index.html':assert (out/f.name).read_bytes()==f.read_bytes()
 print('Four waiting pages built; existing legal files unchanged; future site excluded.')
if __name__=='__main__':build_waiting()
