-- ══════════════════════════════════════════════════════════════
-- SCHEMA CRM Playa Blanca — versión INTERMEDIA (inspirada en Atomic CRM, MIT)
-- Pegar en Supabase → SQL Editor → Run.
-- Tablas: vendedoras · leads · notas · tareas · tags · lead_tags.
-- Profesional pero simple. Seguro de correr varias veces.
-- ══════════════════════════════════════════════════════════════

-- ---------- VENDEDORAS (los "sales") ----------
create table if not exists vendedoras (
  id          uuid primary key default gen_random_uuid(),
  nombre      text not null,
  pin         text unique not null,          -- clave de acceso
  email       text,
  telegram_id text,
  activa      boolean default true,
  creado      timestamptz default now()
);

-- ---------- LEADS (contacto + oportunidad, unificado) ----------
create table if not exists leads (
  id               uuid primary key default gen_random_uuid(),
  creado           timestamptz default now(),
  nombre           text,
  apellido         text,
  email            text,
  telefono         text,
  presupuesto      text,                       -- "$195k–$300k"
  plazo            text,                       -- "6–12 meses"
  proyecto_interes text,                       -- "Aquavista"
  angulo           text,                       -- "Retiro / vida"
  campana          text,
  red              text,
  ad_id            text,
  vendedor_id      uuid references vendedoras(id),
  estado           text default 'nuevo',       -- nuevo/interesado/cita/negociacion/cerrado
  contactado       boolean default false,      -- para follow-up 2h
  origen           text
);

-- ---------- NOTAS (historial por lead) — robado de Atomic ----------
create table if not exists notas (
  id          uuid primary key default gen_random_uuid(),
  lead_id     uuid references leads(id) on delete cascade,
  vendedor_id uuid references vendedoras(id),
  texto       text not null,
  creado      timestamptz default now()
);

-- ---------- TAREAS (con recordatorio) — robado de Atomic ----------
create table if not exists tareas (
  id          uuid primary key default gen_random_uuid(),
  lead_id     uuid references leads(id) on delete cascade,
  vendedor_id uuid references vendedoras(id),
  titulo      text not null,
  vence       timestamptz,                     -- recordatorio
  hecha       boolean default false,
  creado      timestamptz default now()
);

-- ---------- TAGS (etiquetas de color) — robado de Atomic ----------
create table if not exists tags (
  id     uuid primary key default gen_random_uuid(),
  nombre text unique not null,
  color  text default '#6d5ef0'
);
create table if not exists lead_tags (
  lead_id uuid references leads(id) on delete cascade,
  tag_id  uuid references tags(id) on delete cascade,
  primary key (lead_id, tag_id)
);

-- ---------- ÍNDICES ----------
create index if not exists idx_leads_estado   on leads(estado);
create index if not exists idx_leads_vendedor on leads(vendedor_id);
create index if not exists idx_leads_creado    on leads(creado desc);
create index if not exists idx_notas_lead      on notas(lead_id);
create index if not exists idx_tareas_lead     on tareas(lead_id);
create index if not exists idx_tareas_vence    on tareas(vence) where hecha = false;

-- ---------- ROW LEVEL SECURITY ----------
-- RLS ON, sin políticas públicas: el frontend (anon) NO lee directo.
-- Solo el backend (serverless con SERVICE_ROLE) accede y filtra por vendedora.
alter table vendedoras enable row level security;
alter table leads      enable row level security;
alter table notas      enable row level security;
alter table tareas     enable row level security;
alter table tags       enable row level security;
alter table lead_tags  enable row level security;

-- ---------- SEED: 4 vendedoras + tags demo ----------
insert into vendedoras (nombre, pin, email) values
  ('Dyana','1111','dyana@playablanca.demo'),
  ('Carolina','2222','carolina@playablanca.demo'),
  ('Roberto','3333','roberto@playablanca.demo'),
  ('Sofía','4444','sofia@playablanca.demo')
on conflict (pin) do nothing;

insert into tags (nombre, color) values
  ('Retiro','#d97706'), ('Inversión','#2f6dff'),
  ('Familia','#db2777'), ('Vacacional','#0d9488'), ('Caliente','#e5484d')
on conflict (nombre) do nothing;

-- Listo → "Success. No rows returned". Verifica en Table Editor (6 tablas).
