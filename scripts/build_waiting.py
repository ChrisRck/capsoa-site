#!/usr/bin/env python3
"""Publish waiting homepages and approved, non-indexed legal documents."""
from pathlib import Path
import shutil
from build import ROOT, LANGS, LABELS, SOURCE, build
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
  instagram_labels = {'fr': 'Suivez CAPSOA sur Instagram', 'en': 'Follow CAPSOA on Instagram', 'es': 'Siguenos en Instagram', 'pt': 'Siga a CAPSOA no Instagram'}
  social_css = """<style>
    .instagram-link { display:inline-flex; align-items:center; justify-content:center; gap:10px; max-width:100%; margin-top:22px; padding:12px 16px; min-height:48px; color:#fff; background:rgba(20,13,29,.88); border:1px solid rgba(255,255,255,.45); border-radius:14px; font-size:1rem; line-height:1.5; text-decoration:underline; text-underline-offset:4px; }
    .instagram-link svg { width:28px; height:28px; flex-shrink:0; }
    .instagram-link:hover { background:rgba(65,30,80,.95); border-color:#e5a6ed; }
    .instagram-link:focus-visible { outline:3px solid #fff; outline-offset:4px; }
  </style>"""
  social_link = f'''<a class="instagram-link" href="https://www.instagram.com/capsoa.fr/" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 32 32" fill="none" aria-hidden="true" focusable="false"><defs><radialGradient id="instagram-colors" cx="28%" cy="100%" r="125%"><stop offset="0" stop-color="#ffdc80"/><stop offset=".24" stop-color="#fcaf45"/><stop offset=".45" stop-color="#f77737"/><stop offset=".62" stop-color="#e1306c"/><stop offset=".8" stop-color="#c13584"/><stop offset="1" stop-color="#5851db"/></radialGradient></defs><rect width="32" height="32" rx="8" fill="url(#instagram-colors)"/><rect x="7" y="7" width="18" height="18" rx="5.5" stroke="#fff" stroke-width="2"/><circle cx="16" cy="16" r="4.5" stroke="#fff" stroke-width="2"/><circle cx="22" cy="10" r="1.3" fill="#fff"/></svg><span>{instagram_labels[lang]}</span></a>'''
  page = page.replace('</head>', social_css + '</head>')
  assert page.count('</section>') == 1
  page = page.replace('</section>', social_link + '\n    </section>')
  (out/lang).mkdir(exist_ok=True);(out/lang/'index.html').write_text(page)
 (out/'index.html').write_text((out/'fr/index.html').read_text())
 # Build the approved documents, keeping every waiting homepage unchanged.
 build()
 for lang in LANGS:
  for name in SOURCE:
   if name != 'index.html':
    shutil.copyfile(ROOT/'public'/lang/name,out/lang/name)
 for name in SOURCE:
  if name != 'index.html':
   shutil.copyfile(ROOT/'public'/name,out/name)
 print('Waiting homepages preserved; approved legal documents published with noindex in four languages.')
if __name__=='__main__':build_waiting()
