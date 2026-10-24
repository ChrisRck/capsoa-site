#!/usr/bin/env python3
"""Build all static locales, failing if approved French text has changed."""
from html.parser import HTMLParser
from html import escape
from pathlib import Path
from urllib.parse import urlsplit, quote
import json,re,shutil
ROOT=Path(__file__).resolve().parents[1]
LANGS={'fr':'Français','en':'English','es':'Español','pt':'Português'}
LABELS={
 'fr':('Langue','Informations juridiques',"Disponibilité de l’application"),
 'en':('Language','Legal information','App availability'),
 'es':('Idioma','Información legal','Disponibilidad de la aplicación'),
 'pt':('Idioma','Informações legais','Disponibilidade da aplicação')}
DESC={
 'fr':"CAPSOA, l’application française de capsule temporelle numérique. Aujourd’hui ne s’oubliera jamais. Bientôt disponible sur App Store et Google Play.",
 'en':'CAPSOA, the French digital time capsule app. Capture Today, Surprise Tomorrow. Coming soon to the App Store and Google Play.',
 'es':'CAPSOA, la aplicación francesa de cápsulas temporales digitales. Capture Today, Surprise Tomorrow. Próximamente en App Store y Google Play.',
 'pt':'CAPSOA, a aplicação francesa de cápsulas temporais digitais. Capture Today, Surprise Tomorrow. Em breve na App Store e no Google Play.'}
BODIES={
 'fr':'Bonjour,\nJe souhaite supprimer mon compte CAPSOA et les données associées.\nAdresse du compte concerné : \nMerci.',
 'en':'Hello,\nI would like to delete my CAPSOA account and its associated data.\nEmail address of the account concerned: \nThank you.',
 'es':'Hola:\nDeseo eliminar mi cuenta CAPSOA y sus datos asociados.\nCorreo electrónico de la cuenta: \nGracias.',
 'pt':'Olá,\nPretendo eliminar a minha conta CAPSOA e os dados associados.\nEndereço de e-mail da conta: \nObrigado.'}
SOURCE=json.loads((ROOT/'translations/fr.json').read_text())
def route(lang,name):return '/'+lang+'/' + ('' if name=='index.html' else name[:-5])
class Translate(HTMLParser):
 def __init__(self,name,lang,strings):
  super().__init__(convert_charrefs=True);self.name=name;self.lang=lang;self.strings=strings;self.i=0;self.out=[];self.skip=[]
 def handle_decl(self,s):self.out.append('<!'+s+'>')
 def handle_comment(self,s):self.out.append('<!--'+s+'-->')
 def handle_starttag(self,tag,attrs):
  if tag in ('script','style','svg'):self.skip.append(tag)
  result=[]
  for k,v in attrs:
   if k=='lang' and tag=='html':v=self.lang
   if tag=='meta' and dict(attrs).get('name')=='description' and k=='content':v=DESC[self.lang]
   if k=='aria-label':
    v={'Informations juridiques':LABELS[self.lang][1],"Disponibilité de l'application":LABELS[self.lang][2]}.get(v,v)
   if k=='src' and v and v.lstrip('./') in ('logo-capsoa.png','fond-tour-eiffel.png'):
    v='/assets/'+v.lstrip('./')
    if v=='/assets/logo-capsoa.png' and self.lang!='fr':v='/assets/logo-capsoa-international.png'
   if k=='href' and v:
    u=urlsplit(v);filename=u.path.rsplit('/',1)[-1]
    if not u.scheme and not u.netloc and (filename in SOURCE or u.path=='/'):
     v=route(self.lang,filename if filename in SOURCE else 'index.html')+('?' + u.query if u.query else '')+('#'+u.fragment if u.fragment else '')
    if v=='https://capsoa.web.app/contact':v+='?lang='+self.lang
    if v.startswith('mailto:contact@capsoa.fr?'):
     strings=json.loads((ROOT/('translations/'+self.lang+'.json')).read_text())
     v='mailto:contact@capsoa.fr?subject='+quote(strings['suppression-compte.html'][10])+'&body='+quote(BODIES[self.lang])
   result.append(k if v is None else k+'="'+escape(v,quote=True)+'"')
  self.out.append('<'+tag+(' '+' '.join(result) if result else '')+'>')
 def handle_startendtag(self,tag,attrs):
  self.handle_starttag(tag,attrs);self.out[-1]=self.out[-1][:-1]+'/>'
  if self.skip and self.skip[-1]==tag:self.skip.pop()
 def handle_endtag(self,tag):
  self.out.append('</'+tag+'>')
  if self.skip and self.skip[-1]==tag:self.skip.pop()
 def handle_data(self,data):
  if self.skip:
   self.out.append(data.replace('./fond-tour-eiffel.png','/assets/fond-tour-eiffel.png'));return
  if not data.strip():self.out.append(data);return
  assert self.i<len(SOURCE[self.name]) and data.strip()==SOURCE[self.name][self.i],f'Source changed: {self.name} node {self.i}'
  translated=self.strings[self.i];assert translated.strip(),f'Empty: {self.name} {self.i}'
  self.i+=1
  m=re.match(r'^(\s*)(.*?)(\s*)$',data,re.S)
  self.out.append(m[1]+escape(translated,quote=False)+m[3])
 def render(self,source):
  self.feed(source);assert self.i==len(SOURCE[self.name]);return ''.join(self.out)

