-- Seminar 11 · OOP Logic Lab 01
-- Question-driven, language-neutral OOP reasoning activity using the shared learning_activity engine.
-- Requires the shared Statistics 11 learning_activity schema/functions deployed by the academic backend baseline.

insert into public.learning_activities(slug,title,status,max_points,grade_min,grade_max,updated_at)
values('seminar11-oop-logic-01-2026','Seminar 11 · OOP Logic Lab 01','open',12,1,5,clock_timestamp())
on conflict (slug) do update set title=excluded.title,status='open',max_points=12,grade_min=1,grade_max=5,updated_at=clock_timestamp();

with a as (select id from public.learning_activities where slug='seminar11-oop-logic-01-2026')
insert into public.learning_activity_checkpoints(activity_id,checkpoint_key,sequence_no,title,prompt,code,hint,answer_type,expected_text,tolerance,points)
select a.id,v.k,v.seq,v.title,v.prompt,null,v.hint,'text',v.expected,0,1
from a cross join (values
('Q01',1,'Class vs Object · Clase vs Objeto','Identifica qué representa una clase en POO.','Piensa en una clase como una definición reutilizable, no como un dato concreto.','Una plantilla que define estado y comportamiento'),
('Q02',2,'Instance · Instancia','Distingue una instancia concreta de su clase.','Una variable creada con el constructor representa un objeto concreto.','Un objeto (instancia) de la clase'),
('Q03',3,'State vs Behavior · Estado vs Comportamiento','Distingue atributos/campos de métodos.','El estado describe datos; el comportamiento describe acciones.','El método representa comportamiento'),
('Q04',4,'Constructor · Constructor','Razona para qué existe un constructor.','El constructor prepara el estado inicial antes de usar el objeto.','Inicializar un objeto con un estado válido'),
('Q05',5,'Encapsulation · Encapsulamiento','Selecciona la razón correcta para proteger el estado interno.','Encapsular no es esconder por esconder: permite controlar reglas e invariantes.','Controlar cómo se modifica el estado y proteger invariantes'),
('Q06',6,'self / this · Objeto actual','Interpreta self/this dentro de un método de instancia.','self/this apunta al objeto concreto que recibió la llamada.','El objeto actual que ejecuta el método'),
('Q07',7,'Object State Trace · Seguimiento de estado','Sigue una mutación cuando dos referencias apuntan al mismo objeto.','Si dos referencias apuntan al mismo objeto, ambas observan el mismo estado.','0'),
('Q08',8,'Inheritance · Herencia','Reconoce una relación is-a correcta.','Herencia expresa especialización: la subclase es un tipo de la superclase.','Herencia: la subclase es-un tipo de la superclase'),
('Q09',9,'Polymorphism · Polimorfismo','Predice qué implementación se ejecuta con overriding.','En despacho dinámico importa la clase real del objeto.','Se ejecuta la versión sobrescrita de la clase real del objeto'),
('Q10',10,'Composition · Composición','Reconoce una relación has-a entre objetos.','Composición modela colaboración: un objeto contiene o utiliza otro.','Composición: el objeto contiene y usa otro objeto'),
('Q11',11,'Abstraction · Abstracción','Identifica el propósito de una interfaz o abstracción.','Una abstracción define un contrato útil sin obligar a exponer todos los detalles internos.','Definir qué debe hacer un tipo sin imponer todos los detalles de implementación'),
('Q12',12,'Integrated OOP Trace · Reto integrado','Combina constructor, estado, métodos y referencias.','Dibuja el objeto una sola vez y actualiza su estado después de cada llamada.','0')
) as v(k,seq,title,prompt,hint,expected)
on conflict (activity_id,checkpoint_key) do update set sequence_no=excluded.sequence_no,title=excluded.title,prompt=excluded.prompt,hint=excluded.hint,answer_type=excluded.answer_type,expected_text=excluded.expected_text,tolerance=0,points=1;

