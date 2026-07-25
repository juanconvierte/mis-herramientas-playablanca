// API de leads (serverless Vercel). GET lista · POST crea+asigna · PATCH actualiza.
const { createLead, listLeads, updateLead } = require("../lib/leads");

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
  try {
    if (req.method === "GET") {
      return res.status(200).json(await listLeads());
    }
    if (req.method === "POST") {
      const body = await readBody(req);
      const result = await createLead(body);
      // TODO Fase 2: disparar aviso Telegram + correo Resend aquí.
      return res.status(200).json(result);
    }
    if (req.method === "PATCH") {
      const body = await readBody(req);
      const { id, ...patch } = body;
      if (!id) return res.status(400).json({ error: "falta id" });
      return res.status(200).json(await updateLead(id, patch));
    }
    res.status(405).json({ error: "método no permitido" });
  } catch (e) {
    res.status(500).json({ error: String(e.message || e) });
  }
};
