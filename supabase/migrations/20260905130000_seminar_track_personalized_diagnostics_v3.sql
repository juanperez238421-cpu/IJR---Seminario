-- Seminar 11 specialized project diagnostics v3
-- Personalized stage credit for the five project tracks.
-- 4 Theory + Workshop stages. Bank v3 is copied from the QA-reviewed v2 bank,
-- with stage metadata and additional critical gates for cybersecurity/robotics.

alter table public.seminar_track_diagnostic_questions
  add column if not exists stage_no smallint,
  add column if not exists concept_code text,
  add column if not exists critical boolean not null default false;

alter table public.seminar_track_diagnostic_attempts
  add column if not exists studio_profile_id uuid,
  add column if not exists stage_scores jsonb not null default '{}'::jsonb,
  add column if not exists highest_mastered_stage smallint,
  add column if not exists recommended_stage smallint,
  add column if not exists critical_gates jsonb not null default '{}'::jsonb,
  add column if not exists mastery_policy_version text;

do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname='seminar_track_diag_questions_stage_check'
      and conrelid='public.seminar_track_diagnostic_questions'::regclass
  ) then
    alter table public.seminar_track_diagnostic_questions
      add constraint seminar_track_diag_questions_stage_check
      check (stage_no is null or stage_no between 1 and 4);
  end if;

  if not exists (
    select 1 from pg_constraint
    where conname='seminar_track_diag_attempts_stage_check'
      and conrelid='public.seminar_track_diagnostic_attempts'::regclass
  ) then
    alter table public.seminar_track_diagnostic_attempts
      add constraint seminar_track_diag_attempts_stage_check
      check (
        (highest_mastered_stage is null or highest_mastered_stage between 0 and 4)
        and (recommended_stage is null or recommended_stage between 1 and 4)
      );
  end if;

  if not exists (
    select 1 from pg_constraint
    where conname='seminar_track_diag_attempts_profile_fkey'
      and conrelid='public.seminar_track_diagnostic_attempts'::regclass
  ) then
    alter table public.seminar_track_diagnostic_attempts
      add constraint seminar_track_diag_attempts_profile_fkey
      foreign key (studio_profile_id)
      references public.seminar_studio_profiles(id)
      on delete set null;
  end if;
end
$$;

create unique index if not exists seminar_track_diag_question_position_uidx
  on public.seminar_track_diagnostic_questions(track_slug, bank_version, position);

create index if not exists seminar_track_diag_attempt_profile_track_idx
  on public.seminar_track_diagnostic_attempts(studio_profile_id, track_slug, completed_at desc)
  where studio_profile_id is not null;

comment on column public.seminar_track_diagnostic_questions.stage_no is
  'Personalized Theory + Workshop stage 1..4. NULL for self-profile items.';
comment on column public.seminar_track_diagnostic_questions.critical is
  'Safety/authorization gate. Critical items must be correct before a stage can receive prior-knowledge credit.';
comment on column public.seminar_track_diagnostic_attempts.stage_scores is
  'Server-computed per-stage mastery summary. Client code cannot self-declare mastery.';
comment on column public.seminar_track_diagnostic_attempts.studio_profile_id is
  'Private Studio profile resolved from the student edit-token hash for personalized v3 diagnostics.';

delete from public.seminar_track_diagnostic_questions
where bank_version='2026-09-05-v3';

insert into public.seminar_track_diagnostic_questions
  (id,track_slug,position,bank_version,domain,kind,prompt,options,correct_option,scored,stage_no,concept_code,critical)
select
  q.track_slug || '-20260905-v3-' || lpad(q.position::text,2,'0'),
  q.track_slug,
  q.position,
  '2026-09-05-v3',
  q.domain,
  q.kind,
  q.prompt,
  q.options,
  q.correct_option,
  q.scored,
  case when q.scored then (((q.position-1)/3)+1)::smallint else null end,
  case when q.scored then q.track_slug || '-s' || (((q.position-1)/3)+1)::text || '-q' || q.position::text else 'self-profile-' || q.position::text end,
  case
    when q.track_slug='cybersecurity' and q.position in (2,6,9,10,11) then true
    when q.track_slug='robotics' and q.position in (5,6,9,11) then true
    else false
  end
