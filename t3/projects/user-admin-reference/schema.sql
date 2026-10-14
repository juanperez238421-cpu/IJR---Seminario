-- Additive reference app; does not modify institutional identities or course progress.
create schema if not exists seminar_web_private;
revoke all on schema seminar_web_private from public, anon, authenticated;

create table public.seminar_web_memberships (
  project_slug text not null references public.seminar_student_projects(project_slug) check (project_slug in ('cortes-web-definition','jaramillo-web-definition','velasquez-web-definition','gomez-gta-v-mod-showcase')),
  user_id uuid not null references auth.users(id) on delete cascade,
  role text not null check (role in ('admin','viewer')),
  primary key(project_slug,user_id)
);
alter table public.seminar_web_memberships enable row level security;
create index seminar_web_memberships_user on public.seminar_web_memberships(user_id);
revoke all on public.seminar_web_memberships from anon, authenticated;
grant select on public.seminar_web_memberships to authenticated;
create policy web_membership_own on public.seminar_web_memberships for select to authenticated
using (user_id = (select auth.uid()));

create table public.seminar_web_directory (
  id uuid primary key default gen_random_uuid(),
  project_slug text not null references public.seminar_student_projects(project_slug),
  alias text not null check (char_length(trim(alias)) between 2 and 80),
  contact text not null check (char_length(contact) between 3 and 120 and contact = lower(trim(contact)) and contact ~ '^[^[:space:]@]+@example[.]test$'),
  category text not null default 'member' check (char_length(category) between 1 and 40),
  status text not null default 'active' check (status in ('active','archived')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(project_slug,contact)
);
alter table public.seminar_web_directory enable row level security;
revoke all on public.seminar_web_directory from anon, authenticated;
grant select, insert on public.seminar_web_directory to authenticated;
grant update(alias,contact,category,status) on public.seminar_web_directory to authenticated;
create policy web_directory_read on public.seminar_web_directory for select to authenticated
using (exists (select 1 from public.seminar_web_memberships m where m.project_slug=seminar_web_directory.project_slug and m.user_id=(select auth.uid())));
create policy web_directory_insert on public.seminar_web_directory for insert to authenticated
with check (exists (select 1 from public.seminar_web_memberships m where m.project_slug=seminar_web_directory.project_slug and m.user_id=(select auth.uid()) and m.role='admin'));
create policy web_directory_update on public.seminar_web_directory for update to authenticated
using (exists (select 1 from public.seminar_web_memberships m where m.project_slug=seminar_web_directory.project_slug and m.user_id=(select auth.uid()) and m.role='admin'))
with check (exists (select 1 from public.seminar_web_memberships m where m.project_slug=seminar_web_directory.project_slug and m.user_id=(select auth.uid()) and m.role='admin'));

create table public.seminar_web_directory_events (
  id uuid primary key default gen_random_uuid(),
  project_slug text not null references public.seminar_student_projects(project_slug),
  record_id uuid not null references public.seminar_web_directory(id),
  actor_id uuid not null,
  action text not null,
  occurred_at timestamptz not null default now()
);
create index seminar_web_directory_events_project_time on public.seminar_web_directory_events(project_slug,occurred_at desc);
create index seminar_web_directory_events_record on public.seminar_web_directory_events(record_id);
alter table public.seminar_web_directory_events enable row level security;
revoke all on public.seminar_web_directory_events from anon, authenticated;
grant select on public.seminar_web_directory_events to authenticated;
create policy web_events_admin_read on public.seminar_web_directory_events for select to authenticated
using (exists (select 1 from public.seminar_web_memberships m where m.project_slug=seminar_web_directory_events.project_slug and m.user_id=(select auth.uid()) and m.role='admin'));

-- Trigger alone can write audit events. No personal fields or credentials are logged.
create function seminar_web_private.audit_directory() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  if auth.uid() is null or not exists (
    select 1 from public.seminar_web_memberships where project_slug=new.project_slug and user_id=auth.uid() and role='admin'
  ) then raise exception 'project_admin_required'; end if;
  insert into public.seminar_web_directory_events(project_slug,record_id,actor_id,action)
  values(new.project_slug,new.id,auth.uid(),case when tg_op='INSERT' then 'created' when new.status<>old.status then new.status else 'updated' end);
  return new;
end $$;
revoke all on function seminar_web_private.audit_directory() from public,anon,authenticated;
-- AFTER keeps the audit foreign key valid; timestamps are supplied by a separate invoker trigger.
create function seminar_web_private.touch_directory() returns trigger
language plpgsql security invoker set search_path = '' as $$
begin new.updated_at := now(); return new; end $$;
revoke all on function seminar_web_private.touch_directory() from public,anon,authenticated;
create trigger web_directory_touch before update on public.seminar_web_directory for each row execute function seminar_web_private.touch_directory();
create trigger web_directory_audit after insert or update on public.seminar_web_directory for each row execute function seminar_web_private.audit_directory();
comment on table public.seminar_web_directory is 'Isolated teaching app directory. Synthetic contacts only; these records are not Supabase Auth accounts or institutional students.';
