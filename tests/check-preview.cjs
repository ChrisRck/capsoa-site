const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const root=path.join(__dirname,'..'),base=process.argv[2];
if(!base)throw Error('Pass the preview URL');
const source=JSON.parse(fs.readFileSync(path.join(root,'translations/fr.json')));
const jobs=Object.keys(source).flatMap(f=>['fr','en','es','pt'].map(l=>({file:path.join(root,'public',l,f),url:base+'/'+l+'/'+(f==='index.html'?'':f.slice(0,-5))})));
(async()=>{
 for(let i=0;i<jobs.length;i+=4)await Promise.all(jobs.slice(i,i+4).map(async ({file,url})=>{
  const response=await fetch(url);assert.equal(response.status,200,url);
  const body=await response.text();assert.equal(body,fs.readFileSync(file,'utf8'),url);
 }));
 console.log('28 preview routes return HTTP 200 and match the local build byte for byte.');
})();
