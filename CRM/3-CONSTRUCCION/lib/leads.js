// Lógica de leads: crear (con auto-asignación round-robin), listar, actualizar.
const { sb } = require("./db");

// Round-robin justo: asigna a la vendedora ACTIVA con menos leads.
async function pickVendedora() {
  const vs = await sb("vendedoras?select=id,nombre,telegram_id&activa=eq.true");
  if (!vs.length) return null;
  const leads = await sb("leads?select=vendedor_id");
  const tally = {};
  vs.forEach((v) => (tally[v.id] = 0));
  leads.forEach((l) => {
    if (l.vendedor_id && tally[l.vendedor_id] != null) tally[l.vendedor_id]++;
  });
  vs.sort((a, b) => tally[a.id] - tally[b.id]);
  return vs[0];
}

// Crea un lead y lo asigna solo. Devuelve el lead + la vendedora asignada.
async function createLead(data) {
  const v = await pickVendedora();
  const row = { ...data, vendedor_id: v ? v.id : null, estado: "nuevo", contactado: false };
  const created = await sb("leads", {
    method: "POST",
    body: row,
    headers: { Prefer: "return=representation" },
  });
  return { lead: created[0], vendedora: v };
}

// Lista todos los leads con el nombre de su vendedora.
async function listLeads() {
  return sb("leads?select=*,vendedoras(nombre)&order=creado.desc");
}

// Lista solo los leads de una vendedora (por su id).
async function listLeadsByVendedora(vendedorId) {
  return sb(`leads?select=*,vendedoras(nombre)&vendedor_id=eq.${vendedorId}&order=creado.desc`);
}

// Actualiza un lead (estado, notas, vendedor, contactado...).
async function updateLead(id, patch) {
  const upd = await sb(`leads?id=eq.${id}`, {
    method: "PATCH",
    body: patch,
    headers: { Prefer: "return=representation" },
  });
  return upd[0];
}

module.exports = { pickVendedora, createLead, listLeads, listLeadsByVendedora, updateLead };
