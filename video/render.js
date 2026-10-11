// Renderiza os quadros da cena 3D com o Chromium (Playwright).
// uso: node render.js <inicio> <fim> [dpr]   (quadros [inicio, fim))
const { chromium } = require(process.env.PLAYWRIGHT_PATH || "playwright");
const path = require("path"), fs = require("fs");
(async () => {
  const [a, b] = [+process.argv[2], +process.argv[3]];
  const dpr = process.argv[4] || "1.5";
  const out = path.join(__dirname, "work", "frames"); fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ args: ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--allow-file-access-from-files"] });
  const page = await browser.newPage({ viewport: { width: 720, height: 1280 } });
  await page.goto("file://" + path.join(__dirname, "scene", "index.html") + "?dpr=" + dpr);
  await page.waitForFunction("window.READY === true");
  const fps = await page.evaluate("TL.fps");
  for (let i = a; i < b; i++) {
    await page.evaluate(t => window.setT(t), i / fps);
    await page.screenshot({ path: path.join(out, `f${String(i).padStart(5, "0")}.jpg`), type: "jpeg", quality: 93 });
  }
  await browser.close();
})();
