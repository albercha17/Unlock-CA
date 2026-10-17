-- Panel de pedidos (tienda/admin.html), producción automática y avisos por correo. Requiere tienda_pedidos.sql.
-- Se ejecuta UNA vez en Supabase (proyecto de «Noches de Cine», tomwaoskswxfbwxsrkkl) → SQL Editor. Es seguro repetirlo.
--
-- Después, a mano (no va en el repo porque son datos privados):
--   insert into public.tienda_admins (email) values ('TU_CORREO') on conflict do nothing;
--   select vault.create_secret('re_...', 'resend_api_key');        -- clave de Resend (avisos por correo)
--   select vault.create_secret('TU_CORREO', 'tienda_aviso_email');  -- a quién avisar
--
-- Estados de un pedido: nuevo → pagado → desarrollar → en_produccion → listo → entregado (o cancelado).
-- «desarrollar» lo pone el botón del panel; el programa de producción (herramientas/tienda/produccion.py)
-- lo recoge, va escribiendo «progreso» y al terminar deja «listo» con la web del pack en «entrega_url».

alter table public.tienda_pedidos
  add column if not exists progreso    text,
  add column if not exists entrega_url text,
  add column if not exists actualizado timestamptz not null default now();

alter table public.tienda_pedidos drop constraint if exists tienda_pedidos_estado_check;
alter table public.tienda_pedidos add constraint tienda_pedidos_estado_check
  check (estado in ('nuevo', 'pagado', 'desarrollar', 'en_produccion', 'listo', 'entregado', 'cancelado'));

-- ---------- quién es administrador ----------
create table if not exists public.tienda_admins (email text primary key);
alter table public.tienda_admins enable row level security;   -- sin políticas: nadie la lee desde fuera

create or replace function public.es_admin_tienda()
returns boolean language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.tienda_admins where lower(email) = lower(coalesce(auth.jwt() ->> 'email', '')));
$$;
grant execute on function public.es_admin_tienda() to authenticated, anon;

-- ---------- permisos del panel ----------
drop policy if exists "tienda: admin ve pedidos" on public.tienda_pedidos;
create policy "tienda: admin ve pedidos" on public.tienda_pedidos
  for select to authenticated using (public.es_admin_tienda());

drop policy if exists "tienda: admin cambia pedidos" on public.tienda_pedidos;
create policy "tienda: admin cambia pedidos" on public.tienda_pedidos
  for update to authenticated using (public.es_admin_tienda()) with check (public.es_admin_tienda());

drop policy if exists "tienda: admin borra pedidos" on public.tienda_pedidos;
create policy "tienda: admin borra pedidos" on public.tienda_pedidos
  for delete to authenticated using (public.es_admin_tienda());

drop policy if exists "tienda: admin ve fotos" on storage.objects;
create policy "tienda: admin ve fotos" on storage.objects
  for select to authenticated using (bucket_id = 'tienda-fotos' and public.es_admin_tienda());

drop policy if exists "tienda: admin borra fotos" on storage.objects;
create policy "tienda: admin borra fotos" on storage.objects
  for delete to authenticated using (bucket_id = 'tienda-fotos' and public.es_admin_tienda());

create or replace function public.tienda_tocar() returns trigger language plpgsql as $$
begin new.actualizado := now(); return new; end $$;
drop trigger if exists tienda_tocar on public.tienda_pedidos;
create trigger tienda_tocar before update on public.tienda_pedidos for each row execute function public.tienda_tocar();

-- ---------- avisos por correo (Resend) ----------
create extension if not exists pg_net with schema extensions;

create or replace function public.tienda_esc(t text) returns text language sql immutable as $$
  select replace(replace(replace(coalesce(t, ''), '&', '&amp;'), '<', '&lt;'), '>', '&gt;');
$$;

create or replace function public.tienda_avisar() returns trigger
language plpgsql security definer set search_path = public, extensions as $$
declare
  clave   text;
  destino text;
  codigo  text := upper(left(new.id::text, 8));
  panel   text := 'https://albercha17.github.io/Unlock-CA/tienda/admin.html#' || new.id;
  protas  text;
  asunto  text;
  html    text;
begin
  if tg_op = 'UPDATE' and not (new.estado = 'listo' and old.estado is distinct from 'listo') then
    return new;
  end if;
  select decrypted_secret into clave from vault.decrypted_secrets where name = 'resend_api_key';
  select decrypted_secret into destino from vault.decrypted_secrets where name = 'tienda_aviso_email';
  if clave is null or destino is null then return new; end if;

  select string_agg(tienda_esc(p ->> 'nombre'), ' y ') into protas from jsonb_array_elements(new.protagonistas) p;

  if tg_op = 'INSERT' then
    asunto := 'Nuevo pedido ' || codigo || ' · ' || new.precio || ' € · ' || new.nombre;
    html := '<h2>Nuevo pedido ' || codigo || '</h2>'
      || '<p><b>Cliente:</b> ' || tienda_esc(new.nombre) || ' &lt;' || tienda_esc(new.email) || '&gt;'
      || coalesce(' · ' || tienda_esc(new.telefono), '') || '</p>'
      || '<p><b>Protagonistas:</b> ' || coalesce(protas, '—') || '</p>'
      || '<p><b>Aventuras:</b> ' || array_to_string(new.aventuras, ', ') || '</p>'
      || '<p><b>Formato:</b> ' || new.formato || ' · <b>' || new.precio || ' €</b></p>'
      || coalesce('<p><b>Ocasión:</b> ' || tienda_esc(new.ocasion) || '</p>', '')
      || coalesce('<p><b>Para el:</b> ' || to_char(new.fecha_deseada, 'DD/MM/YYYY') || '</p>', '')
      || coalesce('<p><b>Dedicatoria:</b> ' || tienda_esc(new.dedicatoria) || '</p>', '')
      || coalesce('<p><b>Notas:</b> ' || tienda_esc(new.notas) || '</p>', '')
      || '<p><a href="' || panel || '">Abrir en el panel de pedidos</a></p>';
  else
    asunto := 'Pack listo ' || codigo || ' · ' || new.nombre;
    html := '<h2>El pack ' || codigo || ' está listo</h2>'
      || '<p>Protagonistas: ' || coalesce(protas, '—') || '</p>'
      || coalesce('<p><a href="' || tienda_esc(new.entrega_url) || '">Ver el pack terminado</a></p>', '')
      || '<p>Revísalo y mándaselo a ' || tienda_esc(new.email) || '. <a href="' || panel || '">Abrir en el panel</a></p>';
  end if;

  perform net.http_post(
    url     := 'https://api.resend.com/emails',
    headers := jsonb_build_object('Authorization', 'Bearer ' || clave, 'Content-Type', 'application/json'),
    body    := jsonb_build_object('from', 'Cronoportal <onboarding@resend.dev>', 'to', jsonb_build_array(destino),
                                  'reply_to', new.email, 'subject', asunto, 'html', html));
  return new;
exception when others then
  return new;   -- un fallo del aviso nunca debe impedir guardar un pedido
end $$;

drop trigger if exists tienda_avisar on public.tienda_pedidos;
create trigger tienda_avisar after insert or update of estado on public.tienda_pedidos
  for each row execute function public.tienda_avisar();
