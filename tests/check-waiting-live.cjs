const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.join(__dirname,'..','public-waiting');
(async()=>{
 for(const lang of ['fr','en','es','pt']){
  const r=await fetch('https://capsoa.fr/'+lang+'/');assert.equal(r.status,200);assert.equal(await r.text(),fs.readFileSync(path.join(root,lang,'index.html'),'utf8'));
  const absent=await fetch('https://capsoa.fr/'+lang+'/cgv');assert.equal(absent.status,404,'Future legal page unexpectedly live');
 }
 for(const name of ['cgu.html','cgv.html','conditions-mineurs.html','mentions-legales.html','suppression-compte.html']){
  const r=await fetch('https://capsoa.fr/'+name);assert.equal(r.status,200);assert.equal(await r.text(),fs.readFileSync(path.join(root,name),'utf8'));
 }
 console.log('Four live waiting pages verified; five old legal files unchanged; future legal pages remain unpublished.');
})();
