-- Seminar 11 · Master Team Progress Projection V6
-- Projects canonical OOP/UML team evidence to every roster-matched member
-- without duplicating evidence rows. Progress remains attempt-level and auditable.

create or replace function public.seminar_master_dashboard_v6()
returns jsonb
language sql
stable
set search_path to 'public'
as $function$
with base as (
  select public.seminar_master_dashboard_v5() as payload
),
patched as (
  select
    jsonb_set(
      s,
      '{oop_progress}',
      jsonb_build_object(
        'attempt_id', nullif(s->'course'->>'attempt_id','')::uuid,
        'assignment_mode',
          case when coalesce((s->'course'->>'team_size')::int,1)>1 then 'team' else 'individual' end,
        'team_size', coalesce((s->'course'->>'team_size')::int,1),
        'team_label', coalesce(s->'course'->>'team_label',''),
        'source', 'canonical_course_attempt_members',
        'total_sessions', 10,
        'evidenced_sessions', coalesce(p.evidenced_sessions,0),
        'completed_sessions', coalesce(p.completed_sessions,0),
        'progress_percent', least(100, greatest(0, round(100.0*coalesce(p.completed_sessions,0)/10.0)::int)),
        'uml_verified_sessions', coalesce(p.uml_verified_sessions,0),
        'code_validated_sessions', coalesce(p.code_validated_sessions,0),
        'last_progress_at', p.last_progress_at
      ),
      true
    ) as student_json
  from base
  cross join lateral jsonb_array_elements(base.payload->'students') s
  left join lateral (
    select
      count(distinct os.session_key)::int as evidenced_sessions,
      count(distinct os.session_key) filter (where os.status='completed')::int as completed_sessions,
      count(distinct os.session_key) filter (
        where (os.evidence->>'uml_mastery')::boolean is true
          and (os.evidence->>'uml_visual_mastery')::boolean is true
      )::int as uml_verified_sessions,
      count(distinct os.session_key) filter (
        where (os.evidence->>'run_success')::boolean is true
          and (os.evidence->>'implement_success')::boolean is true
          and (os.evidence->>'test_success')::boolean is true
          and coalesce((os.evidence->>'successful_run_count')::int,0)>0
      )::int as code_validated_sessions,
      max(coalesce(os.completed_at,os.updated_at)) as last_progress_at
    from public.seminar_oop_uml_session_records os
    where os.attempt_id = nullif(s->'course'->>'attempt_id','')::uuid
  ) p on true
),
students_payload as (
  select coalesce(
    jsonb_agg(student_json order by student_json->>'group_code',(student_json->>'source_position')::integer),
    '[]'::jsonb
  ) as students
  from patched
),
quality_patch as (
  select jsonb_build_object(
    'team_attempts_with_oop_evidence',(
      select count(distinct a.id)
      from public.seminar_course_attempts a
      where a.course_slug='seminario-programacion-t3-2026'
        and a.team_size>1
        and exists(select 1 from public.seminar_oop_uml_session_records os where os.attempt_id=a.id)
    ),
    'students_receiving_team_progress',(
      select count(distinct m.student_registry_id)
      from public.seminar_course_attempts a
      join public.seminar_course_attempt_members m on m.attempt_id=a.id
      where a.course_slug='seminario-programacion-t3-2026'
        and a.team_size>1
        and m.student_registry_id is not null
        and exists(select 1 from public.seminar_oop_uml_session_records os where os.attempt_id=a.id)
    ),
    'unmatched_team_members_with_progress',(
      select count(*)
      from public.seminar_course_attempts a
      join public.seminar_course_attempt_members m on m.attempt_id=a.id
      where a.course_slug='seminario-programacion-t3-2026'
        and a.team_size>1
        and m.student_registry_id is null
        and exists(select 1 from public.seminar_oop_uml_session_records os where os.attempt_id=a.id)
    ),
    'cross_group_team_members_with_progress',(
      select count(*)
      from public.seminar_course_attempts a
      join public.seminar_course_attempt_members m on m.attempt_id=a.id
      join public.student_registry r on r.id=m.student_registry_id
      where a.course_slug='seminario-programacion-t3-2026'
        and a.team_size>1
        and exists(select 1 from public.seminar_oop_uml_session_records os where os.attempt_id=a.id)
        and replace(a.group_code,'-','')<>replace(r.group_code,'-','')
    ),
    'team_progress_rule','Progress is projected to every roster-matched member of the canonical stored team attempt; evidence rows are not duplicated.'
  ) as patch
)
select
  (base.payload - 'students' - 'data_quality')
  || jsonb_build_object(
    'students',students_payload.students,
    'data_quality',coalesce(base.payload->'data_quality','{}'::jsonb) || quality_patch.patch,
    'payload_version','seminar_master_dashboard_v6'
  )
from base,students_payload,quality_patch;
$function$;

create or replace function public.seminar_master_code_v1(p_teacher_token text)
returns jsonb
language plpgsql
security definer
set search_path to 'public','private','extensions','pg_catalog'
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
      'payload_version','seminar_master_dashboard_v6'
    )
  );

  return public.seminar_master_dashboard_v6();
end;
$function$;
