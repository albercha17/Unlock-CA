-- Tabla de partidas de Unlock C&A (tiempos y aventuras completadas).
-- Se ejecuta UNA vez en Supabase: proyecto «Supervivencia» → SQL Editor → New query → pegar todo → Run.
-- Es seguro repetirlo (usa IF NOT EXISTS). Cada persona solo ve y crea sus propias partidas (RLS).

create table if not exists public.unlock_partidas (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid not null default auth.uid() references auth.users (id) on delete cascade,
  cliente_id  text not null,                       -- id que genera el móvil: evita duplicados al sincronizar
  juego       text not null,                       -- faro, egipto, marte, florencia, dinosaurios, cuento, trono...
  tiempo_seg  integer not null check (tiempo_seg >= 0),
  pistas      integer not null default 0,
  cartas      integer not null default 0,
  completada  boolean not null default true,
  informe     text,
  fin         timestamptz not null default now(),
  unique (user_id, cliente_id)
);

create index if not exists unlock_partidas_user_juego on public.unlock_partidas (user_id, juego, tiempo_seg);

alter table public.unlock_partidas enable row level security;

drop policy if exists "partidas: ver las mias" on public.unlock_partidas;
create policy "partidas: ver las mias" on public.unlock_partidas
  for select using (auth.uid() = user_id);

drop policy if exists "partidas: guardar las mias" on public.unlock_partidas;
create policy "partidas: guardar las mias" on public.unlock_partidas
  for insert with check (auth.uid() = user_id);

drop policy if exists "partidas: borrar las mias" on public.unlock_partidas;
create policy "partidas: borrar las mias" on public.unlock_partidas
  for delete using (auth.uid() = user_id);
