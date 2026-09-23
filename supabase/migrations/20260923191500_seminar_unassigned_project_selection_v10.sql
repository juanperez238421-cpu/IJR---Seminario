-- Allow any active Grade 11 student with a registered institutional identity to create\n-- a project from the Project Decision Center when no project row exists yet.\n\ncreate or replace function public.seminar_student_project_save_decision_v2(
  p_student_registry_id uuid,
  p_track_slug text,
  p_choice_key text,
  p_project_title text,
  p_project_summary text,
  p_objective text,
  p_stack text[],
  p_student_note text default null,
  p_ip_hash text default null,
  p_user_agent text default null
)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $function$
declare
  v_before public.seminar_student_projects;
  v_after public.seminar_student_projects;
  v_template public.seminar_student_projects;
  v_roster public.student_registry;
  v_stack text[];
  v_now timestamptz := clock_timestamp();
  v_track text := btrim(coalesce(p_track_slug,''));
  v_slug text;
begin
  if p_student_registry_id is null then
    raise exception 'student_registry_id_required';
  end if;

  if v_track not in ('web','data-science','cybersecurity','3d-programming','robotics') then
    raise exception 'invalid_track_slug';
  end if;

  if p_choice_key is null
     or p_choice_key !~ '^[a-z0-9][a-z0-9-]{1,79}$' then
    raise exception 'invalid_choice_key';
  end if;

  if p_project_title is null
     or char_length(btrim(p_project_title)) < 3
     or char_length(btrim(p_project_title)) > 180 then
    raise exception 'invalid_project_title';
  end if;

  if p_project_summary is null
     or char_length(btrim(p_project_summary)) < 10
     or char_length(btrim(p_project_summary)) > 1600 then
    raise exception 'invalid_project_summary';
  end if;

  if p_objective is null
     or char_length(btrim(p_objective)) < 10
     or char_length(btrim(p_objective)) > 1200 then
    raise exception 'invalid_objective';
  end if;

  if p_student_note is not null and char_length(btrim(p_student_note)) > 1200 then
    raise exception 'invalid_student_note';
  end if;

  select coalesce(array_agg(btrim(x)), '{}'::text[])
    into v_stack
  from unnest(coalesce(p_stack, '{}'::text[])) as x
  where btrim(x) <> '';

  if coalesce(array_length(v_stack, 1), 0) > 12
     or exists (
       select 1
       from unnest(v_stack) as x
       where char_length(x) > 80
     ) then
    raise exception 'invalid_stack';
  end if;

  select *
    into v_before
  from public.seminar_student_projects
  where student_registry_id = p_student_registry_id
  for update;

  if found then
    if v_track <> v_before.track_slug then
      raise exception 'track_change_not_allowed';
    end if;

    update public.seminar_student_projects
    set project_title = btrim(p_project_title),
        project_summary = btrim(p_project_summary),
        objective = btrim(p_objective),
        stack = v_stack,
        student_choice_key = p_choice_key,
        student_decision_note = nullif(btrim(p_student_note), ''),
        student_decided_at = v_now,
        student_revision_count = student_revision_count + 1,
        decision_status = 'confirmed',
        confirmed_at = v_now,
        assignment_status = case
          when assignment_status = 'assigned' then 'active'
          else assignment_status
        end,
        updated_at = v_now
    where student_registry_id = p_student_registry_id
    returning * into v_after;
  else
    select *
      into v_roster
    from public.student_registry
    where id = p_student_registry_id
      and active = true
      and group_code in ('11A','11B','11C')
    for share;

    if not found then
      raise exception 'student_not_eligible';
    end if;

    select *
      into v_template
    from public.seminar_student_projects
    where track_slug = v_track
    order by case when project_mode = 'guided_definition' then 0 else 1 end,
             created_at asc
    limit 1;

    if not found then
      raise exception 'track_template_not_found';
    end if;

    v_slug := 'student-project-' || substr(replace(p_student_registry_id::text,'-',''),1,12);

    insert into public.seminar_student_projects(
      student_registry_id,
      group_code,
      student_name,
      project_slug,
      track_slug,
      project_title,
      project_summary,
      objective,
      stack,
      source_kind,
      source_ref,
      safety_scope,
      sprints,
      assignment_status,
      teacher_note,
      decision_status,
      decision_note,
      confirmed_at,
      project_mode,
      definition_questions,
      initial_project_title,
      initial_project_summary,
      initial_objective,
      initial_stack,
      student_choice_key,
      student_decision_note,
      student_decided_at,
      student_revision_count,
      content_sections,
      created_at,
      updated_at
    ) values (
      p_student_registry_id,
      v_roster.group_code,
      v_roster.display_name,
      v_slug,
      v_track,
      btrim(p_project_title),
      btrim(p_project_summary),
      btrim(p_objective),
      v_stack,
      'student',
      'Selección del estudiante desde Project Decision Center',
      v_template.safety_scope,
      v_template.sprints,
      'active',
      null,
      'confirmed',
      null,
      v_now,
      'guided_definition',
      v_template.definition_questions,
      btrim(p_project_title),
      btrim(p_project_summary),
      btrim(p_objective),
      v_stack,
      p_choice_key,
      nullif(btrim(p_student_note), ''),
      v_now,
      1,
      v_template.content_sections,
      v_now,
      v_now
    )
    returning * into v_after;
  end if;

  insert into public.seminar_project_decision_events(
    student_registry_id,
    choice_key,
    revision_number,
    previous_project,
    new_project,
    student_note,
    ip_hash,
    user_agent
  ) values (
    p_student_registry_id,
    p_choice_key,
    v_after.student_revision_count,
    case
      when v_before.student_registry_id is null then '{}'::jsonb
      else to_jsonb(v_before)
    end,
    to_jsonb(v_after),
    nullif(btrim(p_student_note), ''),
    nullif(btrim(p_ip_hash), ''),
    nullif(left(p_user_agent, 1000), '')
  );

  return jsonb_build_object(
    'ok', true,
    'student_registry_id', v_after.student_registry_id,
    'track_slug', v_after.track_slug,
    'project_title', v_after.project_title,
    'project_summary', v_after.project_summary,
    'objective', v_after.objective,
    'stack', v_after.stack,
    'student_choice_key', v_after.student_choice_key,
    'student_decision_note', v_after.student_decision_note,
    'student_decided_at', v_after.student_decided_at,
    'student_revision_count', v_after.student_revision_count,
    'decision_status', v_after.decision_status,
    'confirmed_at', v_after.confirmed_at,
    'created_new_project', v_before.student_registry_id is null,
    'updated_at', v_after.updated_at
  );
end;
$function$;

revoke all on function public.seminar_student_project_save_decision_v2(
  uuid,text,text,text,text,text,text[],text,text,text
) from public, anon, authenticated;

grant execute on function public.seminar_student_project_save_decision_v2(
  uuid,text,text,text,text,text,text[],text,text,text
) to service_role;\n