from public.seminar_track_diagnostic_questions q
where q.bank_version='2026-08-31-v2';

-- Make authorization/scope itself a scored gate in Cybersecurity Stage 1.
update public.seminar_track_diagnostic_questions
set
  prompt='¿Cuál escenario es apropiado para las prácticas de este track?',
  options='["Una aplicación propia, un sandbox o un sistema explícitamente autorizado","Un servicio externo real sin permiso","Una cuenta ajena para probar contraseñas","Cualquier red pública disponible"]'::jsonb,
  correct_option=0,
  critical=true,
  concept_code='cybersecurity-s1-authorized-scope'
where track_slug='cybersecurity'
  and bank_version='2026-09-05-v3'
  and position=2;

create or replace function public.seminar_track_diagnostic_get_questions(
  p_track_slug text,
  p_bank_version text
)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
declare
  v_track text := lower(trim(coalesce(p_track_slug,'')));
  v_version text := trim(coalesce(p_bank_version,''));
  v_questions jsonb;
begin
  if v_track not in ('web','data-science','cybersecurity','3d-programming','robotics') then
    raise exception 'invalid_track';
  end if;
  if v_version not in ('2026-08-31-v1','2026-08-31-v2','2026-09-05-v3') then
    raise exception 'invalid_bank_version';
  end if;

  select coalesce(
    jsonb_agg(
      jsonb_build_object(
        'id',q.id,'position',q.position,'stage_no',q.stage_no,
        'domain',q.domain,'kind',q.kind,'prompt',q.prompt,
        'options',q.options,'scored',q.scored
      ) order by q.position
    ),
    '[]'::jsonb
  )
  into v_questions
  from public.seminar_track_diagnostic_questions q
  where q.track_slug=v_track and q.bank_version=v_version;

  if jsonb_array_length(v_questions) <> 15 then
    raise exception 'question_bank_incomplete';
  end if;

  return v_questions;
end;
$$;

create or replace function public.seminar_track_diagnostic_start(
  p_track_slug text,
  p_bank_version text,
  p_full_name text,
  p_group_code text,
  p_attempt_token text,
  p_user_agent text default null
)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
declare
  v_track text := lower(trim(coalesce(p_track_slug,'')));
  v_version text := trim(coalesce(p_bank_version,''));
  v_name text := regexp_replace(trim(coalesce(p_full_name,'')), '\s+', ' ', 'g');
  v_group text := upper(trim(coalesce(p_group_code,'')));
  v_token text := trim(coalesce(p_attempt_token,''));
  v_token_hash text;
  v_profile_id uuid;
  v_id uuid;
  v_started timestamptz;
begin
  if v_track not in ('web','data-science','cybersecurity','3d-programming','robotics') then
    raise exception 'invalid_track';
  end if;
  if v_version not in ('2026-08-31-v1','2026-08-31-v2','2026-09-05-v3') then
    raise exception 'invalid_bank_version';
  end if;
  if char_length(v_token) < 32 or char_length(v_token) > 200 then
    raise exception 'invalid_token';
  end if;

  v_token_hash := encode(extensions.digest(v_token,'sha256'),'hex');

  if v_version='2026-09-05-v3' then
    select p.id,p.full_name,p.group_code
      into v_profile_id,v_name,v_group
    from public.seminar_studio_profiles p
    where p.edit_token_hash=v_token_hash;

    if not found then
      raise exception 'studio_profile_required';
    end if;
  else
    if char_length(v_name) < 3 or char_length(v_name) > 120 then raise exception 'invalid_name'; end if;
    if v_group not in ('11-A','11-B','11-C') then raise exception 'invalid_group'; end if;
  end if;

  if (
    select count(*) from public.seminar_track_diagnostic_questions q
    where q.track_slug=v_track and q.bank_version=v_version
  ) <> 15 then
    raise exception 'question_bank_incomplete';
  end if;

  insert into public.seminar_track_diagnostic_attempts
    (track_slug,bank_version,full_name,group_code,access_token_hash,user_agent,studio_profile_id,mastery_policy_version)
  values
    (v_track,v_version,v_name,v_group,v_token_hash,left(coalesce(p_user_agent,''),500),v_profile_id,
     case when v_version='2026-09-05-v3' then 'stage-mastery-v3' else null end)
  returning id,started_at into v_id,v_started;

  insert into public.seminar_track_diagnostic_events(attempt_id,event_type,payload)
  values (
    v_id,'STARTED',
    jsonb_build_object('track_slug',v_track,'bank_version',v_version,'personalized',v_profile_id is not null)
  );

  return jsonb_build_object(
    'attempt_id',v_id,'track_slug',v_track,'bank_version',v_version,
    'full_name',v_name,'group_code',v_group,'started_at',v_started,
    'status','in_progress','personalized',v_profile_id is not null
  );
