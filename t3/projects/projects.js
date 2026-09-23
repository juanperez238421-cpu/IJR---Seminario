const config=window.IJR_SEMINAR_T3_CONFIG||{};
const API=(config.supabaseUrl||'https://rlfxnjbqxbozjdzkbwlz.supabase.co')+'/functions/v1/seminar-project-access';
const KEY=config.supabasePublishableKey||'sb_publishable_rmVOQ3Orx49KpW_4uMqYew_c2HpcA87';
const STUDIO_TOKEN_KEY='ijr-seminario-studio-edit-token-v1';
const $=id=>document.getElementById(id);
const trackNames={web:'Web Development','data-science':'Python / Data Analyst',cybersecurity:'Defensive Cybersecurity','3d-programming':'3D + Printing',robotics:'Robotics'};
const decisionNames={proposed:'Por confirmar',confirmed:'Confirmado',revise:'Requiere ajuste',rejected:'Descartado'};
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

let state={email:'',student:null,project:null,options:[]};
let selectedKey='';

function setStatus(id,message,type=''){
  const el=$(id);
  if(!el)return;
  el.textContent=message;
  el.className=(id==='accessStatus'?'access-status ':'decision-status ')+type;
}
function friendlyError(code){
  const map={
    write_authorization_required:'No pude validar el permiso para guardar. Usa tu código ST… o abre primero Project Studio en este mismo equipo.',
    project_fields_required:'Completa título, descripción y objetivo antes de confirmar.',
    invalid_choice:'Selecciona una de las opciones de proyecto antes de guardar.',
    project_not_assigned:'No hay un módulo de proyecto asignado a este correo.',
    project_access_denied:'No se encontró este correo en el registro autorizado de Seminario.',
    institutional_email_required:'Debes usar un correo institucional @ijr.edu.co.',
    invalid_client:'La configuración de acceso no es válida. Informa al docente.',
    invalid_request:'No fue posible completar la solicitud. Revisa los campos e intenta nuevamente.'
  };
  return map[code]||'No fue posible completar la solicitud. Intenta nuevamente.';
}
function showAccess(){
  $('projectPanel').classList.add('hidden');
  $('accessPanel').classList.remove('hidden');
  $('institutionalEmail').focus();
}
function formatDate(value){
  if(!value)return'';
  try{
    return new Date(value).toLocaleString('es-CO',{day:'2-digit',month:'short',hour:'2-digit',minute:'2-digit'});
  }catch{return''}
}
function hasDeviceToken(){
  const token=localStorage.getItem(STUDIO_TOKEN_KEY)||'';
  return /^[a-f0-9]{48,128}$/i.test(token);
}
async function api(payload){
  const response=await fetch(API,{
    method:'POST',
    headers:{'Content-Type':'application/json','apikey':KEY},
    body:JSON.stringify(payload)
  });
  const data=await response.json().catch(()=>({}));
  if(!response.ok){
    const error=new Error(data.error||`HTTP ${response.status}`);
    error.code=data.error||'request_failed';
    throw error;
  }
  return data;
}
function updateSelectionUI(){
  document.querySelectorAll('.option-card').forEach(card=>{
    const active=card.dataset.option===selectedKey;
    card.classList.toggle('selected',active);
    card.setAttribute('aria-checked',active?'true':'false');
  });
  const option=state.options.find(x=>x.key===selectedKey);
  $('selectionBadge').textContent=option?option.label:'Sin seleccionar';
  $('selectionBadge').classList.toggle('active',Boolean(option));
  $('choiceKey').value=selectedKey;
}
function fillEditor(values,{clearNote=false}={}){
  $('projectTitleInput').value=values?.title??values?.project_title??'';
  $('projectSummaryInput').value=values?.summary??values?.project_summary??'';
  $('objectiveInput').value=values?.objective??'';
  const stack=values?.stack||[];
  $('stackInput').value=Array.isArray(stack)?stack.join(', '):'';
  if(clearNote)$('studentNote').value='';
}
function chooseOption(key,{silent=false}={}){
  const option=state.options.find(x=>x.key===key);
  if(!option)return;
  selectedKey=key;
  updateSelectionUI();
  fillEditor(option,{clearNote:false});
  if(key==='custom'){
    $('projectTitleInput').focus();
    if(!silent)setStatus('decisionStatus','Escribe tu idea desde cero. Todos los campos se pueden editar.','info');
  }else if(!silent){
    setStatus('decisionStatus','Base cargada. Ahora modifícala para que el proyecto sea tuyo antes de confirmar.','info');
  }
}
function restoreCurrent(){
  const p=state.project;
  if(!p)return;
  selectedKey=p.student_choice_key&&state.options.some(x=>x.key===p.student_choice_key)
    ?p.student_choice_key
    :'teacher-proposal';
  updateSelectionUI();
  fillEditor(p);
  $('studentNote').value=p.student_decision_note||'';
  setStatus('decisionStatus','Se recuperó la última versión guardada.','info');
}
function renderOptions(){
  const kindLabel={teacher:'Propuesta inicial',curated:'Opción sugerida',custom:'Proyecto libre'};
  $('optionGrid').innerHTML=state.options.map(option=>`
    <button type="button" class="option-card" role="radio" aria-checked="false" data-option="${esc(option.key)}">
      <div class="option-top">
        <span class="option-label">${esc(option.label)}</span>
        <span class="option-kind ${esc(option.kind)}">${esc(kindLabel[option.kind]||'Opción')}</span>
      </div>
      <h4>${esc(option.title||'Escribir mi propio proyecto')}</h4>
      <p>${esc(option.summary||'Define libremente qué quieres construir dentro de tu ruta actual.')}</p>
      <div class="option-stack">${(option.stack||[]).slice(0,4).map(x=>`<span>${esc(x)}</span>`).join('')}</div>
      <div class="choose-hint">Seleccionar y editar →</div>
    </button>
  `).join('');
  document.querySelectorAll('.option-card').forEach(card=>{
    card.addEventListener('click',()=>chooseOption(card.dataset.option));
  });
}
function render(data){
  state.student=data.student;
  state.project=data.project;
  state.options=Array.isArray(data.options)?data.options:[];
  const s=state.student,p=state.project;

  $('studentName').textContent=s.name;
  $('groupBadge').textContent=s.group_code;
  $('trackBadge').textContent=trackNames[p.track_slug]||p.track_slug;
  $('modeBadge').textContent=p.project_mode==='fixed'?'Proyecto específico':'Ruta flexible';
  $('modeBadge').dataset.mode=p.project_mode||'guided_definition';
  $('projectTitle').textContent=p.project_title;
  $('projectSummary').textContent=p.project_summary;

  const decisionText=decisionNames[p.decision_status]||p.decision_status||'Por confirmar';
  $('decisionBadgeTop').textContent=decisionText;
  $('decisionBadgeTop').dataset.state=p.decision_status||'proposed';
  $('decisionBadge').textContent=decisionText;
  $('decisionBadge').dataset.state=p.decision_status||'proposed';

  if(p.student_decided_at){
    $('revisionMeta').textContent=`Última confirmación: ${formatDate(p.student_decided_at)} · Revisiones guardadas: ${Number(p.student_revision_count||0)}`;
  }else{
    $('revisionMeta').textContent='Aún no has confirmado una decisión final.';
  }

  $('decisionNote').textContent=p.decision_note||'Usa estas preguntas para cerrar el alcance antes de confirmar.';
  $('defineTitle').textContent=p.project_mode==='fixed'?'Revisa el alcance técnico':'Cierra el alcance de tu idea';
  const questions=Array.isArray(p.definition_questions)?p.definition_questions:[];
  $('definitionQuestions').innerHTML=questions.map(q=>'<li>'+esc(q)+'</li>').join('');
  $('defineToday').classList.toggle('hidden',questions.length===0&&!p.decision_note);

  $('objective').textContent=p.objective;
  $('stack').innerHTML=(p.stack||[]).map(x=>'<span>'+esc(x)+'</span>').join('');
  if(p.safety_scope){
    $('safetyScope').textContent=p.safety_scope;
    $('safetyPanel').classList.remove('hidden');
  }else{
    $('safetyPanel').classList.add('hidden');
  }
  $('sprintGrid').innerHTML=(p.sprints||[]).map(step=>`
    <article class="sprint-card">
      <div class="sprint-number">S${esc(step.n)}</div>
      <div>
        <h4>${esc(step.title)}</h4>
        <p>${esc(step.goal)}</p>
        <div class="deliverable"><strong>Evidencia</strong><span>${esc(step.deliverable)}</span></div>
      </div>
    </article>
  `).join('');

  renderOptions();
  selectedKey=p.student_choice_key&&state.options.some(x=>x.key===p.student_choice_key)
    ?p.student_choice_key
    :'teacher-proposal';
  updateSelectionUI();
  fillEditor(p);
  $('studentNote').value=p.student_decision_note||'';
  $('studentCode').value='';
  $('finalConfirm').checked=false;

  if(hasDeviceToken()){
    $('authHelp').textContent='Este equipo tiene una sesión de Project Studio disponible. Intentaremos validarla automáticamente; el código ST… queda como respaldo.';
    $('studentCode').required=false;
  }else{
    $('authHelp').textContent='Para guardar desde este equipo, escribe tu código personal ST… de estudiante.';
    $('studentCode').required=true;
  }

  $('accessPanel').classList.add('hidden');
  $('projectPanel').classList.remove('hidden');
  window.scrollTo({top:0,behavior:'smooth'});
}

