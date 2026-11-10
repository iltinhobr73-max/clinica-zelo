const { chromium } = require('playwright');
(async () => { const b = await chromium.launch();
  for (const [tag, vp, dsf] of [['desktop', {width:1440,height:900}, 1], ['celular', {width:390,height:844}, 2]]) {
    const p = await (await b.newContext({ viewport: vp, deviceScaleFactor: dsf })).newPage();
    await p.goto('http://localhost:8765/index.html', { waitUntil: 'load' });
    await p.evaluate(async () => { document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-in')); document.querySelectorAll('img').forEach(i=>i.loading='eager'); const d=document.querySelector('.dock'); if(d) d.style.display='none'; await document.fonts.ready; await Promise.all([...document.images].map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; }))); });
    await p.waitForTimeout(500);
    await p.screenshot({ path: `previa/inicio-${tag}.png`, fullPage: true });
  }
  await b.close(); })();