end;
$$;

create or replace function public.seminar_track_diagnostic_submit(
  p_attempt_id uuid,
  p_attempt_token text,
  p_answers jsonb
)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
declare
  a public.seminar_track_diagnostic_attempts%rowtype;
  v_total integer;
  v_answered integer;
  v_score integer;
  v_max integer;
  v_percent numeric(5,1);
  v_confidence numeric(5,1);
  v_level text;
  v_domain_scores jsonb;
  v_stage_scores jsonb := '{}'::jsonb;
  v_critical_gates jsonb := '{}'::jsonb;
  v_stage integer;
  v_stage_score integer;
  v_stage_max integer;
  v_stage_percent numeric(5,1);
  v_critical_total integer;
  v_critical_correct integer;
  v_stage_mastered boolean;
  v_contiguous boolean := true;
  v_highest integer := 0;
  v_recommended integer := 1;
begin
  if jsonb_typeof(p_answers) <> 'object' then raise exception 'answers_must_be_object'; end if;
  if octet_length(p_answers::text) > 20000 then raise exception 'answers_too_large'; end if;

  select * into a
  from public.seminar_track_diagnostic_attempts x
  where x.id=p_attempt_id
    and x.access_token_hash=encode(extensions.digest(trim(coalesce(p_attempt_token,'')),'sha256'),'hex')
  for update;

  if not found then raise exception 'attempt_not_found'; end if;

  if a.completed_at is not null then
    return jsonb_build_object(
      'attempt_id',a.id,'track_slug',a.track_slug,'bank_version',a.bank_version,
      'full_name',a.full_name,'group_code',a.group_code,'started_at',a.started_at,
      'completed_at',a.completed_at,'status','completed','score',a.score,'max_score',a.max_score,
      'knowledge_percent',a.knowledge_percent,'confidence_percent',a.confidence_percent,
      'level',a.level,'domain_scores',a.domain_scores,'stage_scores',a.stage_scores,
      'highest_mastered_stage',a.highest_mastered_stage,'recommended_stage',a.recommended_stage,
      'critical_gates',a.critical_gates,'mastery_policy_version',a.mastery_policy_version
    );
  end if;

  select count(*) into v_total
  from public.seminar_track_diagnostic_questions q
  where q.track_slug=a.track_slug and q.bank_version=a.bank_version;

  select count(*) into v_answered
  from public.seminar_track_diagnostic_questions q
  where q.track_slug=a.track_slug and q.bank_version=a.bank_version
    and p_answers ? q.id
    and (p_answers->>q.id) ~ '^[0-9]+$'
    and (p_answers->>q.id)::integer between 0 and jsonb_array_length(q.options)-1;

  if v_total <> 15 or v_answered <> v_total then raise exception 'complete_all_questions'; end if;

  select
    count(*) filter (where q.scored),
    count(*) filter (where q.scored and (p_answers->>q.id)::integer=q.correct_option)
  into v_max,v_score
  from public.seminar_track_diagnostic_questions q
  where q.track_slug=a.track_slug and q.bank_version=a.bank_version;

  v_percent := round((100.0*v_score/greatest(v_max,1))::numeric,1);

  select round(avg(
    ((p_answers->>q.id)::numeric / greatest(jsonb_array_length(q.options)-1,1)::numeric) * 100.0
  ),1)
  into v_confidence
  from public.seminar_track_diagnostic_questions q
  where q.track_slug=a.track_slug and q.bank_version=a.bank_version and not q.scored;

  select coalesce(
    jsonb_object_agg(
      s.domain,
      jsonb_build_object(
        'score',s.score,'max',s.max_score,
        'percent',round((100.0*s.score/greatest(s.max_score,1))::numeric,1)
      )
    ),
    '{}'::jsonb
  )
  into v_domain_scores
  from (
    select q.domain,
      count(*)::integer as max_score,
      count(*) filter (where (p_answers->>q.id)::integer=q.correct_option)::integer as score
    from public.seminar_track_diagnostic_questions q
    where q.track_slug=a.track_slug and q.bank_version=a.bank_version and q.scored
    group by q.domain
  ) s;

  if a.bank_version='2026-09-05-v3' then
    for v_stage in 1..4 loop
      select
        count(*) filter (where q.scored)::integer,
        count(*) filter (where q.scored and (p_answers->>q.id)::integer=q.correct_option)::integer,
        count(*) filter (where q.scored and q.critical)::integer,
        count(*) filter (where q.scored and q.critical and (p_answers->>q.id)::integer=q.correct_option)::integer
      into v_stage_max,v_stage_score,v_critical_total,v_critical_correct
      from public.seminar_track_diagnostic_questions q
      where q.track_slug=a.track_slug and q.bank_version=a.bank_version and q.stage_no=v_stage;

      v_stage_percent := case
        when v_stage_max > 0 then round((100.0*v_stage_score/v_stage_max)::numeric,1)
        else 0
      end;

      v_stage_mastered :=
        v_stage_max=3
        and v_stage_percent >= 66.7
        and v_critical_correct=v_critical_total;

      if v_contiguous and v_stage_mastered then
        v_highest := v_stage;
      else
        v_contiguous := false;
      end if;

      v_stage_scores := v_stage_scores || jsonb_build_object(
        v_stage::text,
        jsonb_build_object(
          'score',v_stage_score,'max',v_stage_max,'percent',v_stage_percent,
          'critical_total',v_critical_total,'critical_correct',v_critical_correct,
          'critical_pass',v_critical_correct=v_critical_total,'mastered',v_stage_mastered
        )
      );

      v_critical_gates := v_critical_gates || jsonb_build_object(
        v_stage::text,
        jsonb_build_object(
          'required',v_critical_total,'passed',v_critical_correct,'ok',v_critical_correct=v_critical_total
        )
      );
    end loop;

    v_recommended := case when v_highest >= 4 then 4 else v_highest + 1 end;
  end if;

  v_level := case
    when v_percent < 35 then 'foundation'
    when v_percent < 60 then 'developing'
    when v_percent < 85 then 'proficient'
    else 'advanced'
  end;

  update public.seminar_track_diagnostic_attempts
  set
    answers=p_answers,domain_scores=v_domain_scores,score=v_score,max_score=v_max,
    knowledge_percent=v_percent,confidence_percent=v_confidence,level=v_level,
    stage_scores=case when a.bank_version='2026-09-05-v3' then v_stage_scores else stage_scores end,
    highest_mastered_stage=case when a.bank_version='2026-09-05-v3' then v_highest else highest_mastered_stage end,
    recommended_stage=case when a.bank_version='2026-09-05-v3' then v_recommended else recommended_stage end,
    critical_gates=case when a.bank_version='2026-09-05-v3' then v_critical_gates else critical_gates end,
    mastery_policy_version=case when a.bank_version='2026-09-05-v3' then 'stage-mastery-v3' else mastery_policy_version end,
    completed_at=now(),
    duration_seconds=greatest(0,extract(epoch from (now()-started_at))::integer),
    updated_at=now()
  where id=a.id;

  insert into public.seminar_track_diagnostic_events(attempt_id,event_type,payload)
  values (
    a.id,'COMPLETED',
    jsonb_build_object(
      'track_slug',a.track_slug,'score',v_score,'max_score',v_max,
      'knowledge_percent',v_percent,'confidence_percent',v_confidence,'level',v_level,
      'highest_mastered_stage',case when a.bank_version='2026-09-05-v3' then v_highest else null end,
      'recommended_stage',case when a.bank_version='2026-09-05-v3' then v_recommended else null end
    )
  );

  return jsonb_build_object(
    'attempt_id',a.id,'track_slug',a.track_slug,'bank_version',a.bank_version,
    'full_name',a.full_name,'group_code',a.group_code,'started_at',a.started_at,
    'completed_at',now(),'status','completed','score',v_score,'max_score',v_max,
    'knowledge_percent',v_percent,'confidence_percent',v_confidence,'level',v_level,
    'domain_scores',v_domain_scores,
    'stage_scores',case when a.bank_version='2026-09-05-v3' then v_stage_scores else '{}'::jsonb end,
    'highest_mastered_stage',case when a.bank_version='2026-09-05-v3' then v_highest else null end,
    'recommended_stage',case when a.bank_version='2026-09-05-v3' then v_recommended else null end,
    'critical_gates',case when a.bank_version='2026-09-05-v3' then v_critical_gates else '{}'::jsonb end,
    'mastery_policy_version',case when a.bank_version='2026-09-05-v3' then 'stage-mastery-v3' else a.mastery_policy_version end
  );
