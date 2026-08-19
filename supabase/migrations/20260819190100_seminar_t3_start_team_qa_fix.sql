-- QA hardening for the Seminar T3 team-start RPC.
-- The original function used the set-returning alias in trim(...); this replacement
-- addresses the explicit `value` column so name validation works at runtime.

create or replace function public.seminar_course_start_team(
  p_course_slug text,
  p_language text,
  p_student_names jsonb,
  p_group_code text,
  p_session_id uuid,
  p_user_agent text
)
returns jsonb
language plpgsql
security definer
set search_path='public','extensions'
as $$
declare
  a public.seminar_course_attempts%rowtype;
  v_lang text;
  v_group text;
  v_size int;
  v_key text;
  v_label text;
  v_token text;
  duplicate_count int;
begin
  if trim(coalesce(p_course_slug,'')) <> 'seminario-programacion-t3-2026' then
    raise exception 'Unknown course';
  end if;

  v_lang := lower(trim(coalesce(p_language,'')));
  if v_lang not in ('python','java') then raise exception 'Select Python or Java'; end if;

  v_group := upper(trim(coalesce(p_group_code,'')));
  if v_group not in ('11-A','11-B','11-C') then raise exception 'Select a valid group'; end if;

  if p_student_names is null or jsonb_typeof(p_student_names) <> 'array' then
    raise exception 'Provide team members';
  end if;
  v_size := jsonb_array_length(p_student_names);
  if v_size < 1 or v_size > 3 then raise exception 'Register 1 to 3 students'; end if;

  if exists (
    select 1
    from jsonb_array_elements_text(p_student_names) as n(value)
    where length(trim(n.value)) < 2
  ) then
    raise exception 'Write every team member name';
  end if;

  with names as (
    select ord::int as ord,
           regexp_replace(trim(value),'[[:space:]]+',' ','g') as display_name
    from jsonb_array_elements_text(p_student_names) with ordinality t(value,ord)
  ), normalized as (
    select ord,display_name,lower(display_name) normalized_name
    from names
  )
  select string_agg(normalized_name,'|' order by normalized_name),
         string_agg(display_name,' · ' order by ord),
         count(*) - count(distinct normalized_name)
  into v_key,v_label,duplicate_count
  from normalized;

  if duplicate_count > 0 then raise exception 'Do not repeat a name inside one team'; end if;

  v_token := replace(gen_random_uuid()::text,'-','') || replace(gen_random_uuid()::text,'-','');

  select * into a
  from public.seminar_course_attempts
  where course_slug=p_course_slug
    and language=v_lang
    and group_code=v_group
    and team_key=v_key
  order by started_at desc
  limit 1;

  if a.id is null then
    insert into public.seminar_course_attempts(
      course_slug,language,group_code,team_key,team_label,team_size,
      session_id,access_token_hash,user_agent
    ) values (
      p_course_slug,v_lang,v_group,v_key,v_label,v_size,
      coalesce(p_session_id,gen_random_uuid()),
      encode(digest(v_token,'sha256'),'hex'),p_user_agent
    ) returning * into a;
  else
    update public.seminar_course_attempts
    set team_label=v_label,
        team_size=v_size,
        access_token_hash=encode(digest(v_token,'sha256'),'hex'),
        last_activity_at=clock_timestamp(),
        user_agent=coalesce(p_user_agent,user_agent)
    where id=a.id
    returning * into a;
    delete from public.seminar_course_attempt_members where attempt_id=a.id;
  end if;

  insert into public.seminar_course_attempt_members(
    attempt_id,member_order,display_name,normalized_name
  )
  select a.id,
         ord::int,
         regexp_replace(trim(value),'[[:space:]]+',' ','g'),
         lower(regexp_replace(trim(value),'[[:space:]]+',' ','g'))
  from jsonb_array_elements_text(p_student_names) with ordinality t(value,ord);

  insert into public.seminar_course_events(attempt_id,event_type,metadata)
  values(a.id,'TEAM_SESSION_STARTED',jsonb_build_object(
    'language',v_lang,'team_size',v_size,'group_code',v_group
  ));

  return jsonb_build_object(
    'attempt_id',a.id,
    'attempt_token',v_token,
    'snapshot',public.seminar_course_snapshot(a.id,v_token)
  );
end;
$$;

grant execute on function public.seminar_course_start_team(text,text,jsonb,text,uuid,text) to anon,authenticated;
notify pgrst,'reload schema';
