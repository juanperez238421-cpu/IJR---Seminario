-- Extend Specific Project live-code workspace to Arduino/C++ source files.

alter table public.seminar_project_code_files
  drop constraint if exists seminar_project_code_files_language_check;

alter table public.seminar_project_code_files
  add constraint seminar_project_code_files_language_check
  check (language in ('python','html','css','javascript','cpp','openscad','json','markdown','text'));