def build():
 out=ROOT/'public';out.mkdir(exist_ok=True);(out/'assets').mkdir(exist_ok=True)
 for name in ['logo-capsoa.png','fond-tour-eiffel.png']:
  shutil.copyfile(ROOT/name,out/'assets'/name)
 shutil.copyfile(ROOT/'src/assets/logo-capsoa-international.png',out/'assets/logo-capsoa-international.png')
 shutil.copyfile(ROOT/'src/language.js',out/'assets/language.js')
 shutil.copyfile(ROOT/'src/language.css',out/'assets/language.css')
 for lang in LANGS:
  translations=json.loads((ROOT/('translations/'+lang+'.json')).read_text())
  assert set(translations)==set(SOURCE),f'Missing pages: {lang}'
  (out/lang).mkdir(exist_ok=True)
  for name,source_strings in SOURCE.items():
   assert len(translations[name])==len(source_strings),f'Missing paragraphs: {lang} {name}'
   source=(ROOT/'src/fr'/name).read_text()
   page=Translate(name,lang,translations[name]).render(source)
   alternates=''.join(f'<link rel="alternate" hreflang="{l}" href="https://capsoa.fr{route(l,name)}">' for l in LANGS)
   nav=f'<nav class="language-switcher" aria-label="{LABELS[lang][0]}"><span>{LABELS[lang][0]} :</span>'
   for l,label in LANGS.items():
    current=' aria-current="page"' if l==lang else ''
    nav+=f'<a href="{route(l,name)}" lang="{l}" hreflang="{l}" data-language="{l}"{current}>{label}</a>'
   nav+='</nav>'
   page=page.replace('</head>',alternates+'<link rel="stylesheet" href="/assets/language.css"><script defer src="/assets/language.js"></script></head>')
   page=page.replace('<body>','<body>'+nav,1)
   if name=='cgu.html':
    word={'fr':'ici','en':'here','es':'aquí','pt':'aqui'}[lang]
    page=page.replace('['+word+']',f'<a href="/{lang}/conditions-mineurs">{word}</a>')
   (out/lang/name).write_text(page)
 # Legacy URLs remain usable without JS, defaulting to French. JS honours explicit
 # ?lang=, saved preference and browser language on these unprefixed pages only.
 for name in SOURCE:
  page=(out/'fr'/name).read_text()
  (out/name).write_text(page)
 (out/'404.html').write_text((out/'fr/index.html').read_text())
 print(f'Built {len(SOURCE)*len(LANGS)} complete localized pages plus legacy entry points.')
if __name__=='__main__':build()