with a as (select id from public.learning_activities where slug='seminar11-oop-logic-01-2026'),
p as (
  select n,
    (array['Robot','BankAccount','Book','Sensor','Order','Player'])[1+((n-1)%6)] as entity,
    (array['Vehicle','Animal','Account','Device','Employee','Shape'])[1+((n-1)%6)] as base_class,
    (array['ElectricCar','Dog','SavingsAccount','Phone','Developer','Circle'])[1+((n-1)%6)] as child_class,
    2+((n*7)%8) as start_value,
    1+((n*5)%5) as delta,
    10+((n*11)%31) as energy
  from generate_series(1,36) n
), rows as (
  select a.id as activity_id,p.n,v.* from a cross join p cross join lateral (values
    ('Q01','choice',format('En el sistema aparece la clase %s. ¿Qué describe mejor una clase en Programación Orientada a Objetos?',p.entity),null::text,'Una plantilla que define estado y comportamiento','Piensa en blueprint/plantilla frente a instancia concreta.',jsonb_build_array('Una plantilla que define estado y comportamiento','Una variable temporal usada por un método','Un único objeto ya creado en memoria','Una lista de instrucciones que siempre se ejecuta en orden'),jsonb_build_object('topic','class_object','concept','class','explanation','Una clase define la estructura y el comportamiento que compartirán sus instancias.')),
    ('Q02','choice',format('Observa: %s unitA = new %s(...). ¿Qué representa unitA conceptualmente?',p.entity,p.entity),format('%s unitA = new %s(...);',p.entity,p.entity),'Un objeto (instancia) de la clase','La expresión new/constructor crea una instancia concreta.',jsonb_build_array('Un objeto (instancia) de la clase','La definición completa de la clase','Un método estático','Un paquete o módulo'),jsonb_build_object('topic','class_object','concept','object','explanation','unitA es una referencia a una instancia concreta creada a partir de la clase.')),
    ('Q03','choice',format('La clase %s tiene energy y recharge(). ¿Cuál miembro representa comportamiento?',p.entity),format('class %s { energy = %s; recharge() { ... } }',p.entity,p.energy),'El método representa comportamiento','Los verbos/acciones suelen modelarse como métodos.',jsonb_build_array('El método representa comportamiento','El atributo representa comportamiento','La clase completa es solo un dato primitivo','Ninguno: en POO no existe comportamiento'),jsonb_build_object('topic','state_behavior','concept','method','explanation','energy representa estado; recharge() representa una acción del objeto.')),
    ('Q04','choice',format('Al crear un %s se requiere un valor inicial de energy. ¿Cuál es la mejor responsabilidad del constructor?',p.entity),format('%s(initialEnergy)',p.entity),'Inicializar un objeto con un estado válido','Pregunta qué debe ser cierto inmediatamente después de crear el objeto.',jsonb_build_array('Inicializar un objeto con un estado válido','Ejecutar todos los métodos de la clase automáticamente','Convertir la clase en una lista','Eliminar la necesidad de atributos'),jsonb_build_object('topic','constructor','concept','valid_state','explanation','El constructor establece el estado inicial necesario para que el objeto nazca válido.')),
    ('Q05','choice',format('En %s el campo balance/energy se protege y solo cambia mediante métodos validados. ¿Por qué es mejor este diseño?',p.entity),null::text,'Controlar cómo se modifica el estado y proteger invariantes','La palabra clave es controlar cambios válidos del estado.',jsonb_build_array('Controlar cómo se modifica el estado y proteger invariantes','Hacer que el programa use más memoria','Evitar completamente el uso de métodos','Permitir que cualquier parte cambie el campo sin reglas'),jsonb_build_object('topic','encapsulation','concept','invariant','explanation','El encapsulamiento concentra las reglas que mantienen válido el estado del objeto.')),
    ('Q06','choice',format('Dentro de un método de instancia de %s aparece self.energy o this.energy. ¿Qué representa self/this?',p.entity),format('self.energy = self.energy + %s',p.delta),'El objeto actual que ejecuta el método','Imagina dos objetos distintos llamando al mismo método.',jsonb_build_array('El objeto actual que ejecuta el método','La clase completa y todas sus instancias a la vez','Una variable global obligatoria','El método constructor exclusivamente'),jsonb_build_object('topic','self_this','concept','current_object','explanation','self/this permite acceder al estado del objeto específico que recibió la llamada.')),
    ('Q07','choice',format('Un objeto Counter inicia en %s. first y second apuntan al MISMO objeto. second.add(%s) modifica value. ¿Qué observa first.value?',p.start_value,p.delta),format(E'first -> Counter(value=%s)\nsecond = first\nsecond.add(%s)',p.start_value,p.delta),(p.start_value+p.delta)::text,'No hay dos objetos: hay dos referencias al mismo objeto.',jsonb_build_array((p.start_value+p.delta)::text,p.start_value::text,(p.start_value+2*p.delta)::text,'Error'),jsonb_build_object('topic','references_state','concept','aliasing','explanation','La mutación ocurre sobre el único objeto compartido; first y second observan el mismo value.')),
    ('Q08','choice',format('%s extiende/hereda de %s. ¿Cuál interpretación es correcta?',p.child_class,p.base_class),format('%s extends %s',p.child_class,p.base_class),'Herencia: la subclase es-un tipo de la superclase','Lee la relación como “child is a base”.',jsonb_build_array('Herencia: la subclase es-un tipo de la superclase','Composición: la superclase está guardada siempre como un campo','No existe relación entre los tipos','La superclase es necesariamente una instancia de la subclase'),jsonb_build_object('topic','inheritance','concept','is_a','explanation','La herencia modela especialización: la subclase puede tratarse como un tipo de la superclase.')),
    ('Q09','choice',format('Una referencia de tipo %s apunta a un objeto real %s que sobrescribe action(). Al llamar action(), ¿qué ocurre?',p.base_class,p.child_class),format(E'%s x = new %s();\nx.action();',p.base_class,p.child_class),'Se ejecuta la versión sobrescrita de la clase real del objeto','Distingue tipo de la referencia frente a clase real del objeto.',jsonb_build_array('Se ejecuta la versión sobrescrita de la clase real del objeto','Siempre se ejecuta la versión de la superclase','Se ejecutan ambas versiones automáticamente','La llamada es inválida por usar una referencia de superclase'),jsonb_build_object('topic','polymorphism','concept','dynamic_dispatch','explanation','El polimorfismo permite que la llamada se resuelva según la implementación del objeto real.')),
    ('Q10','choice','Una clase Car guarda un objeto Engine y delega en él parte de su trabajo. ¿Qué relación describe mejor este diseño?','class Car { Engine engine; }','Composición: el objeto contiene y usa otro objeto','Pregunta si la relación se lee “Car has an Engine”.',jsonb_build_array('Composición: el objeto contiene y usa otro objeto','Herencia: Car es-un Engine','Polimorfismo: Engine siempre reemplaza Car','Encapsulamiento significa que no pueden colaborar'),jsonb_build_object('topic','composition','concept','has_a','explanation','Car has-a Engine: los objetos colaboran sin afirmar que uno sea un subtipo del otro.')),
    ('Q11','choice','Varias clases deben cumplir el contrato process() pero cada una puede implementarlo diferente. ¿Qué idea POO se busca principalmente?','interface Processor { process(); }','Definir qué debe hacer un tipo sin imponer todos los detalles de implementación','Un contrato separa el qué del cómo.',jsonb_build_array('Definir qué debe hacer un tipo sin imponer todos los detalles de implementación','Guardar todos los campos como variables globales','Duplicar el mismo código en cada clase','Evitar por completo el polimorfismo'),jsonb_build_object('topic','abstraction','concept','contract','explanation','La abstracción/interfaz define capacidades esperadas y deja los detalles a implementaciones concretas.')),
    ('Q12','choice',format('Counter nace con value=%s. a y b apuntan al mismo objeto. a.add(%s) y luego b.add(%s). ¿Cuál es el value final?',p.start_value,p.delta,p.delta),format(E'a = Counter(%s)\nb = a\na.add(%s)\nb.add(%s)',p.start_value,p.delta,p.delta),(p.start_value+2*p.delta)::text,'Dibuja un solo objeto y actualiza value dos veces.',jsonb_build_array((p.start_value+2*p.delta)::text,(p.start_value+p.delta)::text,p.start_value::text,(p.start_value+3*p.delta)::text),jsonb_build_object('topic','integrated_trace','concept','constructor_state_reference','explanation','El constructor fija el estado inicial y las dos referencias modifican el mismo objeto dos veces.'))
  ) as v(checkpoint_key,mode,prompt,starter_code,expected_text,hint,choices,metadata)
)
insert into public.learning_activity_variant_bank(activity_id,checkpoint_key,pack_no,variant_key,mode,prompt,starter_code,solution_code,hint,answer_type,expected_text,tolerance,choices,metadata,updated_at)
select activity_id,checkpoint_key,n,format('%s-P%02s',checkpoint_key,n),mode,prompt,starter_code,metadata->>'explanation',hint,'text',expected_text,0,choices,metadata,clock_timestamp()
from rows
on conflict (activity_id,checkpoint_key,pack_no) do update set variant_key=excluded.variant_key,mode=excluded.mode,prompt=excluded.prompt,starter_code=excluded.starter_code,solution_code=excluded.solution_code,hint=excluded.hint,answer_type=excluded.answer_type,expected_text=excluded.expected_text,tolerance=excluded.tolerance,choices=excluded.choices,metadata=excluded.metadata,updated_at=clock_timestamp();

