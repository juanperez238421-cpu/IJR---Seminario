create or replace function public.seminar_email_access_v1(p_email text)
returns jsonb
language plpgsql
security invoker
set search_path = ''
as $$
declare
  v_email text := lower(btrim(coalesce(p_email, '')));
begin
  if v_email ~ '^[^[:space:]@]+@ijr[.]edu[.]co$' then
    return jsonb_build_object(
      'ok', true,
      'email', v_email,
      'domain', 'ijr.edu.co'
    );
  end if;

  return jsonb_build_object(
    'ok', false,
    'error', 'institutional_email_required'
  );
end;
$$;

revoke all on function public.seminar_email_access_v1(text) from public;
grant execute on function public.seminar_email_access_v1(text) to anon, authenticated, service_role;

comment on function public.seminar_email_access_v1(text) is
'Seminar 11 student-page gate. Accepts only syntactically valid @ijr.edu.co institutional email addresses and returns no private roster data.';
