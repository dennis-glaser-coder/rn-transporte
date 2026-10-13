-- RN BüroPilot / Supabase schema for read-only pilot.
create extension if not exists pgcrypto;
create table if not exists public.rn_staff (
 user_id uuid primary key references auth.users(id) on delete cascade,
 org_id uuid not null,
 role text not null default 'reader' check (role in ('reader','dispatcher','admin')),
 enabled boolean not null default false
);
create table if not exists public.rn_jobs (
 id uuid primary key default gen_random_uuid(),
 org_id uuid not null,
 customer text not null,
 site text not null,
 date date not null,
 start_time time not null,
 pump text not null,
 status text not null default 'Geplant',
 volume_m3 numeric(12,2),
 created_at timestamptz not null default now()
);
create index if not exists rn_jobs_org_date on public.rn_jobs(org_id,date,start_time);
alter table public.rn_staff enable row level security;
alter table public.rn_jobs enable row level security;
revoke all on public.rn_staff from anon,authenticated;
revoke all on public.rn_jobs from anon,authenticated;
grant select on public.rn_staff to authenticated;
grant select on public.rn_jobs to authenticated;
drop policy if exists rn_staff_self on public.rn_staff;
create policy rn_staff_self on public.rn_staff for select to authenticated using (user_id=(select auth.uid()));
drop policy if exists rn_jobs_read on public.rn_jobs;
create policy rn_jobs_read on public.rn_jobs for select to authenticated using (
 exists (
 select 1 from public.rn_staff s
 where s.user_id=(select auth.uid()) and s.org_id=rn_jobs.org_id and s.enabled=true
 )
);
-- This pilot intentionally has no authenticated INSERT / UPDATE / DELETE permissions or policies.
