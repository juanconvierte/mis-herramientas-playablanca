const fs = require("fs");
// cargar .env
fs.readFileSync(__dirname + "/.env", "utf8").split("\n").forEach((l) => {
  const m = l.match(/^([A-Z_]+)=(.+)$/);
  if (m && m[2] && !m[2].startsWith("#")) process.env[m[1]] = m[2].trim();
});
const { createLead, listLeads } = require("./lib/leads");
(async () => {
  console.log("→ creando lead de prueba con auto-asignación...");
  const r = await createLead({
    nombre: "PRUEBA", apellido: "Sistema", email: "prueba@test.com",
    telefono: "+50700000000", presupuesto: "$300k–$500k", plazo: "6–12 meses",
    proyecto_interes: "Aquavista", angulo: "Retiro / vida", origen: "test-sistema",
  });
  console.log("✓ lead creado:", r.lead.id.slice(0,8), "→ asignado a:", r.vendedora?.nombre);
  const all = await listLeads();
  console.log("✓ total leads en la base:", all.length);
  console.log("✓ últimos:", all.slice(0,3).map(l => `${l.nombre} ${l.apellido||""} [${l.estado}] → ${l.vendedoras?.nombre||"sin asignar"}`));
})().catch((e) => { console.error("✗ ERROR:", e.message); process.exit(1); });