create or replace function public.seminar_oop_assign_variant_pack_v1(p_attempt_id uuid)
returns smallint language plpgsql security definer set search_path='public','extensions' as $$
declare v_attempt public.learning_activity_attempts%rowtype; v_slug text; v_pack smallint;
begin
  select x.* into v_attempt from public.learning_activity_attempts x where x.id=p_attempt_id for update;
  if v_attempt.id is null then raise exception 'Activity attempt not found'; end if;
  select a.slug into v_slug from public.learning_activities a where a.id=v_attempt.activity_id;
  if v_slug<>'seminar11-oop-logic-01-2026' then raise exception 'Wrong activity'; end if;
  select pack_no into v_pack from public.learning_activity_attempt_variant_pack where attempt_id=p_attempt_id;
  if v_pack is not null then return v_pack; end if;
  perform pg_advisory_xact_lock(hashtext('seminar11-oop-logic-01-pack-allocation'));
  select p.n::smallint into v_pack
  from generate_series(1,36) p(n)
  left join (
    select ap.pack_no,count(*)::integer uses
    from public.learning_activity_attempt_variant_pack ap
    join public.learning_activity_attempts x on x.id=ap.attempt_id
    where ap.activity_id=v_attempt.activity_id and x.started_at>=clock_timestamp()-interval '4 hours'
    group by ap.pack_no
  ) u on u.pack_no=p.n
  order by coalesce(u.uses,0),random() limit 1;
  insert into public.learning_activity_attempt_variant_pack(attempt_id,activity_id,pack_no,assignment_reason)
  values(v_attempt.id,v_attempt.activity_id,v_pack,'least_used_random_4h');
  insert into public.learning_activity_events(attempt_id,event_type,metadata)
  values(v_attempt.id,'OOP_VARIANT_PACK_ASSIGNED',jsonb_build_object('pack_no',v_pack,'bank_size',36));
  return v_pack;
