-- Seminar 11 diagnostics: expose only through the constrained Studio Edge Function.
-- The Edge Function validates the allowed origin and the student's private Studio edit token,
-- then invokes these RPCs with the service role. No direct anon/authenticated RPC access remains.

revoke execute on function public.seminar_track_diagnostic_get_questions(text,text) from public, anon, authenticated;
revoke execute on function public.seminar_track_diagnostic_start(text,text,text,text,text,text) from public, anon, authenticated;
revoke execute on function public.seminar_track_diagnostic_submit(uuid,text,jsonb) from public, anon, authenticated;
revoke execute on function public.seminar_track_diagnostic_snapshot(uuid,text) from public, anon, authenticated;
revoke execute on function public.seminar_track_diagnostic_status(text,text) from public, anon, authenticated;

grant execute on function public.seminar_track_diagnostic_get_questions(text,text) to service_role;
grant execute on function public.seminar_track_diagnostic_start(text,text,text,text,text,text) to service_role;
grant execute on function public.seminar_track_diagnostic_submit(uuid,text,jsonb) to service_role;
grant execute on function public.seminar_track_diagnostic_snapshot(uuid,text) to service_role;
grant execute on function public.seminar_track_diagnostic_status(text,text) to service_role;
