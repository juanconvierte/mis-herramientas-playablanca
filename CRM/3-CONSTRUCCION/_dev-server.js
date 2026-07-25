// Servidor local SOLO para probar (no es producción). Carga .env, sirve la UI y las APIs.
const http = require("http"), fs = require("fs");
fs.readFileSync(__dirname + "/.env", "utf8").split("\n").forEach((l) => {
  const m = l.match(/^([A-Z_]+)=(.+)$/);
  if (m && m[2] && !m[2].startsWith("#")) process.env[m[1]] = m[2].trim();
});
const leadsApi = require("./api/leads"), loginApi = require("./api/login");
function shim(res) {
  res.status = (c) => { res.statusCode = c; return res; };
  res.json = (o) => { res.setHeader("Content-Type", "application/json"); res.end(JSON.stringify(o)); return res; };
  return res;
}
http.createServer((req, res) => {
  shim(res);
  const u = req.url.split("?")[0];
  if (u === "/api/leads") return leadsApi(req, res);
  if (u === "/api/login") return loginApi(req, res);
  if (u === "/" || u === "/index.html") { res.setHeader("Content-Type", "text/html; charset=utf-8"); return res.end(fs.readFileSync(__dirname + "/index.html")); }
  res.statusCode = 404; res.end("not found");
}).listen(8795, () => console.log("dev server http://127.0.0.1:8795"));
