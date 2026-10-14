import {PROJECTS,validateRecord,filterRecords} from './model.js';
const cfg=window.SEMINAR_WEB_CONFIG, $=id=>document.getElementById(id);
const project=new URL(location.href).searchParams.get('project');
let session=null, role=null, records=[], offset=0;
const PAGE=100;
function message(text){$('message').textContent=text}
function clear(){session=null;role=null;records=[];$('loginPanel').hidden=false;$('directoryPanel').hidden=true;$('rows').replaceChildren();$('audit').replaceChildren();$('editor').reset();$('login').reset()}
async function auth(path,body){
  const r=await fetch(cfg.url+'/auth/v1/'+path,{method:'POST',headers:{apikey:cfg.publishableKey,'Content-Type':'application/json'},body:JSON.stringify(body)});
  const data=await r.json().catch(()=>({}));
  if(!r.ok)throw Error('Acceso rechazado. Revisa tu cuenta de prueba.');
  return {...data,expiresAt:Date.now()+data.expires_in*1000};
}
async function api(path,method='GET',body){
  if(!session)throw Error('Inicia sesión.');
  if(Date.now()>session.expiresAt-30000){try{session=await auth('token?grant_type=refresh_token',{refresh_token:session.refresh_token})}catch{clear();throw Error('La sesión venció. Inicia sesión de nuevo.')}}
  const r=await fetch(cfg.url+'/rest/v1/'+path,{method,headers:{apikey:cfg.publishableKey,Authorization:'Bearer '+session.access_token,'Content-Type':'application/json',Prefer:'return=representation'},body:body?JSON.stringify(body):undefined});
  const data=await r.json().catch(()=>([]));
  if(!r.ok){if(r.status===401){clear();throw Error('La sesión venció.')}throw Error(data.code==='23505'?'Ese contacto ya existe en este proyecto.':'No se pudo guardar o consultar. Revisa los permisos y los datos.');}
  return data;
}
const scope=()=>`project_slug=eq.${encodeURIComponent(project)}`;
function render(){
  const filtered=filterRecords(records,$('search').value,$('status').value);$('rows').replaceChildren();
  $('count').textContent=`${filtered.length} visibles de ${records.length} cargados. La búsqueda filtra los registros cargados.`;
  if(!filtered.length){const tr=document.createElement('tr'),td=document.createElement('td');td.colSpan=5;td.textContent='No hay usuarios que coincidan.';tr.append(td);$('rows').append(tr)}
  for(const row of filtered){const tr=document.createElement('tr');for(const field of ['alias','contact','category','status']){const td=document.createElement('td');td.textContent=row[field];tr.append(td)}const actions=document.createElement('td');
    if(role==='admin'){for(const [label,run] of [['Editar',()=>{for(const key of ['id','alias','contact','category'])$('editor').elements[key].value=row[key];$('editorTitle').textContent='Editar usuario';$('editor').elements.alias.focus()}],[row.status==='active'?'Archivar':'Restaurar',()=>changeStatus(row)]]){const b=document.createElement('button');b.textContent=label;b.onclick=()=>guard(run);actions.append(b)}}
    tr.append(actions);$('rows').append(tr);
  }
}
async function load(append=false){
  const start=append?offset:0;
  const page=await api(`seminar_web_directory?${scope()}&select=id,alias,contact,category,status,created_at&order=created_at.desc,id&limit=${PAGE}&offset=${start}`);
  records=append?[...records,...page]:page;offset=start+page.length;$('more').hidden=page.length<PAGE;render();
  if(role==='admin'){const events=await api(`seminar_web_directory_events?${scope()}&select=action,record_id,occurred_at&order=occurred_at.desc&limit=20`);$('audit').replaceChildren();for(const e of events){const li=document.createElement('li');li.textContent=`${new Date(e.occurred_at).toLocaleString()} · ${e.action} · ${e.record_id}`;$('audit').append(li)}}
}
async function changeStatus(row){
  const changed=await api(`seminar_web_directory?${scope()}&id=eq.${row.id}`,'PATCH',{status:row.status==='active'?'archived':'active'});
  if(changed.length!==1)throw Error('El registro no se actualizó. Revisa los permisos.');await load();message('Estado guardado.');
}
async function guard(run){try{message('Procesando…');await run()}catch(e){message(e.message)}}
if(!PROJECTS[project]){message('Abre el enlace de uno de los cuatro proyectos web.');$('loginPanel').hidden=true}else{
  $('projectName').textContent=PROJECTS[project];
  $('login').onsubmit=e=>{e.preventDefault();guard(async()=>{
    const form=new FormData(e.target);session=await auth('token?grant_type=password',{email:form.get('email'),password:form.get('password')});e.target.reset();
    try{const memberships=await api(`seminar_web_memberships?${scope()}&select=role`);role=memberships[0]?.role;if(!role)throw Error('Tu cuenta no tiene acceso a este proyecto. El docente debe asignarte un permiso de prueba.');
      $('loginPanel').hidden=true;$('directoryPanel').hidden=false;$('editor').hidden=role!=='admin';$('auditPanel').hidden=role!=='admin';$('role').textContent=role==='admin'?'Administrador del directorio':'Consulta del directorio';await load();message('Sesión iniciada.');
    }catch(err){clear();throw err}
  })};
  $('editor').onsubmit=e=>{e.preventDefault();guard(async()=>{const data=Object.fromEntries(new FormData(e.target)),id=data.id,valid=validateRecord(data);
    const saved=await api('seminar_web_directory'+(id?`?${scope()}&id=eq.${id}`:''),id?'PATCH':'POST',id?valid:{...valid,project_slug:project});
    if(saved.length!==1)throw Error('No se guardó el registro.');e.target.reset();$('editorTitle').textContent='Nuevo usuario del directorio';await load();message('Usuario guardado.');})};
  $('cancel').onclick=()=>{$('editor').reset();$('editorTitle').textContent='Nuevo usuario del directorio'};
  $('search').oninput=render;$('status').onchange=render;$('more').onclick=()=>guard(()=>load(true));$('reload').onclick=()=>guard(async()=>{await load();message('Datos actualizados.')});
  $('logout').onclick=()=>guard(async()=>{const token=session?.access_token;clear();if(token)await fetch(cfg.url+'/auth/v1/logout?scope=local',{method:'POST',headers:{apikey:cfg.publishableKey,Authorization:'Bearer '+token}});message('Sesión cerrada.');});
}
