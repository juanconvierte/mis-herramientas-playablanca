// Siembra leads de PRUEBA (origen "seed") para ver el Kanban con datos. Se borran luego.
const fs = require("fs");
fs.readFileSync(__dirname + "/.env", "utf8").split("\n").forEach((l) => {
  const m = l.match(/^([A-Z_]+)=(.+)$/);
  if (m && m[2] && !m[2].startsWith("#")) process.env[m[1]] = m[2].trim();
});
const { createLead, updateLead } = require("./lib/leads");
const data = [
  { nombre: "Marta", apellido: "Pérez", presupuesto: "+$500k", proyecto_interes: "Terrazas Villas", angulo: "Retiro / vida", estado: "nuevo" },
  { nombre: "Zoraida", apellido: "Martínez", presupuesto: "$195k–$300k", proyecto_interes: "Aquavista", angulo: "Retiro / vida", estado: "interesado" },
  { nombre: "Ricardo", apellido: "Herrera", presupuesto: "$195k–$300k", proyecto_interes: "Aquavista", angulo: "Inversión / futuro", estado: "interesado" },
  { nombre: "Dumas", apellido: "Rodríguez", presupuesto: "$300k–$500k", proyecto_interes: "Coral Park", angulo: "Inversión / futuro", estado: "cita" },
  { nombre: "Alberto", apellido: "Gómez", presupuesto: "$300k–$500k", proyecto_interes: "Ocean Two", angulo: "Familia / laguna", estado: "negociacion" },
  { nombre: "Elena", apellido: "Torres", presupuesto: "$195k–$300k", proyecto_interes: "Aquavista", angulo: "Retiro / vida", estado: "cerrado" },
];
(async () => {
  for (const d of data) {
    const { estado, ...fields } = d;
    const r = await createLead({ ...fields, email: fields.nombre.toLowerCase() + "@lead.com", telefono: "+507", plazo: "6–12 meses", origen: "seed" });
    if (estado !== "nuevo") await updateLead(r.lead.id, { estado });
    console.log(`✓ ${d.nombre} ${d.apellido} [${estado}] → ${r.vendedora?.nombre}`);
  }
  console.log("seed listo");
})().catch((e) => { console.error("ERR", e.message); process.exit(1); });
