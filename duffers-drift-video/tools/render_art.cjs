// Render tools/art/*.html to images in assets/art/ (run after gen_art.py).
// Sand tables become JPEGs; everything with transparency becomes PNG.
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const artDir = path.join(root, "tools/art");
const outDir = path.join(root, "assets/art");
fs.mkdirSync(outDir, { recursive: true });

(async () => {
  const browser = await chromium.launch();
  const only = process.argv.slice(2);
  for (const file of fs.readdirSync(artDir).filter((f) => f.endsWith(".html"))) {
    const name = file.replace(/\.html$/, "");
    if (only.length && !only.includes(name)) continue;
    const html = fs.readFileSync(path.join(artDir, file), "utf8");
    const w = +html.match(/width:(\d+)px/)[1];
    const h = +html.match(/height:(\d+)px/)[1];
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1.5 });
    await page.goto("file://" + path.join(artDir, file));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    const opaque = name.startsWith("sand-");
    const out = path.join(outDir, `${name}.${opaque ? "jpg" : "png"}`);
    await page.screenshot({ path: out, type: opaque ? "jpeg" : "png", quality: opaque ? 88 : undefined, omitBackground: !opaque });
    console.log(name, (fs.statSync(out).size / 1024).toFixed(0) + "KB");
    await page.close();
  }
  await browser.close();
})();
