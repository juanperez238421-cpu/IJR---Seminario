alter table public.seminar_student_projects
  add column if not exists decision_status text not null default 'proposed'
    check (decision_status in ('proposed','confirmed','revise','rejected')),
  add column if not exists decision_note text,
  add column if not exists confirmed_at timestamptz;

update public.seminar_student_projects
set decision_status = 'proposed',
    decision_note = coalesce(decision_note, 'Proyecto específico propuesto para definición con el estudiante el 23 de septiembre de 2026.'),
    confirmed_at = null
where decision_status is distinct from 'confirmed';

create index if not exists seminar_student_projects_decision_idx
  on public.seminar_student_projects(decision_status, group_code, student_name);

create or replace function public.seminar_studio_teacher_dashboard()
returns jsonb
language sql
security definer
set search_path=''
as $fn$
select jsonb_build_object(
  'generated_at', clock_timestamp(),
  'students', coalesce((
    select jsonb_agg(jsonb_build_object(
      'id',p.id,'response_id',p.response_id,'created_at',p.created_at,'updated_at',p.updated_at,
      'last_student_activity_at',p.last_student_activity_at,'teacher_updated_at',p.teacher_updated_at,
      'full_name',p.full_name,'group_code',p.group_code,'topics',p.topics,'first_choice',p.first_choice,
      'track_slug',p.track_slug,'work_mode',p.work_mode,'partner_name',p.partner_name,'project_idea',p.project_idea,
      'project_title',p.project_title,'repo_full_name',p.repo_full_name,'uml_url',p.uml_url,
      'sprint_current',p.sprint_current,'progress_percent',p.progress_percent,'next_goal',p.next_goal,
      'status',p.status,'teacher_note',p.teacher_note,'student_registry_id',p.student_registry_id
    ) order by p.group_code,p.full_name)
    from public.seminar_studio_profiles p
  ), '[]'::jsonb),
  'assignments', coalesce((
    select jsonb_agg(jsonb_build_object(
      'student_registry_id',a.student_registry_id,'group_code',a.group_code,'student_name',a.student_name,
      'project_slug',a.project_slug,'track_slug',a.track_slug,'project_title',a.project_title,
      'project_summary',a.project_summary,'objective',a.objective,'stack',a.stack,
      'source_kind',a.source_kind,'source_ref',a.source_ref,'safety_scope',a.safety_scope,
      'sprints',a.sprints,'assignment_status',a.assignment_status,'teacher_note',a.teacher_note,
      'decision_status',a.decision_status,'decision_note',a.decision_note,'confirmed_at',a.confirmed_at,
      'updated_at',a.updated_at
    ) order by a.group_code,a.student_name)
    from public.seminar_student_projects a
  ), '[]'::jsonb)
);
$fn$;

revoke execute on function public.seminar_studio_teacher_dashboard() from public, anon, authenticated;
grant execute on function public.seminar_studio_teacher_dashboard() to service_role;
