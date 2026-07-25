// Login por PIN. POST {pin} → devuelve la vendedora si el PIN es válido.
const { sb } = require("../lib/db");

function readBody(req) {
  return new Promise((resolve) => {
    let d = "";
    req.on("data", (c) => (d += c));
    req.on("end", () => { try { resolve(d ? JSON.parse(d) : {}); } catch { resolve({}); } });
  });
}

module.exports = async (req, res) => {
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") return res.status(405).json({ error: "usa POST" });
  try {
    const { pin } = await readBody(req);
    const clean = String(pin || "").trim();
    if (!clean) return res.status(400).json({ error: "falta PIN" });
    const vs = await sb(
      `vendedoras?select=id,nombre&pin=eq.${encodeURIComponent(clean)}&activa=eq.true`
    );
    if (!vs.length) return res.status(401).json({ error: "PIN inválido" });
    res.status(200).json({ vendedora: vs[0] });
  } catch (e) {
    res.status(500).json({ error: String(e.message || e) });
  }
};
