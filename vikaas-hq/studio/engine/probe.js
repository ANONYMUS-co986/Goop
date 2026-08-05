// probe.js <htmlPath> <outPng> [times...] — seek key beats, tile into one sheet.
const path=require('path'), fs=require('fs'), zlib=require('zlib'), cp=require('child_process');
process.env.LD_LIBRARY_PATH='/tmp/al2023/lib'+(process.env.LD_LIBRARY_PATH?':'+process.env.LD_LIBRARY_PATH:'');
const FFMPEG='/home/user/Goop/vikaas-hq/studio/.venv/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2';
function ensure(){ if(fs.existsSync('/tmp/al2023/lib/libnspr4.so'))return; let dir=path.dirname(require.resolve('@sparticuz/chromium')); for(let i=0;i<8&&!fs.existsSync(path.join(dir,'bin','al2023.tar.br'));i++)dir=path.dirname(dir); const br=path.join(dir,'bin','al2023.tar.br'); fs.mkdirSync('/tmp/al2023',{recursive:true}); fs.writeFileSync('/tmp/al2023.tar',zlib.brotliDecompressSync(fs.readFileSync(br))); cp.execSync('tar -xf /tmp/al2023.tar -C /tmp/al2023'); fs.rmSync('/tmp/al2023.tar',{force:true}); }
const _cr=require('@sparticuz/chromium'); const chromium=_cr.default||_cr; const { chromium: pw }=require('playwright-core');
(async()=>{
  ensure();
  const html=process.argv[2], out=process.argv[3]||'probe.png';
  const times=process.argv.slice(4).map(Number);
  const LIST=times.length?times:[0.3,1.2,2.25,3.0,4.8,7.2,9.9,11.9,14.6,16.8,19.6,22.2,23.6,26.2];
  const tmp=fs.mkdtempSync('/tmp/probe_frames_');
  const browser=await pw.launch({args:chromium.args,executablePath:await chromium.executablePath(),headless:true});
  const page=await browser.newPage({viewport:{width:1080,height:1920}});
  page.on('pageerror',e=>console.error('PAGEERROR:',e.message.slice(0,300)));
  page.on('console',m=>{if(m.type()==='error')console.error('CONSOLE:',m.text().slice(0,200));});
  await page.goto('file://'+path.resolve(html),{waitUntil:'load',timeout:60000});
  await page.evaluate(async()=>{if(document.fonts&&document.fonts.ready)await document.fonts.ready;});
  await page.waitForFunction(()=>window.__reel&&typeof window.__reel.seek==='function',null,{timeout:30000});
  for(let i=0;i<LIST.length;i++){
    await page.evaluate((t)=>window.__reel.seek(t),LIST[i]);
    await page.waitForTimeout(120);
    await page.screenshot({path:path.join(tmp,`p${String(i).padStart(2,'0')}.png`)});
  }
  await browser.close();
  const cols=Math.ceil(Math.sqrt(LIST.length*9/16)), rows=Math.ceil(LIST.length/cols);
  const r=cp.spawnSync(FFMPEG,['-y','-framerate','1','-i',path.join(tmp,'p%02d.png'),'-vf',`scale=270:480,tile=${cols}x${rows}`,'-frames:v','1',out],{encoding:'utf8'});
  if(r.status!==0){console.error(r.stderr.slice(-500));process.exit(1);}
  console.log('probe ->',path.resolve(out),listNote());
  function listNote(){return LIST.length+' frames: '+LIST.join(' ');}
})().catch(e=>{console.error('FAIL',e.message);process.exit(1);});
