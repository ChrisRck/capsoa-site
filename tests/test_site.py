import sys,unittest,json,re
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote,parse_qs
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build
class Inspect(HTMLParser):
 def __init__(self,text):
  super().__init__();self.tags=[];self.feed(text)
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
class SiteTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):build.build()
 def test_28_pages_complete_and_internal_links_resolve(self):
  for lang in build.LANGS:
   for name in build.SOURCE:
    with self.subTest(language=lang,page=name):
     text=(build.ROOT/'public'/lang/name).read_text();p=Inspect(text)
     self.assertIn(('html',{'lang':lang}),p.tags)
     selectors=[a for t,a in p.tags if 'data-language' in a]
     self.assertEqual({a['data-language'] for a in selectors},set(build.LANGS))
     self.assertEqual(len([a for a in selectors if a.get('aria-current')=='page']),1)
     for tag,a in p.tags:
      for k in ['href','src']:
       u=urlsplit(a.get(k,''))
       if not u.path.startswith('/') or u.netloc or u.scheme:continue
       file=build.ROOT/'public'/unquote(u.path).lstrip('/')
       self.assertTrue(file.is_file() or (file/'index.html').is_file() or file.with_suffix('.html').is_file(),str(file))
     original=Inspect((build.ROOT/'src/fr'/name).read_text())
     for element in ['h1','h2','p','li','section']:
      self.assertEqual(sum(t==element for t,a in p.tags),sum(t==element for t,a in original.tags))
 def test_numeric_terms_preserved(self):
  def numbers(s):return sorted(re.findall(r'\d+(?:[.,]\d+)?',s.replace('0,59','0.59')))
  for lang in ['en','es','pt']:
   translation=json.loads((build.ROOT/'translations'/f'{lang}.json').read_text())
   for name,source in build.SOURCE.items():
    for i,original in enumerate(source):
     with self.subTest(language=lang,page=name,node=i):
      self.assertEqual(numbers(original),numbers(translation[name][i]))
 def test_french_source_stays_intact(self):
  for name,strings in build.SOURCE.items():
   build.Translate(name,'fr',strings).render((build.ROOT/'src/fr'/name).read_text())
 def test_contact_and_deletion_are_localized(self):
  for lang in build.LANGS:
   page=(build.ROOT/'public'/lang/'index.html').read_text()
   self.assertIn('https://capsoa.web.app/contact?lang='+lang,page)
   p=Inspect((build.ROOT/'public'/lang/'suppression-compte.html').read_text())
   links=[a['href'] for t,a in p.tags if a.get('href','').startswith('mailto:contact@capsoa.fr?')]
   self.assertEqual(len(links),1)
   q=parse_qs(urlsplit(links[0]).query)
   self.assertEqual(q['body'],[build.BODIES[lang]])
 def test_visible_text_not_silently_left_in_french(self):
  allowed={'App Store','Google Play','©2026 CAPSOA','5 Allée des Demoiselles','77230 Saint-Mard, France','SIRET : 13034465800013','2 - Contact','contact@capsoa.fr','Google Cloud','CAPSOA','CAPSOA ·','www.cnil.fr'}
  for lang in ['en','es','pt']:
   translated=json.loads((build.ROOT/'translations'/f'{lang}.json').read_text())
   for name,strings in build.SOURCE.items():
    for i,s in enumerate(strings):
     if any(c.isalpha() for c in s) and s not in allowed:self.assertNotEqual(s,translated[name][i],(lang,name,i))
if __name__=='__main__':unittest.main()