end;$$;

create or replace function public.seminar_oop_snapshot_v1(p_attempt_id uuid,p_attempt_token text)
returns jsonb language plpgsql security definer set search_path='public','extensions' as $$
declare v_base jsonb; v_activity_id uuid; v_slug text; v_pack smallint; v_checkpoints jsonb;
begin
  v_base:=public.learning_activity_snapshot(p_attempt_id,p_attempt_token);
  select x.activity_id,a.slug into v_activity_id,v_slug from public.learning_activity_attempts x join public.learning_activities a on a.id=x.activity_id where x.id=p_attempt_id;
  if v_slug<>'seminar11-oop-logic-01-2026' then raise exception 'Wrong activity'; end if;
  select pack_no into v_pack from public.learning_activity_attempt_variant_pack where attempt_id=p_attempt_id;
  if v_pack is null then v_pack:=public.seminar_oop_assign_variant_pack_v1(p_attempt_id); end if;
  select coalesce(jsonb_agg(cp.value || jsonb_build_object(
    'prompt',v.prompt,'code',v.starter_code,'hint',v.hint,'mode',v.mode,'choices',v.choices,
    'variant_key',v.variant_key,'variant_pack',v.pack_no,'topic',v.metadata->>'topic','concept_key',v.metadata->>'concept'
  ) order by cp.ord),'[]'::jsonb) into v_checkpoints
  from jsonb_array_elements(v_base->'checkpoints') with ordinality cp(value,ord)
  join public.learning_activity_variant_bank v on v.activity_id=v_activity_id and v.pack_no=v_pack and v.checkpoint_key=cp.value->>'key';
  return jsonb_set(jsonb_set(v_base,'{checkpoints}',v_checkpoints,true),'{variant_pack}',to_jsonb(v_pack),true)
    || jsonb_build_object('variant_bank_size',36,'variant_strategy','least_used_random_4h','activity_kind','oop_logic_questions');
end;$$;

