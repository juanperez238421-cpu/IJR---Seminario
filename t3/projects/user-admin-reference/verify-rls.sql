-- Uses an existing Auth identity only inside a rolled-back transaction.
-- Does not create accounts, persist permissions, or change institutional data.
begin;
select set_config('request.jwt.claims',json_build_object('sub',(select u.id from auth.users u where not exists (select 1 from public.seminar_web_memberships m where m.user_id=u.id) order by u.created_at limit 1),'role','authenticated')::text,true);
insert into public.seminar_web_memberships(project_slug,user_id,role)
values ('cortes-web-definition',auth.uid(),'admin'),('gomez-gta-v-mod-showcase',auth.uid(),'viewer');
set local role authenticated;
do $$
declare affected integer;
begin
  insert into public.seminar_web_directory(project_slug,alias,contact) values('cortes-web-definition','QA example','qa@example.test');
  update public.seminar_web_directory set alias='QA edited',status='archived' where contact='qa@example.test';
  get diagnostics affected = row_count;
  if affected<>1 then raise exception 'admin_update_failed'; end if;
  update public.seminar_web_directory set status='active' where contact='qa@example.test';
  if (select count(*) from public.seminar_web_directory_events where project_slug='cortes-web-definition')<>3 then raise exception 'audit_missing'; end if;
  begin
    insert into public.seminar_web_directory(project_slug,alias,contact) values('cortes-web-definition','Duplicate','qa@example.test');
    raise exception 'duplicate_contact_allowed';
  exception when unique_violation then null; end;
  begin
    insert into public.seminar_web_directory(project_slug,alias,contact) values('cortes-web-definition','Real contact','qa@real.com');
    raise exception 'real_contact_allowed';
  exception when check_violation then null; end;
  begin
    insert into public.seminar_web_directory(project_slug,alias,contact) values('gomez-gta-v-mod-showcase','Viewer write','viewer@example.test');
    raise exception 'viewer_write_allowed';
  exception when insufficient_privilege then null; end;
  begin
    insert into public.seminar_web_directory(project_slug,alias,contact) values('jaramillo-web-definition','Cross project','cross@example.test');
    raise exception 'cross_project_write_allowed';
  exception when insufficient_privilege then null; end;
  begin
    update public.seminar_web_memberships set role='admin' where project_slug='gomez-gta-v-mod-showcase';
    raise exception 'self_promotion_allowed';
  exception when insufficient_privilege then null; end;
  begin
    update public.seminar_web_directory set project_slug='gomez-gta-v-mod-showcase' where contact='qa@example.test';
    raise exception 'project_reassignment_allowed';
  exception when insufficient_privilege then null; end;
  begin
    delete from public.seminar_web_directory where contact='qa@example.test';
    raise exception 'physical_delete_allowed';
  exception when insufficient_privilege then null; end;
  begin
    delete from public.seminar_web_directory_events;
    raise exception 'audit_deletion_allowed';
  exception when insufficient_privilege then null; end;
end $$;
reset role;
update public.seminar_web_memberships set role='viewer' where project_slug='cortes-web-definition';
set local role authenticated;
do $$ declare affected integer; begin
  if (select count(*) from public.seminar_web_directory)<>1 then raise exception 'viewer_read_failed'; end if;
  update public.seminar_web_directory set alias='unauthorized' where contact='qa@example.test';
  get diagnostics affected = row_count;
  if affected<>0 then raise exception 'viewer_update_allowed'; end if;
  if (select count(*) from public.seminar_web_directory_events)<>0 then raise exception 'viewer_audit_allowed'; end if;
end $$;
reset role;
select set_config('request.jwt.claims',json_build_object('sub',gen_random_uuid(),'role','authenticated')::text,true);
set local role authenticated;
do $$ begin
  if (select count(*) from public.seminar_web_directory)<>0 then raise exception 'unassigned_user_read_allowed'; end if;
  if (select count(*) from public.seminar_web_memberships)<>0 then raise exception 'membership_leak'; end if;
end $$;
reset role;
set local role anon;
do $$ begin
  begin perform 1 from public.seminar_web_directory; raise exception 'anonymous_read_allowed';
  exception when insufficient_privilege then null; end;
end $$;
reset role;
rollback;
select 'PASS: admin create/read/update/archive/restore, audit, viewer read-only, isolation, anonymous denial, uniqueness, synthetic contacts, no self-promotion, no project reassignment, no deletion; fixtures rolled back' as result;
