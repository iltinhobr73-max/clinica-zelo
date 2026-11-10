const { chromium } = require('playwright');
const out = process.argv[2]; const pages = (process.argv[3]||'index').split(',');
(async () => {
  const b = await chromium.launch();
  for (const [tag, vp] of [['m', {width:390,height:844}], ['d', {width:1440,height:900}]]) {
    const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: 1 });
    const p = await ctx.newPage();
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    for (const name of pages) {
      await p.goto(`http://localhost:8765/${name}.html`, { waitUntil: 'load' });
      await p.evaluate(async () => { document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-in')); document.querySelectorAll('img').forEach(i=>i.loading='eager'); await document.fonts.ready; });
      await p.waitForTimeout(600); await p.evaluate(() => Promise.all([...document.images].map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; }))));
      const ov = await p.evaluate(() => { const w = document.documentElement.clientWidth; const bad=[]; document.querySelectorAll('body *').forEach(e=>{const r=e.getBoundingClientRect(); if(r.width>0 && (r.right>w+1||r.left<-1) && !e.closest('.toc') && !e.closest('.menu') && !e.closest('.skip') && !e.classList.contains('vh')) bad.push(e.tagName+'.'+e.className+' '+Math.round(r.left)+'-'+Math.round(r.right));}); return {sw: document.documentElement.scrollWidth, w, bad: bad.slice(0,8)}; });
      console.log(tag, name, JSON.stringify(ov), errs.join('|'));
      const h = await p.evaluate(() => document.documentElement.scrollHeight);
      const step = tag==='m' ? 2600 : 2200;
      for (let y=0, i=0; y<h; y+=step, i++) await p.screenshot({ path: `${out}/${name}-${tag}-${i}.png`, fullPage: true, clip: {x:0,y,width:vp.width,height:Math.min(step,h-y)} });
    }
    await ctx.close();
  }
  await b.close();
})();