create or replace function public.seminar_oop_start_team_v1(p_student_names jsonb,p_group_code text,p_session_id uuid,p_user_agent text)
returns jsonb language plpgsql security definer set search_path='public','extensions' as $$
declare v_activity public.learning_activities%rowtype; v_attempt public.learning_activity_attempts%rowtype; v_student public.student_registry%rowtype; v_group text; v_token text; v_team_key text; v_team_label text; v_size int; v_i int; v_display text; v_norm text; v_match_count int; v_names text[]:=array[]::text[]; v_norms text[]:=array[]::text[]; v_all_roster boolean:=true;
begin
  v_group:=upper(replace(trim(coalesce(p_group_code,'')),'-',''));
  if v_group not in ('11A','11B','11C') then raise exception 'Select a valid group'; end if;
  if p_student_names is null or jsonb_typeof(p_student_names)<>'array' then raise exception 'Provide team members'; end if;
  v_size:=jsonb_array_length(p_student_names); if v_size<1 or v_size>3 then raise exception 'Register 1 to 3 students'; end if;
  select * into v_activity from public.learning_activities where slug='seminar11-oop-logic-01-2026' and status='open';
  if v_activity.id is null then raise exception 'Activity is not open'; end if;
  for v_i in 0..v_size-1 loop
    v_display:=regexp_replace(trim(coalesce(p_student_names->>v_i,'')),'[[:space:]]+',' ','g');
    if length(v_display)<2 then raise exception 'Write every team member name'; end if;
    v_norm:=public.normalize_student_name(v_display); if coalesce(length(v_norm),0)=0 then v_norm:=lower(v_display); end if;
    if v_norm=any(v_norms) then raise exception 'Do not repeat the same name inside one team'; end if;
    v_names:=array_append(v_names,v_display); v_norms:=array_append(v_norms,v_norm);
  end loop;
  select string_agg(n,'|' order by n) into v_team_key from unnest(v_norms) n;
  select string_agg(n,' · ' order by ord) into v_team_label from unnest(v_names) with ordinality t(n,ord);
  v_token:=replace(gen_random_uuid()::text,'-','')||replace(gen_random_uuid()::text,'-','');
  select * into v_attempt from public.learning_activity_attempts where activity_id=v_activity.id and session_id=p_session_id order by started_at desc limit 1;
  if v_attempt.id is null then
    insert into public.learning_activity_attempts(activity_id,student_registry_id,student_name_snapshot,student_name_normalized,is_roster_match,group_code,session_id,access_token_hash,user_agent,team_key,team_size,registration_mode)
    values(v_activity.id,null,v_team_label,v_team_key,false,v_group,coalesce(p_session_id,gen_random_uuid()),encode(digest(v_token,'sha256'),'hex'),p_user_agent,v_team_key,v_size,'team') returning * into v_attempt;
  else
    update public.learning_activity_attempts set student_name_snapshot=v_team_label,student_name_normalized=v_team_key,access_token_hash=encode(digest(v_token,'sha256'),'hex'),last_activity_at=clock_timestamp(),user_agent=coalesce(p_user_agent,user_agent),team_key=v_team_key,team_size=v_size,registration_mode='team' where id=v_attempt.id returning * into v_attempt;
    delete from public.learning_activity_attempt_members where attempt_id=v_attempt.id;
  end if;
  for v_i in 1..v_size loop
    v_display:=v_names[v_i]; v_norm:=v_norms[v_i];
    select count(*) into v_match_count from public.student_registry s where s.active=true and s.group_code=v_group and (s.normalized_name=v_norm or (s.name_is_truncated and v_norm like s.normalized_name||'%'));
    if v_match_count=1 then select * into v_student from public.student_registry s where s.active=true and s.group_code=v_group and (s.normalized_name=v_norm or (s.name_is_truncated and v_norm like s.normalized_name||'%')) limit 1; else v_student.id:=null; v_all_roster:=false; end if;
    insert into public.learning_activity_attempt_members(attempt_id,activity_id,group_code,member_order,student_registry_id,display_name,normalized_name,is_roster_match)
    values(v_attempt.id,v_activity.id,v_group,v_i,case when v_match_count=1 then v_student.id else null end,v_display,v_norm,(v_match_count=1));
  end loop;
  update public.learning_activity_attempts set is_roster_match=v_all_roster where id=v_attempt.id;
  perform public.seminar_oop_assign_variant_pack_v1(v_attempt.id);
  insert into public.learning_activity_events(attempt_id,event_type,metadata) values(v_attempt.id,'OOP_TEAM_SESSION_STARTED',jsonb_build_object('team_size',v_size,'group_code',v_group));
  return jsonb_build_object('attempt_id',v_attempt.id,'attempt_token',v_token,'snapshot',public.seminar_oop_snapshot_v1(v_attempt.id,v_token));
end;$$;

create or replace function public.seminar_oop_resume_v1(p_attempt_id uuid,p_attempt_token text)
returns jsonb language sql security definer set search_path='public','extensions' as $$ select jsonb_build_object('snapshot',public.seminar_oop_snapshot_v1(p_attempt_id,p_attempt_token)); $$;

