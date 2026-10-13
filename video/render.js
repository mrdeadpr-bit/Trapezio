// Renderiza quadros da cena 3D no Chromium (Playwright), servindo os arquivos por HTTP local.
// uso: node render.js <inicio> <fim>     (quadros [inicio, fim))   env: PLAYWRIGHT_PATH
const { chromium } = require(process.env.PLAYWRIGHT_PATH || "playwright");
const http = require("http"), path = require("path"), fs = require("fs");
const ROOT = __dirname, THREE_DIR = path.join(ROOT, "node_modules", "three");
const TYPES = { ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript", ".json": "application/json" };

function serve() {
  return new Promise(res => {
    const s = http.createServer((req, rsp) => {
      let p = decodeURIComponent(req.url.split("?")[0]);
      const f = p.startsWith("/three/") ? path.join(THREE_DIR, p.slice(7)) : path.join(ROOT, p);
      fs.readFile(f, (e, d) => { if (e) { rsp.writeHead(404); rsp.end(); } else { rsp.writeHead(200, { "content-type": TYPES[path.extname(f)] || "application/octet-stream" }); rsp.end(d); } });
    }).listen(0, "127.0.0.1", () => res(s));
  });
}

(async () => {
  const list = process.argv[2].includes(",") ? process.argv[2].split(",").map(Number) : null;
  const [a, b] = list ? [0, list.length] : [+process.argv[2], +process.argv[3]];
  const out = path.join(ROOT, "work", "frames"); fs.mkdirSync(out, { recursive: true });
  const server = await serve(); const port = server.address().port;
  const browser = await chromium.launch({ args: ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on("pageerror", e => console.error("pageerror:", e.message));
  page.on("console", m => { if (m.type() === "error") console.error("console:", m.text()); });
  await page.goto(`http://127.0.0.1:${port}/scene/index.html${process.env.QS || ''}`);
  await page.waitForFunction("window.READY === true", null, { timeout: 60000 });
  const fps = await page.evaluate("window.TIMELINE.fps");
  for (let n = a; n < b; n++) {
    const i = list ? list[n] : n;
    await page.evaluate(t => window.setT(t), i / fps);
    await page.screenshot({ path: path.join(out, `f${String(i).padStart(5, "0")}.jpg`), type: "jpeg", quality: 93 });
  }
  await browser.close(); server.close();
})();
