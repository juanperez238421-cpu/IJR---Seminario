create or replace function public.seminar_student_project_decide(
  p_student_registry_id uuid,
  p_decision_status text,
  p_decision_note text default null
) returns jsonb
language plpgsql
security definer
set search_path=''
as $fn$
declare
  v_row public.seminar_student_projects;
begin
  if p_decision_status not in ('proposed','confirmed','revise','rejected') then
    raise exception 'invalid_decision_status';
  end if;

  update public.seminar_student_projects
  set decision_status = p_decision_status,
      decision_note = case
        when p_decision_note is null then decision_note
        else nullif(btrim(p_decision_note),'')
      end,
      confirmed_at = case
        when p_decision_status = 'confirmed' then clock_timestamp()
        else null
      end,
      updated_at = clock_timestamp()
  where student_registry_id = p_student_registry_id
  returning * into v_row;

  if not found then
    raise exception 'student_project_not_found';
  end if;

  return jsonb_build_object(
    'ok', true,
    'student_registry_id', v_row.student_registry_id,
    'decision_status', v_row.decision_status,
    'decision_note', v_row.decision_note,
    'confirmed_at', v_row.confirmed_at,
    'updated_at', v_row.updated_at
  );
end;
$fn$;

revoke execute on function public.seminar_student_project_decide(uuid,text,text)
  from public, anon, authenticated;
grant execute on function public.seminar_student_project_decide(uuid,text,text)
  to service_role;