create or replace function public.seminar_oop_submit_v1(p_attempt_id uuid,p_attempt_token text,p_checkpoint_key text,p_answer text)
returns jsonb language plpgsql security definer set search_path='public','extensions' as $$
declare a public.learning_activity_attempts%rowtype; cp public.learning_activity_checkpoints%rowtype; r public.learning_activity_responses%rowtype; v_pack smallint; v_expected text; v_variant text; v_correct boolean; v_awarded numeric:=0; v_wrong int:=0; v_help int:=0;
begin
  select * into a from public.learning_activity_attempts where id=p_attempt_id and access_token_hash=encode(digest(p_attempt_token,'sha256'),'hex') for update;
  if a.id is null then raise exception 'Invalid activity session'; end if; if a.status='submitted' then return jsonb_build_object('correct',false,'snapshot',public.seminar_oop_snapshot_v1(p_attempt_id,p_attempt_token)); end if;
  select c.* into cp from public.learning_activity_checkpoints c left join public.learning_activity_responses x on x.checkpoint_id=c.id and x.attempt_id=a.id where c.activity_id=a.activity_id and coalesce(x.completed,false)=false order by c.sequence_no limit 1;
  if cp.id is null or cp.checkpoint_key<>p_checkpoint_key then raise exception 'Complete the current stage first'; end if;
  v_pack:=public.seminar_oop_assign_variant_pack_v1(a.id);
  select expected_text,variant_key into v_expected,v_variant from public.learning_activity_variant_bank where activity_id=a.activity_id and pack_no=v_pack and checkpoint_key=cp.checkpoint_key;
  v_correct:=lower(trim(coalesce(p_answer,'')))=lower(trim(v_expected));
  select * into r from public.learning_activity_responses where attempt_id=a.id and checkpoint_id=cp.id for update;
  if r.id is null then
    if v_correct then v_awarded:=public.learning_activity_stage_credit(cp.points,0,0); insert into public.learning_activity_responses(attempt_id,checkpoint_id,latest_answer,correct,try_count,first_try_correct,first_answered_at,last_answered_at,completed,completion_mode,awarded_points,wrong_attempts) values(a.id,cp.id,p_answer,true,1,true,clock_timestamp(),clock_timestamp(),true,'solved',v_awarded,0);
    else v_wrong:=1; insert into public.learning_activity_responses(attempt_id,checkpoint_id,latest_answer,correct,try_count,first_try_correct,first_answered_at,last_answered_at,completed,completion_mode,awarded_points,wrong_attempts) values(a.id,cp.id,p_answer,false,1,false,clock_timestamp(),clock_timestamp(),false,'pending',0,1); end if;
  else
    v_help:=coalesce(r.help_count,0); v_wrong:=coalesce(r.wrong_attempts,0);
    if v_correct then v_awarded:=public.learning_activity_stage_credit(cp.points,v_help,v_wrong); update public.learning_activity_responses set latest_answer=p_answer,correct=true,try_count=try_count+1,last_answered_at=clock_timestamp(),completed=true,completion_mode='solved',awarded_points=v_awarded where id=r.id;
    else v_wrong:=v_wrong+1; update public.learning_activity_responses set latest_answer=p_answer,correct=false,try_count=try_count+1,last_answered_at=clock_timestamp(),wrong_attempts=v_wrong where id=r.id; end if;
  end if;
  update public.learning_activity_attempts set last_activity_at=clock_timestamp() where id=a.id;
  insert into public.learning_activity_events(attempt_id,event_type,metadata) values(a.id,'OOP_ANSWER_VALIDATED',jsonb_build_object('checkpoint_key',cp.checkpoint_key,'variant_key',v_variant,'pack_no',v_pack,'correct',v_correct));
  perform public.learning_activity_refresh_attempt_score(a.id);
  return jsonb_build_object('correct',v_correct,'awarded_points',case when v_correct then v_awarded else 0 end,'wrong_attempts',v_wrong,'snapshot',public.seminar_oop_snapshot_v1(a.id,p_attempt_token));
end;$$;

create or replace function public.seminar_oop_use_help_v1(p_attempt_id uuid,p_attempt_token text,p_checkpoint_key text)
returns jsonb language plpgsql security definer set search_path='public','extensions' as $$
declare d jsonb; v_pack smallint; v_hint text;
begin
  d:=public.student_learning_activity_use_help(p_attempt_id,p_attempt_token,p_checkpoint_key);
  v_pack:=public.seminar_oop_assign_variant_pack_v1(p_attempt_id);
  select hint into v_hint from public.learning_activity_variant_bank v join public.learning_activity_attempts a on a.activity_id=v.activity_id where a.id=p_attempt_id and v.pack_no=v_pack and v.checkpoint_key=p_checkpoint_key;
  return jsonb_set(d,'{snapshot}',public.seminar_oop_snapshot_v1(p_attempt_id,p_attempt_token),true)||jsonb_build_object('variant_hint',v_hint);
end;$$;

