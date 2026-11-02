-- Y2C HOLDINGS private report workspace
-- Run once using Supabase SQL Editor. Never publish password spreadsheets or service_role keys.
create extension if not exists pgcrypto;

create table if not exists public.y2c_admins (
  user_id uuid primary key references auth.users(id) on delete cascade,
  role text not null default 'editor' check (role in ('admin','editor')),
  active boolean not null default true,
  created_at timestamptz not null default now()
);

create table if not exists public.y2c_reports (
  id uuid primary key default gen_random_uuid(),
  created_by uuid not null references auth.users(id),
  title text not null check (char_length(title) between 1 and 200),
  client_name text not null default '',
  target_market text not null default '',
  industry text not null default '',
  status text not null default 'draft' check (status in ('draft','review','final')),
  sections jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists y2c_reports_updated_idx on public.y2c_reports(updated_at desc);

create or replace function public.y2c_update_timestamp() returns trigger
language plpgsql set search_path = '' as $$
begin new.updated_at = now(); return new; end;
$$;
drop trigger if exists y2c_reports_timestamp on public.y2c_reports;
create trigger y2c_reports_timestamp before update on public.y2c_reports
for each row execute function public.y2c_update_timestamp();

alter table public.y2c_admins enable row level security;
alter table public.y2c_reports enable row level security;
revoke all on public.y2c_admins from anon, authenticated;
revoke all on public.y2c_reports from anon, authenticated;
grant select on public.y2c_admins to authenticated;
grant select, insert, update, delete on public.y2c_reports to authenticated;

drop policy if exists "Y2C admins: read self" on public.y2c_admins;
create policy "Y2C admins: read self" on public.y2c_admins
for select to authenticated using (user_id = (select auth.uid()));

drop policy if exists "Y2C reports: approved read" on public.y2c_reports;
create policy "Y2C reports: approved read" on public.y2c_reports
for select to authenticated using (
  exists (select 1 from public.y2c_admins a where a.user_id=(select auth.uid()) and a.active)
);
drop policy if exists "Y2C reports: approved insert" on public.y2c_reports;
create policy "Y2C reports: approved insert" on public.y2c_reports
for insert to authenticated with check (
  created_by=(select auth.uid()) and
  exists (select 1 from public.y2c_admins a where a.user_id=(select auth.uid()) and a.active)
);
drop policy if exists "Y2C reports: approved update" on public.y2c_reports;
create policy "Y2C reports: approved update" on public.y2c_reports
for update to authenticated using (
  exists (select 1 from public.y2c_admins a where a.user_id=(select auth.uid()) and a.active)
) with check (
  exists (select 1 from public.y2c_admins a where a.user_id=(select auth.uid()) and a.active)
);
drop policy if exists "Y2C reports: admin delete" on public.y2c_reports;
create policy "Y2C reports: admin delete" on public.y2c_reports
for delete to authenticated using (
  exists (select 1 from public.y2c_admins a where a.user_id=(select auth.uid()) and a.active and a.role='admin')
);
