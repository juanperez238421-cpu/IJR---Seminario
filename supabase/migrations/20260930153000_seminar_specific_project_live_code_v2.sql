-- Specific Project Live Code v2
-- Persistent project source files, browser runtime verification and per-unit code snapshots.

create table if not exists public.seminar_project_code_files (
  student_registry_id uuid not null references public.student_registry(id) on delete cascade,
  project_slug text not null references public.seminar_student_projects(project_slug) on delete cascade,
  file_key text not null,
  language text not null check (language in ('python','html','css','javascript','openscad','json','markdown','text')),
  content text not null default '',
  revision integer not null default 1 check (revision >= 1),
  last_unit_no smallint not null check (last_unit_no between 1 and 12),
  last_run_ok boolean not null default false,
  last_run_at timestamptz,
  last_run_output text,
  content_sha256 text,
  created_at timestamptz not null default clock_timestamp(),
  updated_at timestamptz not null default clock_timestamp(),
  primary key (student_registry_id, project_slug, file_key),
  constraint seminar_project_code_files_key_format
    check (
      char_length(file_key) between 1 and 120
      and file_key ~ '^[A-Za-z0-9][A-Za-z0-9._/-]*$'
      and position('..' in file_key) = 0
      and left(file_key,1) <> '/'
    ),
  constraint seminar_project_code_files_content_len check (char_length(content) <= 120000),
  constraint seminar_project_code_files_output_len check (last_run_output is null or char_length(last_run_output) <= 10000),
  constraint seminar_project_code_files_sha check (content_sha256 is null or content_sha256 ~ '^[a-f0-9]{64}$')
);

create table if not exists public.seminar_project_code_runtime (
  student_registry_id uuid not null references public.student_registry(id) on delete cascade,
  project_slug text not null references public.seminar_student_projects(project_slug) on delete cascade,
  runtime_kind text not null check (runtime_kind in ('web','python-browser','python-syntax','source')),
  run_count integer not null default 0 check (run_count >= 0),
  successful_run_count integer not null default 0 check (successful_run_count >= 0 and successful_run_count <= run_count),
  last_run_ok boolean not null default false,
  last_run_output text,
  last_run_error text,
  last_run_at timestamptz,
  bundle_sha256 text,
  last_unit_no smallint check (last_unit_no is null or last_unit_no between 1 and 12),
  updated_at timestamptz not null default clock_timestamp(),
  primary key (student_registry_id, project_slug),
  constraint seminar_project_code_runtime_output_len check (last_run_output is null or char_length(last_run_output) <= 10000),
  constraint seminar_project_code_runtime_error_len check (last_run_error is null or char_length(last_run_error) <= 10000),
  constraint seminar_project_code_runtime_sha check (bundle_sha256 is null or bundle_sha256 ~ '^[a-f0-9]{64}$')
);

create table if not exists public.seminar_project_code_snapshots (
  student_registry_id uuid not null references public.student_registry(id) on delete cascade,
  project_slug text not null references public.seminar_student_projects(project_slug) on delete cascade,
  unit_no smallint not null check (unit_no between 1 and 12),
  files jsonb not null default '[]'::jsonb,
  runtime jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default clock_timestamp(),
  updated_at timestamptz not null default clock_timestamp(),
  primary key (student_registry_id, project_slug, unit_no),
  constraint seminar_project_code_snapshots_files_array check (jsonb_typeof(files)='array'),
  constraint seminar_project_code_snapshots_runtime_object check (jsonb_typeof(runtime)='object')
);

create index if not exists seminar_project_code_files_project_idx on public.seminar_project_code_files(project_slug, updated_at desc);
create index if not exists seminar_project_code_files_student_idx on public.seminar_project_code_files(student_registry_id, updated_at desc);
create index if not exists seminar_project_code_snapshots_project_idx on public.seminar_project_code_snapshots(project_slug, unit_no);

alter table public.seminar_project_code_files enable row level security;
alter table public.seminar_project_code_runtime enable row level security;
alter table public.seminar_project_code_snapshots enable row level security;

revoke all on table public.seminar_project_code_files from public, anon, authenticated;
revoke all on table public.seminar_project_code_runtime from public, anon, authenticated;
revoke all on table public.seminar_project_code_snapshots from public, anon, authenticated;
grant select,insert,update,delete on table public.seminar_project_code_files to service_role;
grant select,insert,update,delete on table public.seminar_project_code_runtime to service_role;
grant select,insert,update,delete on table public.seminar_project_code_snapshots to service_role;