end;
$$;

create or replace function public.seminar_track_diagnostic_snapshot(
  p_attempt_id uuid,
  p_attempt_token text
)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
declare a public.seminar_track_diagnostic_attempts%rowtype;
begin
  select * into a
  from public.seminar_track_diagnostic_attempts x
  where x.id=p_attempt_id
    and x.access_token_hash=encode(extensions.digest(trim(coalesce(p_attempt_token,'')),'sha256'),'hex');

  if not found then raise exception 'attempt_not_found'; end if;

  insert into public.seminar_track_diagnostic_events(attempt_id,event_type,payload)
  values (a.id,'RESUMED',jsonb_build_object('completed',a.completed_at is not null));

  return jsonb_build_object(
    'attempt_id',a.id,'track_slug',a.track_slug,'bank_version',a.bank_version,
    'full_name',a.full_name,'group_code',a.group_code,'started_at',a.started_at,
    'completed_at',a.completed_at,
    'status',case when a.completed_at is null then 'in_progress' else 'completed' end,
    'score',a.score,'max_score',a.max_score,'knowledge_percent',a.knowledge_percent,
    'confidence_percent',a.confidence_percent,'level',a.level,'domain_scores',a.domain_scores,
    'stage_scores',a.stage_scores,'highest_mastered_stage',a.highest_mastered_stage,
    'recommended_stage',a.recommended_stage,'critical_gates',a.critical_gates,
    'mastery_policy_version',a.mastery_policy_version
  );