create or replace function public.seminar_oop_reveal_v1(p_attempt_id uuid,p_attempt_token text,p_checkpoint_key text)
returns jsonb language plpgsql security definer set search_path='public','extensions' as $$
declare a public.learning_activity_attempts%rowtype; cp public.learning_activity_checkpoints%rowtype; v_pack smallint; v_expected text; v_explanation text; v_variant text; v_awarded numeric;
begin
  select * into a from public.learning_activity_attempts where id=p_attempt_id and access_token_hash=encode(digest(p_attempt_token,'sha256'),'hex') for update;
  if a.id is null then raise exception 'Invalid activity session'; end if; if a.status='submitted' then raise exception 'Activity already completed'; end if;
  select c.* into cp from public.learning_activity_checkpoints c left join public.learning_activity_responses r on r.checkpoint_id=c.id and r.attempt_id=a.id where c.activity_id=a.activity_id and coalesce(r.completed,false)=false order by c.sequence_no limit 1;
  if cp.id is null or cp.checkpoint_key<>p_checkpoint_key then raise exception 'Reveal is only available for the current stage'; end if;
  v_pack:=public.seminar_oop_assign_variant_pack_v1(a.id);
  select expected_text,solution_code,variant_key into v_expected,v_explanation,v_variant from public.learning_activity_variant_bank where activity_id=a.activity_id and pack_no=v_pack and checkpoint_key=cp.checkpoint_key;
  v_awarded:=round(cp.points*0.25,4);
  insert into public.learning_activity_responses(attempt_id,checkpoint_id,latest_answer,correct,try_count,completed,completion_mode,awarded_points,solution_revealed) values(a.id,cp.id,v_expected,false,0,true,'revealed',v_awarded,true)
  on conflict(attempt_id,checkpoint_id) do update set latest_answer=v_expected,correct=false,completed=true,completion_mode='revealed',awarded_points=v_awarded,solution_revealed=true,last_answered_at=clock_timestamp();
  insert into public.learning_activity_events(attempt_id,event_type,metadata) values(a.id,'OOP_SOLUTION_REVEALED',jsonb_build_object('checkpoint_key',p_checkpoint_key,'variant_key',v_variant,'pack_no',v_pack));
  perform public.learning_activity_refresh_attempt_score(a.id);
  return jsonb_build_object('expected_answer',v_expected,'explanation',v_explanation,'awarded_points',v_awarded,'snapshot',public.seminar_oop_snapshot_v1(a.id,p_attempt_token));
end;$$;

create or replace function public.seminar_oop_skip_v1(p_attempt_id uuid,p_attempt_token text,p_checkpoint_key text)
returns jsonb language plpgsql security definer set search_path='public','extensions' as $$ declare d jsonb; begin d:=public.student_learning_activity_skip_stage(p_attempt_id,p_attempt_token,p_checkpoint_key); return jsonb_set(d,'{snapshot}',public.seminar_oop_snapshot_v1(p_attempt_id,p_attempt_token),true); end; $$;

create or replace function public.teacher_seminar_oop_dashboard_v1(p_teacher_token text)
returns jsonb language plpgsql security definer set search_path='public','extensions' as $$
declare v_teacher uuid; v_activity public.learning_activities%rowtype;
begin
  v_teacher:=public.teacher_code_session_id(p_teacher_token);
  if v_teacher is null then raise exception 'Invalid or expired teacher session'; end if;
  select * into v_activity from public.learning_activities where slug='seminar11-oop-logic-01-2026';
  return jsonb_build_object('generated_at',clock_timestamp(),'activity_slug',v_activity.slug,'activity_title',v_activity.title,'sessions',(
    select coalesce(jsonb_agg(jsonb_build_object(
      'attempt_id',x.id,'group_code',x.group_code,'status',x.status,'team_size',x.team_size,
      'participants',coalesce(ms.participants,'[]'::jsonb),'variant_pack',ap.pack_no,'grade',x.grade,
      'projected_grade',proj.projected_grade,'completed_count',coalesce(rs.completed_count,0),'checkpoint_count',12,
      'wrong_attempts',coalesce(rs.wrong_attempts,0),'helps',coalesce(rs.helps,0),
      'revealed_count',coalesce(rs.revealed_count,0),'skipped_count',coalesce(rs.skipped_count,0),
      'latest_checkpoint_key',lr.checkpoint_key,'latest_answer',lr.latest_answer,'latest_answer_correct',lr.correct,
      'started_at',x.started_at,'last_activity_at',x.last_activity_at
    ) order by x.last_activity_at desc),'[]'::jsonb)
    from public.learning_activity_attempts x
    left join public.learning_activity_attempt_variant_pack ap on ap.attempt_id=x.id
    left join lateral (select jsonb_agg(jsonb_build_object('display_name',m.display_name,'member_order',m.member_order) order by m.member_order) participants from public.learning_activity_attempt_members m where m.attempt_id=x.id) ms on true
    left join lateral (select count(*) filter(where r.completed)::int completed_count,coalesce(sum(r.wrong_attempts),0)::int wrong_attempts,coalesce(sum(r.help_count),0)::int helps,count(*) filter(where r.completion_mode='revealed')::int revealed_count,count(*) filter(where r.completion_mode='skipped')::int skipped_count from public.learning_activity_responses r where r.attempt_id=x.id) rs on true
    left join lateral (select c.checkpoint_key,r.latest_answer,r.correct from public.learning_activity_responses r join public.learning_activity_checkpoints c on c.id=r.checkpoint_id where r.attempt_id=x.id order by r.last_answered_at desc nulls last,c.sequence_no desc limit 1) lr on true
    left join lateral (select round(v_activity.grade_min+(v_activity.grade_max-v_activity.grade_min)*(coalesce(sum(case when coalesce(r.completed,false) then coalesce(r.awarded_points,0) else public.learning_activity_stage_credit(c.points,coalesce(r.help_count,0),coalesce(r.wrong_attempts,0)) end),0)/greatest(v_activity.max_points,1)),2) projected_grade from public.learning_activity_checkpoints c left join public.learning_activity_responses r on r.checkpoint_id=c.id and r.attempt_id=x.id where c.activity_id=x.activity_id) proj on true
    where x.activity_id=v_activity.id
  ));
