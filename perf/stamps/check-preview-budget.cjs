const fs=require('fs'),path=require('path'),assert=require('assert'),crypto=require('crypto');
const root=process.cwd(),build=path.resolve(process.argv[2]||'.next');
const manifest=JSON.parse(fs.readFileSync(path.join(root,'data/stamp-preview-manifest.json'),'utf8'));
const original=JSON.parse(fs.readFileSync(path.join(root,'data/image-manifest.json'),'utf8'));
let before=0,after=0;const inverse=new Map();
for(const [source,item] of Object.entries(manifest)){
 assert(original[source],`Unknown source ${source}`);
 assert(/^\/images\/stamp-previews\/\d{4}\/.+\.[a-f0-9]{16}\.webp$/.test(item.preview),`Invalid preview ${source}`);
 assert(item.width>0&&item.height>0&&Math.max(item.width,item.height)<=640,`Oversized preview ${source}`);
 assert(item.bytes>0&&item.bytes<item.sourceBytes*.9,`Preview not smaller: ${source}`);
 assert(/^[a-f0-9]{64}$/.test(item.sourceSha256),`Missing source fingerprint ${source}`);
 inverse.set(item.preview,source);before+=item.sourceBytes;after+=item.bytes;
 const local=path.join(root,'image-store',item.preview); // This optional local check is absent on the hosted build.
 if(fs.existsSync(path.join(root,'image-store'))){assert(fs.statSync(local).size===item.bytes,`Missing or stale local preview ${source}`);const hash=crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'image-store',source))).digest('hex');assert(hash===item.sourceSha256,`Original changed: regenerate previews for ${source}`);}
}
let used=0;
for(const route of ['stamps','years/2026']){
 const html=fs.readFileSync(path.join(build,'server/app',route+'.html'),'utf8');
 const imgs=[...html.matchAll(/<img[^>]+src="([^"]+)"/g)].map(m=>decodeURIComponent(new URL(m[1],'https://local').pathname).replace(/^\/gh\/willieweigz\/fangcunji-images@main/,''));
 for(const image of imgs){if(image.includes('/stamp-previews/')){assert(inverse.has(image),`Unknown rendered preview ${image}`);used++;}else assert(!manifest[image],`${route} bypassed existing preview for ${image}`);}
}
assert(used>0,'No previews in fresh build');
for(const file of fs.readdirSync(path.join(build,'static/chunks'),{recursive:true}).filter(f=>f.endsWith('.js'))){assert(!fs.readFileSync(path.join(build,'static/chunks',file),'utf8').includes('sourceSha256'),'Preview manifest leaked into client JavaScript');}
console.log(JSON.stringify({status:'STAMP_PREVIEW_BUDGET_OK',previews:Object.keys(manifest).length,before,after,reduction:1-after/before,checkedRenderedImages:used},null,2));