end;
$$;

create or replace function public.seminar_track_diagnostic_status(
  p_track_slug text,
  p_attempt_token text
)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
declare
  v_track text := lower(trim(coalesce(p_track_slug,'')));
  v_token_hash text := encode(extensions.digest(trim(coalesce(p_attempt_token,'')),'sha256'),'hex');
  v_profile_id uuid;
  a public.seminar_track_diagnostic_attempts%rowtype;
begin
  if v_track not in ('web','data-science','cybersecurity','3d-programming','robotics') then
    raise exception 'invalid_track';
  end if;

  select p.id into v_profile_id
  from public.seminar_studio_profiles p
  where p.edit_token_hash=v_token_hash;

  if not found then raise exception 'studio_profile_required'; end if;

  select * into a
  from public.seminar_track_diagnostic_attempts x
  where x.studio_profile_id=v_profile_id
    and x.track_slug=v_track
    and x.bank_version='2026-09-05-v3'
    and x.completed_at is not null
  order by x.completed_at desc
  limit 1;

  if not found then
    return jsonb_build_object('status','not_started','track_slug',v_track,'bank_version','2026-09-05-v3');
  end if;

  return jsonb_build_object(
    'status','completed','attempt_id',a.id,'track_slug',a.track_slug,'bank_version',a.bank_version,
    'completed_at',a.completed_at,'score',a.score,'max_score',a.max_score,
    'knowledge_percent',a.knowledge_percent,'confidence_percent',a.confidence_percent,
    'level',a.level,'domain_scores',a.domain_scores,'stage_scores',a.stage_scores,
    'highest_mastered_stage',a.highest_mastered_stage,'recommended_stage',a.recommended_stage,
    'critical_gates',a.critical_gates,'mastery_policy_version',a.mastery_policy_version
  );
