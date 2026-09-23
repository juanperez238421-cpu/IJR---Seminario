create or replace function public.seminar_oop_uml_start_email_v8(
  p_institutional_email text,
  p_language text default 'python',
  p_session_id uuid default gen_random_uuid(),
  p_user_agent text default null
)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_email text := lower(btrim(coalesce(p_institutional_email, '')));
  v_language text := lower(btrim(coalesce(p_language, 'python')));
  v_name text;
  v_group text;
  v_group_course text;
  v_registry_id uuid;
  v_result jsonb;
begin
  if v_email !~ '^[^[:space:]@]+@ijr[.]edu[.]co$' then
    raise exception 'institutional_email_required';
  end if;
  if v_language not in ('python','java') then
    raise exception 'invalid_language';
  end if;
  select psi.student_registry_id, coalesce(sr.display_name, psi.display_name), sr.group_code
    into v_registry_id, v_name, v_group
  from public.python_hub_student_identities psi
  join public.student_registry sr on sr.id = psi.student_registry_id
  where lower(btrim(psi.institutional_email)) = v_email and sr.active is true
  limit 1;
  if v_registry_id is null then
    raise exception 'institutional_email_not_registered';
  end if;
  v_group_course := case v_group
    when '11A' then '11-A'
    when '11B' then '11-B'
    when '11C' then '11-C'
    else v_group
  end;
  if v_group_course not in ('11-A','11-B','11-C') then
    raise exception 'invalid_student_group';
  end if;
  v_result := public.seminar_course_start_team(
    'seminario-programacion-t3-2026',
    v_language,
    jsonb_build_array(v_name),
    v_group_course,
    coalesce(p_session_id, gen_random_uuid()),
    p_user_agent
  );
  return v_result || jsonb_build_object('institutional_email', v_email, 'student_registry_id', v_registry_id);
end;
$$;
revoke all on function public.seminar_oop_uml_start_email_v8(text,text,uuid,text) from public;
grant execute on function public.seminar_oop_uml_start_email_v8(text,text,uuid,text) to anon, authenticated, service_role;