comment on table public.seminar_project_code_files is
'Current student-owned source files for the Seminar 11 Specific Project live coding workspace. Access is mediated by the constrained seminar-project-access Edge Function.';
comment on table public.seminar_project_code_runtime is
'Latest browser-runtime verification state for each Specific Project code workspace.';
comment on table public.seminar_project_code_snapshots is
'Per-unit code snapshots captured when a Specific Project unit gate is passed.';

create or replace function public.seminar_master_dashboard_v5()
returns jsonb
language sql
stable
set search_path = 'public'
as $function$
with base as (
  select public.seminar_master_dashboard_v4() as payload
),
patched as (
  select
    case
      when not (s ? 'specific_project') then s
      else jsonb_set(
        s,
        '{specific_project,code}',
        jsonb_build_object(
          'file_count',(select count(*) from public.seminar_project_code_files f where f.student_registry_id=(s->>'student_registry_id')::uuid and f.project_slug=s->'specific_project'->>'project_slug'),
          'latest_revision',coalesce((select max(f.revision) from public.seminar_project_code_files f where f.student_registry_id=(s->>'student_registry_id')::uuid and f.project_slug=s->'specific_project'->>'project_slug'),0),
          'last_code_saved_at',(select max(f.updated_at) from public.seminar_project_code_files f where f.student_registry_id=(s->>'student_registry_id')::uuid and f.project_slug=s->'specific_project'->>'project_slug'),
          'runtime_kind',(select r.runtime_kind from public.seminar_project_code_runtime r where r.student_registry_id=(s->>'student_registry_id')::uuid and r.project_slug=s->'specific_project'->>'project_slug'),
          'run_count',coalesce((select r.run_count from public.seminar_project_code_runtime r where r.student_registry_id=(s->>'student_registry_id')::uuid and r.project_slug=s->'specific_project'->>'project_slug'),0),
          'successful_run_count',coalesce((select r.successful_run_count from public.seminar_project_code_runtime r where r.student_registry_id=(s->>'student_registry_id')::uuid and r.project_slug=s->'specific_project'->>'project_slug'),0),
          'last_run_ok',coalesce((select r.last_run_ok from public.seminar_project_code_runtime r where r.student_registry_id=(s->>'student_registry_id')::uuid and r.project_slug=s->'specific_project'->>'project_slug'),false),
          'last_run_at',(select r.last_run_at from public.seminar_project_code_runtime r where r.student_registry_id=(s->>'student_registry_id')::uuid and r.project_slug=s->'specific_project'->>'project_slug'),
          'last_unit_no',(select r.last_unit_no from public.seminar_project_code_runtime r where r.student_registry_id=(s->>'student_registry_id')::uuid and r.project_slug=s->'specific_project'->>'project_slug'),
          'snapshot_count',(select count(*) from public.seminar_project_code_snapshots cs where cs.student_registry_id=(s->>'student_registry_id')::uuid and cs.project_slug=s->'specific_project'->>'project_slug')
        ),
        true
      )
    end as student_json
  from base, jsonb_array_elements(base.payload->'students') s
),
students_payload as (
  select coalesce(
    jsonb_agg(student_json order by student_json->>'group_code',(student_json->>'source_position')::integer),
    '[]'::jsonb
  ) students
  from patched
)
select
  (base.payload - 'students')
  || jsonb_build_object(
    'students',students_payload.students,
    'payload_version','seminar_master_dashboard_v5'
  )
from base,students_payload;
$function$;

revoke all on function public.seminar_master_dashboard_v5() from public,anon,authenticated;
grant execute on function public.seminar_master_dashboard_v5() to service_role;

create or replace function public.seminar_master_code_v1(p_teacher_token text)
returns jsonb
language plpgsql
security definer
set search_path = 'public', 'private', 'extensions', 'pg_catalog'
as $function$
declare
  v_sid uuid;
begin
  v_sid := public.teacher_code_session_id(p_teacher_token);
  if v_sid is null then
    raise exception 'Sesión docente inválida o expirada';
  end if;

  insert into public.teacher_code_audit(teacher_session_id, action_type, metadata)
  values (
    v_sid,
    'SEMINAR_MASTER_VIEW',
    jsonb_build_object('source','seminar/t3/teacher','payload_version','seminar_master_dashboard_v5')
  );

  return public.seminar_master_dashboard_v5();
end;
$function$;
