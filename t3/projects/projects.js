const config=window.IJR_SEMINAR_T3_CONFIG||{};
const API=(config.supabaseUrl||'https://rlfxnjbqxbozjdzkbwlz.supabase.co')+'/functions/v1/seminar-project-access';
const KEY=config.supabasePublishableKey||'sb_publishable_rmVOQ3Orx49KpW_4uMqYew_c2HpcA87';
const $=id=>document.getElementById(id);
const trackNames={web:'Web Development','data-science':'Python / Data Analyst',cybersecurity:'Defensive Cybersecurity','3d-programming':'3D + Printing',robotics:'Robotics'};
const decisionNames={proposed:'Por definir / propuesto',confirmed:'Confirmado',revise:'Requiere ajuste',rejected:'Descartado'};
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

function setStatus(message,type=''){
  const el=$('accessStatus');
  el.textContent=message;
  el.className='access-status '+type;
}
function showAccess(){
  $('projectPanel').classList.add('hidden');
  $('accessPanel').classList.remove('hidden');
  $('institutionalEmail').focus();
}
function render(data){
  const s=data.student,p=data.project;
  $('studentName').textContent=s.name;
  $('groupBadge').textContent=s.group_code;
  $('trackBadge').textContent=trackNames[p.track_slug]||p.track_slug;
  $('modeBadge').textContent=p.project_mode==='fixed'?'Proyecto específico':'Definir hoy';
  $('modeBadge').dataset.mode=p.project_mode||'guided_definition';
  $('projectTitle').textContent=p.project_title;
  $('projectSummary').textContent=p.project_summary;
  $('objective').textContent=p.objective;
  $('decisionBadge').textContent=decisionNames[p.decision_status]||p.decision_status||'Propuesta';
  $('decisionBadge').dataset.state=p.decision_status||'proposed';
  $('decisionNote').textContent=p.decision_note||'Revisa las preguntas y define el alcance con el docente.';
  $('defineTitle').textContent=p.project_mode==='fixed'?'Concreta el alcance técnico':'Define hoy tu proyecto específico';
  $('definitionQuestions').innerHTML=(p.definition_questions||[]).map(q=>'<li>'+esc(q)+'</li>').join('');
  $('stack').innerHTML=(p.stack||[]).map(x=>'<span>'+esc(x)+'</span>').join('');
  if(p.safety_scope){
    $('safetyScope').textContent=p.safety_scope;
    $('safetyPanel').classList.remove('hidden');
  }else{
    $('safetyPanel').classList.add('hidden');
  }
  $('sprintGrid').innerHTML=(p.sprints||[]).map(step=>'<article class="sprint-card"><div class="sprint-number">S'+esc(step.n)+'</div><div><h4>'+esc(step.title)+'</h4><p>'+esc(step.goal)+'</p><div class="deliverable"><strong>Evidencia</strong><span>'+esc(step.deliverable)+'</span></div></div></article>').join('');
  $('accessPanel').classList.add('hidden');
  $('projectPanel').classList.remove('hidden');
  window.scrollTo({top:0,behavior:'smooth'});
}

$('accessForm').addEventListener('submit',async e=>{
  e.preventDefault();
  const email=$('institutionalEmail').value.trim().toLowerCase();
  if(!email.endsWith('@ijr.edu.co')){
    setStatus('Usa tu correo institucional @ijr.edu.co.','error');
    return;
  }
  setStatus('Buscando tu módulo…');
  const submit=e.submitter;
  if(submit) submit.disabled=true;
  try{
    const response=await fetch(API,{
      method:'POST',
      headers:{'Content-Type':'application/json','apikey':KEY},
      body:JSON.stringify({email})
    });
    const data=await response.json().catch(()=>({}));
    if(!response.ok){
      if(data.error==='project_not_assigned'||data.error==='project_access_denied'){
        throw new Error('No hay un módulo de proyecto asignado a este correo. Verifica el correo o consulta al docente.');
      }
      if(data.error==='institutional_email_required'){
        throw new Error('Debes ingresar un correo institucional válido.');
      }
      throw new Error('No fue posible abrir el módulo. Intenta nuevamente.');
    }
    setStatus('');
    render(data);
  }catch(error){
    setStatus(error.message||'Error al cargar el proyecto.','error');
  }finally{
    if(submit) submit.disabled=false;
  }
});
$('changeEmail').addEventListener('click',()=>{
  $('institutionalEmail').value='';
  setStatus('');
  showAccess();
});