end;
$$;

create or replace function public.seminar_studio_teacher_dashboard()
returns jsonb
language sql
security definer
set search_path=''
as $$
  select jsonb_build_object(
    'generated_at',clock_timestamp(),
    'released_sprint',coalesce((
      select s.released_sprint
      from public.seminar_studio_settings s
      where s.course_slug='seminar11-software-engineering-studio-2026'
    ),1),
    'release_updated_at',(
      select s.updated_at
      from public.seminar_studio_settings s
      where s.course_slug='seminar11-software-engineering-studio-2026'
    ),
    'students',coalesce(
      jsonb_agg(
        jsonb_build_object(
          'id',p.id,'response_id',p.response_id,'created_at',p.created_at,'updated_at',p.updated_at,
          'last_student_activity_at',p.last_student_activity_at,'teacher_updated_at',p.teacher_updated_at,
          'full_name',p.full_name,'group_code',p.group_code,'topics',p.topics,'first_choice',p.first_choice,
          'track_slug',p.track_slug,'work_mode',p.work_mode,'partner_name',p.partner_name,'project_idea',p.project_idea,
          'project_title',p.project_title,'repo_full_name',p.repo_full_name,'uml_url',p.uml_url,
          'sprint_current',p.sprint_current,'progress_percent',p.progress_percent,'next_goal',p.next_goal,
          'status',p.status,'teacher_note',p.teacher_note,
          'diagnostic',case when d.id is null then null else jsonb_build_object(
            'completed_at',d.completed_at,'knowledge_percent',d.knowledge_percent,
            'confidence_percent',d.confidence_percent,'level',d.level,'stage_scores',d.stage_scores,
            'highest_mastered_stage',d.highest_mastered_stage,'recommended_stage',d.recommended_stage,
            'critical_gates',d.critical_gates,'mastery_policy_version',d.mastery_policy_version
          ) end
        )
        order by p.group_code,p.full_name
      ),
      '[]'::jsonb
    )
  )
  from public.seminar_studio_profiles p
  left join lateral (
    select x.*
    from public.seminar_track_diagnostic_attempts x
    where x.studio_profile_id=p.id
      and x.track_slug=p.track_slug
      and x.bank_version='2026-09-05-v3'
      and x.completed_at is not null
    order by x.completed_at desc
    limit 1
  ) d on true;
$$;

revoke execute on function public.seminar_track_diagnostic_get_questions(text,text) from public, anon, authenticated;
revoke execute on function public.seminar_track_diagnostic_start(text,text,text,text,text,text) from public, anon, authenticated;
revoke execute on function public.seminar_track_diagnostic_submit(uuid,text,jsonb) from public, anon, authenticated;
revoke execute on function public.seminar_track_diagnostic_snapshot(uuid,text) from public, anon, authenticated;
revoke execute on function public.seminar_track_diagnostic_status(text,text) from public, anon, authenticated;

grant execute on function public.seminar_track_diagnostic_get_questions(text,text) to anon, authenticated;
grant execute on function public.seminar_track_diagnostic_start(text,text,text,text,text,text) to anon, authenticated;
grant execute on function public.seminar_track_diagnostic_submit(uuid,text,jsonb) to anon, authenticated;
grant execute on function public.seminar_track_diagnostic_snapshot(uuid,text) to anon, authenticated;
grant execute on function public.seminar_track_diagnostic_status(text,text) to anon, authenticated;

revoke execute on function public.seminar_studio_teacher_dashboard() from public, anon, authenticated;
grant execute on function public.seminar_studio_teacher_dashboard() to service_role;

revoke all on table public.seminar_track_diagnostic_questions from anon, authenticated;
revoke all on table public.seminar_track_diagnostic_attempts from anon, authenticated;
revoke all on table public.seminar_track_diagnostic_events from anon, authenticated;

alter table public.seminar_track_diagnostic_questions enable row level security;
alter table public.seminar_track_diagnostic_attempts enable row level security;
alter table public.seminar_track_diagnostic_events enable row level security;
