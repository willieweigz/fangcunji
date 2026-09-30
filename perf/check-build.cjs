const fs=require('fs'),path=require('path'),z=require('zlib'),assert=require('assert');
const build=path.resolve(process.argv[2]||'.next');
const budgets=JSON.parse(fs.readFileSync(path.join(__dirname,'budgets.json'),'utf8'));
const results=[];
for(const [route,budget] of Object.entries(budgets.routes)){
 const html=fs.readFileSync(path.join(build,'server/app',`${route}.html`),'utf8');
 const scripts=[...new Set([...html.matchAll(/<script[^>]+src="([^"]+)"/g)].map(m=>m[1]))];
 const jsGzip=scripts.reduce((sum,url)=>sum+z.gzipSync(fs.readFileSync(path.join(build,decodeURIComponent(url.replace(/^\/_next\//,''))))).length,0);
 const htmlGzip=z.gzipSync(html).length;
 assert(jsGzip<=budget.jsGzip,`${route}: JS ${jsGzip} > ${budget.jsGzip}; inspect new dependencies before raising the budget`);
 assert(scripts.length<=budget.requests,`${route}: extra blocking script requests`);
 if(htmlGzip>budget.htmlWarning)console.warn(`WARN ${route}: HTML ${htmlGzip} bytes; review content/index growth`);
 if(route.startsWith('albums')){
  const images=[...html.matchAll(/<img[^>]+src="([^"]+)"/g)].map(m=>m[1]);assert(images.length>0,`${route}: missing rendered image`);
  assert(images.every(url=>/^https?:\/\//.test(url)),`${route}: production image should point directly to CDN, not /album-assets redirect`);
 }
 results.push({route,jsGzip,htmlGzip,requests:scripts.length});
}
console.log(JSON.stringify({status:'PERF_BUILD_OK',results},null,2));
