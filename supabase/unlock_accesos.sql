-- Accesos a los juegos por usuario (la app ya no enseña todo a todo el mundo: cada cuenta ve los juegos que le das).
-- Se ejecuta UNA vez en Supabase (proyecto de «Noches de Cine», tomwaoskswxfbwxsrkkl) → SQL Editor → New query → pegar todo → Run.
-- Requiere tienda_admin.sql (usa public.es_admin_tienda()). Es seguro repetirlo.
--
-- Quién ve qué:
--   · Los administradores (public.tienda_admins) ven TODOS los juegos con Cristina y Alberto, como siempre.
--   · El resto de cuentas solo ven las filas de esta tabla con su correo (y solo si el correo está confirmado).
-- Los accesos se dan por correo, así que se pueden dar antes de que el cliente cree su cuenta.
-- Se gestionan desde tienda/accesos.html (o el botón «Dar acceso» de un pedido en tienda/admin.html).

create table if not exists public.unlock_accesos (
  id        uuid primary key default gen_random_uuid(),
  email     text not null check (email = lower(email) and email ~ '^[^@\s]+@[^@\s]+\.[^@\s]+$'),
  juego     text not null,                    -- id del catálogo: egipto, marte, faro...
  url       text not null default '',         -- web del juego personalizado (pack de Netlify); vacío = el juego normal
  portada   text not null default '',         -- imagen de la portada personalizada; vacío = la normal
  quienes   text not null default '',         -- «Bea y Rubén»: se enseña en el menú del cliente
  pedido_id uuid references public.tienda_pedidos (id) on delete set null,
  creado    timestamptz not null default now(),
  unique (email, juego, url)
);

create index if not exists unlock_accesos_email on public.unlock_accesos (email);

-- correo de la sesión, solo si está confirmado (así nadie se registra con el correo de otro para ver sus juegos)
create or replace function public.unlock_mi_correo()
returns text language sql stable security definer set search_path = public, auth as $$
  select lower(u.email) from auth.users u where u.id = auth.uid() and u.email_confirmed_at is not null;
$$;
grant execute on function public.unlock_mi_correo() to authenticated;

alter table public.unlock_accesos enable row level security;

drop policy if exists "accesos: ver los mios" on public.unlock_accesos;
create policy "accesos: ver los mios" on public.unlock_accesos
  for select to authenticated using (email = public.unlock_mi_correo() or public.es_admin_tienda());

drop policy if exists "accesos: admin crea" on public.unlock_accesos;
create policy "accesos: admin crea" on public.unlock_accesos
  for insert to authenticated with check (public.es_admin_tienda());

drop policy if exists "accesos: admin cambia" on public.unlock_accesos;
create policy "accesos: admin cambia" on public.unlock_accesos
  for update to authenticated using (public.es_admin_tienda()) with check (public.es_admin_tienda());

drop policy if exists "accesos: admin borra" on public.unlock_accesos;
create policy "accesos: admin borra" on public.unlock_accesos
  for delete to authenticated using (public.es_admin_tienda());
