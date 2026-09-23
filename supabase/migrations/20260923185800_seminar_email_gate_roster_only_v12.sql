create or replace function public.seminar_email_access_v1(p_email text)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $function$
declare
  v_email text := lower(btrim(coalesce(p_email, '')));
  v_group text;
begin
  if char_length(v_email) > 254
     or v_email !~ '^[^[:space:]@]+@ijr[.]edu[.]co$' then
    return jsonb_build_object('ok', false, 'error', 'institutional_email_required');
  end if;

  select sr.group_code
    into v_group
  from public.python_hub_student_identities psi
  join public.student_registry sr on sr.id = psi.student_registry_id
  where lower(btrim(psi.institutional_email)) = v_email
    and sr.active is true
    and sr.group_code in ('11A','11B','11C','11-A','11-B','11-C')
  limit 1;

  if v_group is null then
    return jsonb_build_object('ok', false, 'error', 'institutional_email_not_registered');
  end if;

  return jsonb_build_object('ok', true, 'email', v_email);
end;
$function$;

revoke all on function public.seminar_email_access_v1(text) from public;
grant execute on function public.seminar_email_access_v1(text) to anon, authenticated, service_role;

comment on function public.seminar_email_access_v1(text) is
'Seminar 11 student-page gate. Accepts only active Grade 11 institutional emails present in the official roster; returns only ok/email and no private roster data.';
