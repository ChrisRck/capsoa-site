const vm=require('node:vm'), fs=require('node:fs'), assert=require('node:assert/strict');
const script=fs.readFileSync(require('node:path').join(__dirname,'../src/language.js'),'utf8');
function run(path,{saved=null,languages=['fr'],blocked=false}={}) {
 let redirected=null;const links=['fr','en','es','pt'].map(l=>({href:'https://capsoa.fr/'+l+'/cgu',dataset:{language:l},addEventListener(){}}));
 const localStorage={getItem(){if(blocked)throw Error();return saved},setItem(k,v){if(blocked)throw Error();saved=v}};
 vm.runInNewContext(script,{URL,localStorage,navigator:{languages},document:{querySelectorAll:()=>links},window:{location:{href:'https://capsoa.fr'+path,replace:v=>redirected=v}}});
 return {redirected,saved,links};
}
assert.equal(run('/cgu?lang=pt-BR#article-4',{saved:'es'}).redirected,'https://capsoa.fr/pt/cgu#article-4');
assert.equal(run('/en/cgu?lang=pt',{saved:'es'}).redirected,null);
assert.equal(run('/en/cgu',{saved:'es'}).saved,'en');
assert.equal(run('/cgv.html',{saved:'pt'}).redirected,'https://capsoa.fr/pt/cgv');
assert.equal(run('/',{languages:['de','es-MX'],blocked:true}).redirected,'https://capsoa.fr/es/');
assert.equal(run('/',{languages:['de']}).redirected,'https://capsoa.fr/fr/');
assert.equal(run('/pt/cgu#article-4').links[1].href,'https://capsoa.fr/en/cgu#article-4');
assert.equal(run('/unknown',{saved:'pt'}).redirected,null);
console.log('8 language routing checks passed');
