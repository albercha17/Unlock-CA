-- Pedidos de la tienda (tienda/index.html): packs de 4 aventuras personalizadas con fotos de los protagonistas.
-- Se ejecuta UNA vez en Supabase: proyecto de «Noches de Cine» (tomwaoskswxfbwxsrkkl) → SQL Editor → New query → pegar todo → Run.
-- Es seguro repetirlo. El público solo puede CREAR pedidos y SUBIR fotos: no puede leer ni borrar nada.
-- Los pedidos se ven en Table Editor → tienda_pedidos, y las fotos en Storage → tienda-fotos/<id del pedido>/.

create table if not exists public.tienda_pedidos (
  id             uuid primary key,                          -- lo genera la web (así las fotos van a tienda-fotos/<id>/)
  creado         timestamptz not null default now(),
  estado         text not null default 'nuevo',             -- nuevo → pagado → en_produccion → entregado (o cancelado)
  nombre         text not null check (char_length(nombre) between 1 and 120),
  email          text not null check (email ~* '^[^@\s]+@[^@\s]+\.[^@\s]+$' and char_length(email) <= 200),
  telefono       text check (char_length(telefono) <= 40),
  aventuras      text[] not null check (cardinality(aventuras) = 4),
  protagonistas  jsonb not null,                            -- [{nombre, edad, sobre, fotos: ["<id>/p1-1.jpg", ...]}, ...]
  formato        text not null check (formato in ('digital', 'impreso')),
  precio         integer not null check (precio between 0 and 1000),   -- euros, el que vio el cliente
  ocasion        text check (char_length(ocasion) <= 60),
  fecha_deseada  date,
  dedicatoria    text check (char_length(dedicatoria) <= 600),
  direccion      text check (char_length(direccion) <= 400),
  notas          text check (char_length(notas) <= 1500),
  acepta         boolean not null check (acepta)
);

alter table public.tienda_pedidos enable row level security;

drop policy if exists "tienda: crear pedidos" on public.tienda_pedidos;
create policy "tienda: crear pedidos" on public.tienda_pedidos
  for insert to anon, authenticated
  with check (estado = 'nuevo');

-- Fotos: bucket PRIVADO (nadie las ve desde fuera), máx. 6 MB por foto y solo imágenes.
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('tienda-fotos', 'tienda-fotos', false, 6291456, array['image/jpeg', 'image/png', 'image/webp'])
on conflict (id) do update set public = false, file_size_limit = excluded.file_size_limit, allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists "tienda: subir fotos" on storage.objects;
create policy "tienda: subir fotos" on storage.objects
  for insert to anon, authenticated
  with check (bucket_id = 'tienda-fotos');