end;$$;

create or replace function public.teacher_seminar_oop_detail_v1(p_teacher_token text,p_attempt_id uuid)
returns jsonb language plpgsql security definer set search_path='public','extensions' as $$
declare v_teacher uuid; a public.learning_activity_attempts%rowtype; v_pack smallint;
begin
  v_teacher:=public.teacher_code_session_id(p_teacher_token); if v_teacher is null then raise exception 'Invalid or expired teacher session'; end if;
  select x.* into a from public.learning_activity_attempts x join public.learning_activities la on la.id=x.activity_id where x.id=p_attempt_id and la.slug='seminar11-oop-logic-01-2026'; if a.id is null then raise exception 'Registration not found'; end if;
  select pack_no into v_pack from public.learning_activity_attempt_variant_pack where attempt_id=a.id;
  return jsonb_build_object(
    'attempt',jsonb_build_object('attempt_id',a.id,'group_code',a.group_code,'status',a.status,'team_size',a.team_size,'grade',a.grade,'variant_pack',v_pack,'started_at',a.started_at,'last_activity_at',a.last_activity_at,'session_id',a.session_id),
    'participants',(select coalesce(jsonb_agg(jsonb_build_object('member_order',m.member_order,'display_name',m.display_name,'is_roster_match',m.is_roster_match) order by m.member_order),'[]'::jsonb) from public.learning_activity_attempt_members m where m.attempt_id=a.id),
    'responses',(select coalesce(jsonb_agg(jsonb_build_object('sequence',c.sequence_no,'checkpoint_key',c.checkpoint_key,'title',c.title,'prompt',v.prompt,'choices',v.choices,'expected_answer',v.expected_text,'latest_answer',r.latest_answer,'correct',coalesce(r.correct,false),'completed',coalesce(r.completed,false),'completion_mode',coalesce(r.completion_mode,'pending'),'try_count',coalesce(r.try_count,0),'wrong_attempts',coalesce(r.wrong_attempts,0),'help_count',coalesce(r.help_count,0),'awarded_points',coalesce(r.awarded_points,0),'explanation',v.solution_code) order by c.sequence_no),'[]'::jsonb)
      from public.learning_activity_checkpoints c left join public.learning_activity_variant_bank v on v.activity_id=c.activity_id and v.checkpoint_key=c.checkpoint_key and v.pack_no=v_pack left join public.learning_activity_responses r on r.checkpoint_id=c.id and r.attempt_id=a.id where c.activity_id=a.activity_id),
    'events',(select coalesce(jsonb_agg(jsonb_build_object('event_type',e.event_type,'metadata',e.metadata,'created_at',e.created_at) order by e.created_at desc),'[]'::jsonb) from (select * from public.learning_activity_events where attempt_id=a.id order by created_at desc limit 100) e)
  );
end;$$;

revoke all on function public.seminar_oop_assign_variant_pack_v1(uuid) from public,anon,authenticated;
revoke all on function public.seminar_oop_snapshot_v1(uuid,text) from public,anon,authenticated;
revoke all on function public.seminar_oop_start_team_v1(jsonb,text,uuid,text) from public;
revoke all on function public.seminar_oop_resume_v1(uuid,text) from public;
revoke all on function public.seminar_oop_submit_v1(uuid,text,text,text) from public;
revoke all on function public.seminar_oop_use_help_v1(uuid,text,text) from public;
revoke all on function public.seminar_oop_reveal_v1(uuid,text,text) from public;
revoke all on function public.seminar_oop_skip_v1(uuid,text,text) from public;
revoke all on function public.teacher_seminar_oop_dashboard_v1(text) from public;
revoke all on function public.teacher_seminar_oop_detail_v1(text,uuid) from public;

grant execute on function public.seminar_oop_start_team_v1(jsonb,text,uuid,text) to anon,authenticated;
grant execute on function public.seminar_oop_resume_v1(uuid,text) to anon,authenticated;
grant execute on function public.seminar_oop_submit_v1(uuid,text,text,text) to anon,authenticated;
grant execute on function public.seminar_oop_use_help_v1(uuid,text,text) to anon,authenticated;
grant execute on function public.seminar_oop_reveal_v1(uuid,text,text) to anon,authenticated;
grant execute on function public.seminar_oop_skip_v1(uuid,text,text) to anon,authenticated;
grant execute on function public.teacher_seminar_oop_dashboard_v1(text) to anon,authenticated;
grant execute on function public.teacher_seminar_oop_detail_v1(text,uuid) to anon,authenticated;

notify pgrst,'reload schema';