$('accessForm').addEventListener('submit',async e=>{
  e.preventDefault();
  const email=$('institutionalEmail').value.trim().toLowerCase();
  if(!email.endsWith('@ijr.edu.co')){
    setStatus('accessStatus','Usa tu correo institucional @ijr.edu.co.','error');
    return;
  }
  state.email=email;
  setStatus('accessStatus','Buscando tu ruta y tus opciones…','');
  const submit=e.submitter;
  if(submit)submit.disabled=true;
  try{
    const data=await api({action:'load',email});
    setStatus('accessStatus','');
    render(data);
  }catch(error){
    setStatus('accessStatus',friendlyError(error.code||error.message),'error');
  }finally{
    if(submit)submit.disabled=false;
  }
});

$('decisionForm').addEventListener('submit',async e=>{
  e.preventDefault();
  if(!selectedKey){
    setStatus('decisionStatus','Selecciona primero una opción de proyecto.','error');
    return;
  }
  if(!$('finalConfirm').checked){
    setStatus('decisionStatus','Marca la confirmación antes de guardar.','error');
    return;
  }

  const title=$('projectTitleInput').value.trim();
  const summary=$('projectSummaryInput').value.trim();
  const objective=$('objectiveInput').value.trim();
  const stack=$('stackInput').value.split(',').map(x=>x.trim()).filter(Boolean).slice(0,12);
  const editToken=localStorage.getItem(STUDIO_TOKEN_KEY)||'';
  const studentCode=$('studentCode').value.trim();

  if(title.length<3||summary.length<10||objective.length<10){
    setStatus('decisionStatus','Completa título, descripción y objetivo con suficiente detalle.','error');
    return;
  }
  if(!hasDeviceToken()&&!studentCode){
    setStatus('decisionStatus','Escribe tu código ST… para autorizar el guardado.','error');
    $('studentCode').focus();
    return;
  }

  const button=$('saveDecision');
  button.disabled=true;
  setStatus('decisionStatus','Guardando tu decisión final…','');
  try{
    const data=await api({
      action:'save_decision',
      email:state.email,
      choice_key:selectedKey,
      project_title:title,
      project_summary:summary,
      objective,
      stack,
      student_note:$('studentNote').value.trim(),
      edit_token:editToken||null,
      student_code:studentCode||null
    });
    render(data);
    setStatus('decisionStatus','Proyecto confirmado. Tu elección y esta versión quedaron registradas.','ok');
  }catch(error){
    setStatus('decisionStatus',friendlyError(error.code||error.message),'error');
  }finally{
    button.disabled=false;
  }
});

$('restoreCurrent').addEventListener('click',restoreCurrent);
$('changeEmail').addEventListener('click',()=>{
  $('institutionalEmail').value='';
  setStatus('accessStatus','');
  setStatus('decisionStatus','');
  state={email:'',student:null,project:null,options:[]};
  selectedKey='';
  showAccess();
});
