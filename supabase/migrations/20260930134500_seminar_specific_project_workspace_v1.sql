-- Specific Project Workspace v1
-- Persistent per-unit progress + Master panel projection.

create table if not exists public.seminar_project_unit_progress (
  student_registry_id uuid not null references public.student_registry(id) on delete cascade,
  project_slug text not null references public.seminar_student_projects(project_slug) on delete cascade,
  unit_no smallint not null check (unit_no between 1 and 12),
  status text not null default 'not_started' check (status in ('not_started','in_progress','completed')),
  theory_viewed boolean not null default false,
  workshop_started boolean not null default false,
  gate_passed boolean not null default false,
  checklist jsonb not null default '{}'::jsonb,
  evidence_note text,
  evidence_url text,
  repo_ref text,
  started_at timestamptz,
  completed_at timestamptz,
  updated_at timestamptz not null default clock_timestamp(),
  primary key (student_registry_id, project_slug, unit_no),
  constraint seminar_project_unit_progress_checklist_object
    check (jsonb_typeof(checklist)='object'),
  constraint seminar_project_unit_progress_evidence_note_len
    check (evidence_note is null or char_length(evidence_note) <= 2000),
  constraint seminar_project_unit_progress_evidence_url_len
    check (evidence_url is null or char_length(evidence_url) <= 1000),
  constraint seminar_project_unit_progress_repo_ref_len
    check (repo_ref is null or char_length(repo_ref) <= 300)
);

create index if not exists seminar_project_unit_progress_student_idx
  on public.seminar_project_unit_progress(student_registry_id, updated_at desc);
create index if not exists seminar_project_unit_progress_project_idx
  on public.seminar_project_unit_progress(project_slug, unit_no);

alter table public.seminar_project_unit_progress enable row level security;
revoke all on table public.seminar_project_unit_progress from public, anon, authenticated;
grant select, insert, update, delete on table public.seminar_project_unit_progress to service_role;

comment on table public.seminar_project_unit_progress is
'Tracked per-student progress for the Seminar 11 Specific Project Workspace. Browser clients access it only through constrained Edge Functions / teacher master payloads.';

create or replace function public.seminar_master_dashboard_v4()
returns jsonb
language sql
stable
set search_path = 'public'
as $function$
with base as (
  select public.seminar_master_dashboard_v3() as payload
),
patched as (
  select
    s as student_json,
    (
      select jsonb_build_object(
        'project_slug',p.project_slug,
        'track_slug',p.track_slug,
        'project_title',p.project_title,
        'project_mode',p.project_mode,
        'assignment_status',p.assignment_status,
        'decision_status',p.decision_status,
        'unit_count',greatest(0,jsonb_array_length(coalesce(p.sprints,'[]'::jsonb))),
        'completed_units',coalesce((
          select count(*) from public.seminar_project_unit_progress up
          where up.student_registry_id=p.student_registry_id
            and up.project_slug=p.project_slug
            and up.gate_passed=true
        ),0),
        'started_units',coalesce((
          select count(*) from public.seminar_project_unit_progress up
          where up.student_registry_id=p.student_registry_id
            and up.project_slug=p.project_slug
            and (up.workshop_started=true or up.theory_viewed=true or up.status<>'not_started')
        ),0),
        'progress_percent',
          case
            when jsonb_array_length(coalesce(p.sprints,'[]'::jsonb))=0 then 0
            else round(
              100.0 * coalesce((
                select count(*) from public.seminar_project_unit_progress up
                where up.student_registry_id=p.student_registry_id
                  and up.project_slug=p.project_slug
                  and up.gate_passed=true
              ),0)
              / jsonb_array_length(coalesce(p.sprints,'[]'::jsonb))
            )::int
          end,
        'current_unit',
          case
            when jsonb_array_length(coalesce(p.sprints,'[]'::jsonb))=0 then null
            else coalesce((
              select gs
              from generate_series(1,jsonb_array_length(coalesce(p.sprints,'[]'::jsonb))) gs
              where not exists (
                select 1 from public.seminar_project_unit_progress up
                where up.student_registry_id=p.student_registry_id
                  and up.project_slug=p.project_slug
                  and up.unit_no=gs
                  and up.gate_passed=true
              )
              order by gs
              limit 1
            ),jsonb_array_length(coalesce(p.sprints,'[]'::jsonb)))
          end,
        'last_activity_at',greatest(
          p.updated_at,
          coalesce((
            select max(up.updated_at) from public.seminar_project_unit_progress up
            where up.student_registry_id=p.student_registry_id
              and up.project_slug=p.project_slug
          ),'-infinity'::timestamptz)
        ),
        'units',coalesce((
          select jsonb_agg(jsonb_build_object(
            'unit_no',up.unit_no,
            'status',up.status,
            'theory_viewed',up.theory_viewed,
            'workshop_started',up.workshop_started,
            'gate_passed',up.gate_passed,
            'checklist',up.checklist,
            'evidence_note',up.evidence_note,
            'evidence_url',up.evidence_url,
            'repo_ref',up.repo_ref,
            'updated_at',up.updated_at,
            'completed_at',up.completed_at
          ) order by up.unit_no)
          from public.seminar_project_unit_progress up
          where up.student_registry_id=p.student_registry_id
            and up.project_slug=p.project_slug
        ),'[]'::jsonb)
      )
      from public.seminar_student_projects p
      where p.student_registry_id=(s->>'student_registry_id')::uuid
      limit 1
    ) as specific_project
  from base, jsonb_array_elements(base.payload->'students') s
),
students_payload as (
  select coalesce(
    jsonb_agg(
      case
        when specific_project is null then student_json
        else jsonb_set(student_json,'{specific_project}',specific_project,true)
      end
      order by student_json->>'group_code', (student_json->>'source_position')::integer
    ),
    '[]'::jsonb
  ) students
  from patched
)
select
  (base.payload - 'students')
  || jsonb_build_object(
    'students',students_payload.students,
    'payload_version','seminar_master_dashboard_v4'
  )
from base,students_payload;
$function$;

revoke all on function public.seminar_master_dashboard_v4() from public;
grant execute on function public.seminar_master_dashboard_v4() to service_role;

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
    jsonb_build_object(
      'source','seminar/t3/teacher',
      'payload_version','seminar_master_dashboard_v4'
    )
  );

  return public.seminar_master_dashboard_v4();
end;
$function$;
