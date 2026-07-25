// Cliente Supabase vía REST — sin dependencias (usa fetch nativo de Node/Vercel).
// Usa SERVICE_ROLE: SOLO en el backend (funciones serverless). Nunca en el navegador.
const URL = process.env.SUPABASE_URL;
const KEY = process.env.SUPABASE_SERVICE_ROLE;

async function sb(path, { method = "GET", body, headers = {} } = {}) {
  const r = await fetch(`${URL}/rest/v1/${path}`, {
    method,
    headers: {
      apikey: KEY,
      Authorization: `Bearer ${KEY}`,
      "Content-Type": "application/json",
      ...headers,
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await r.text();
  let data;
  try { data = text ? JSON.parse(text) : null; } catch { data = text; }
  if (!r.ok) throw new Error(`Supabase ${r.status}: ${text}`);
  return data;
}

module.exports = { sb };
