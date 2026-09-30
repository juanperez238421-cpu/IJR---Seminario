const cfg=window.IJR_SEMINAR_T3_CONFIG||{};
const API=(cfg.supabaseUrl||'https://rlfxnjbqxbozjdzkbwlz.supabase.co')+'/functions/v1/seminar-project-access';
const KEY=cfg.supabasePublishableKey||'sb_publishable_rmVOQ3Orx49KpW_4uMqYew_c2HpcA87';
const $=id=>document.getElementById(id);
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const TRACK_NAMES={web:'Web Development','data-science':'Python / Data Analyst',cybersecurity:'Defensive Cybersecurity','3d-programming':'3D + Printing',robotics:'Robotics'};
const TRACK_GUIDANCE={
  web:{
    title:'Web engineering focus',
    theory:[
      'Separate structure, presentation, behavior and data responsibilities.',
      'Define the data model and user flow before adding interface details.',
      'Validate empty, invalid and persisted states—not only the happy path.',
      'A release is complete only when the deployed flow can be reproduced.'
    ],
    workshop:'Implement the current increment in the real web project, verify it in the browser, test at least one failure/empty state and preserve the deployed or repository evidence.'
  },
  'data-science':{
    title:'Data / Python engineering focus',
    theory:[
      'Every transformation must be reproducible from the original dataset or input.',
      'Keep data loading, cleaning, analysis and presentation responsibilities explicit.',
      'A graph is evidence only when labels, units and interpretation are correct.',
      'Restart the environment and run the workflow from zero before claiming completion.'
    ],
    workshop:'Implement the current analysis or Python increment, rerun it from a clean state, verify the expected result with data/tests and preserve notebook, output or commit evidence.'
  },
  cybersecurity:{
    title:'Defensive security focus',
    theory:[
      'Work only on the authorized local/sandbox target defined by the project.',
      'Connect each threat to one control and one measurable piece of evidence.',
      'Compare the same condition before and after the defense whenever possible.',
      'Logs must support diagnosis without exposing passwords, tokens or secrets.'
    ],
    workshop:'Run the authorized local scenario, implement or verify the defensive control, compare evidence, and record the exact safe test condition so the teacher can reproduce it.'
  },
  '3d-programming':{
    title:'Parametric CAD / fabrication focus',
    theory:[
      'Model from dimensions, constraints and function—not decorative geometry first.',
      'Keep critical dimensions and tolerances explicit and editable.',
      'Validate fit, wall thickness, orientation and export before fabrication.',
      'A model is not complete until a changed parameter regenerates correctly.'
    ],
    workshop:'Build the current CAD increment, verify dimensions/constraints, export or inspect the artifact when required, and preserve screenshots, model/STL reference or measurement evidence.'
  },
  robotics:{
    title:'Control-system focus',
    theory:[
      'Make Sensor → Controller → Actuator responsibilities explicit.',
      'Represent state transitions and fail-safe behavior before hardware integration.',
      'Test deterministic input sequences and compare them with expected outputs.',
      'Invalid readings, timeout and startup/shutdown behavior are part of the design.'
    ],
    workshop:'Implement or simulate the current control increment, run a defined scenario, verify expected state/output behavior and preserve code, serial/log, video or test-matrix evidence.'
  }
};
let state={email:'',student:null,project:null,progress:null,codeWorkspace:null};
const codeState={files:new Map(),dirty:new Set(),activeKey:'',saveTimer:null,pyodide:null,runtimePromise:null,wired:false};

function setBoot(message){if($('bootStatus'))$('bootStatus').textContent=message}
function friendlyError(code){
  const map={
    project_access_denied:'Tu correo institucional no está vinculado a un estudiante activo de Seminario 11.',
    institutional_email_required:'No se encontró una identidad institucional válida.',
    project_not_defined:'Primero debes confirmar un proyecto en Project Decision Center.',
    project_not_confirmed:'Tu ruta todavía está en modo de definición. Confirma primero el tema, alcance, objetivo y herramientas en Project Decision Center.',
    invalid_project_unit:'La unidad solicitada no existe en este proyecto.',
    previous_project_unit_incomplete:'Debes aprobar la unidad anterior antes de cerrar esta.',
    project_gate_requirements_missing:'Para aprobar el gate debes revisar Theory, iniciar Workshop, completar los cuatro checks y registrar evidencia verificable.',
    backend_unavailable:'El backend del proyecto no está disponible en este momento.',
    invalid_client:'La configuración del cliente no coincide con producción.',
    project_code_not_available:'Este proyecto no usa un workspace de código.',
    invalid_code_file_key:'El nombre del archivo no es válido.',
    invalid_code_language:'Ese tipo de archivo no está habilitado para este proyecto.',
    code_file_too_large:'El archivo supera el tamaño permitido.',
    code_file_limit_reached:'Este proyecto alcanzó el máximo de archivos del workspace.',
    project_runtime_not_available:'Este proyecto guarda código, pero no tiene ejecución completa dentro del navegador.',
    runtime_mismatch:'El runtime no coincide con el tipo de proyecto.',
    project_code_required:'Guarda código real del proyecto antes de ejecutar.',
    project_code_incomplete:'Aún quedan marcadores TODO_BUILD o WRITE_HERE en el código ejecutable.',
    project_code_run_required:'Antes de aprobar este gate debes guardar y ejecutar/validar correctamente la versión actual del código.'
  };
  return map[code]||'No fue posible sincronizar el proyecto. Intenta nuevamente.';
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
async function identityEmail(){
  if(window.IJRSeminarAccess?.ready){
    const result=await window.IJRSeminarAccess.ready;
    if(result?.email)return String(result.email).trim().toLowerCase();
  }
  try{
    const saved=JSON.parse(localStorage.getItem('ijr-seminar-email-access-v2')||'null');
    if(saved?.email)return String(saved.email).trim().toLowerCase();
  }catch{}
  return '';
}
async function load(){
  const email=await identityEmail();
  if(!email){location.replace('../../index.html');return null}
  state.email=email;
  setBoot('Loading your assigned project and tracked progress…');
  const data=await api({action:'load',email});
  state.student=data.student;
  state.project=data.project;
  state.progress=data.progress||{unit_count:0,completed_units:0,started_units:0,current_unit:null,progress_percent:0,units:[]};
  state.codeWorkspace=data.code_workspace||null;
  return data;
}
function unitMeta(n){
  const list=Array.isArray(state.project?.sprints)?state.project.sprints:[];
  return list[n-1]||null;
}
function progressRow(n){
  return (state.progress?.units||[]).find(x=>Number(x.unit_no)===Number(n))||{
    unit_no:n,status:'not_started',theory_viewed:false,workshop_started:false,gate_passed:false,
    checklist:{defined:false,built:false,tested:false,evidence:false},evidence_note:'',evidence_url:'',repo_ref:''
  };
}
function projectReady(){
  const p=state.project;
  return Boolean(p?.is_defined && (p.project_mode==='fixed' || p.decision_status==='confirmed'));
}
function projectUnitLabel(){
  return state.project?.project_slug==='rico-portable-python-visual-show'?'Class':'Unit';
}
function renderPlaybook(targetId){
  const target=$(targetId);if(!target)return;
  const sections=Array.isArray(state.project?.content_sections)?state.project.content_sections:[];
  target.innerHTML=sections.length?sections.map(section=>`
    <article class="playbook-item">
      <div class="eyebrow">${esc(section.kicker||'PROJECT')}</div>
      <h4>${esc(section.title||'Project guidance')}</h4>
      ${section.body?`<p>${esc(section.body)}</p>`:''}
      ${Array.isArray(section.items)&&section.items.length?`<ul>${section.items.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`:''}
      ${Array.isArray(section.theory)&&section.theory.length?`<ul>${section.theory.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`:''}
    </article>
  `).join(''):'<p>No additional playbook sections were defined for this project.</p>';
}
function renderResources(){
  const box=$('specialResources'),links=$('resourceLinks');
  if(!box||!links)return;
  const resources=[];
  const slug=state.project?.project_slug||'';
  const track=state.project?.track_slug||'';
  if(slug==='rico-portable-python-visual-show'){
    resources.push(['Detailed 4-class reference build','../student-workshops/rico-paramo/index.html']);
    resources.push(['Reference implementation','https://github.com/juanperez238421-cpu/IJR---Seminario/tree/main/t3/projects/student-workshops/rico-paramo/reference_project']);
  }
  if(track==='cybersecurity')resources.push(['Defensive cyber case library','../cyber-cases/']);
  if(slug.includes('visual')||slug.includes('animation'))resources.push(['Python animation project reference','../python-message-animation/']);
  box.classList.toggle('hidden',resources.length===0);
  links.innerHTML=resources.map(([label,href])=>`<a href="${esc(href)}" ${String(href).startsWith('http')?'target="_blank" rel="noopener noreferrer"':''}>${esc(label)} →</a>`).join('');
}
function renderHub(){
  const p=state.project,s=state.student,progress=state.progress;
  $('bootPanel').classList.add('hidden');
  if(!projectReady()){
    $('noProjectPanel').classList.remove('hidden');
    if(p?.is_defined&&p?.project_mode==='guided_definition'){
      $('noProjectPanel').querySelector('h2').textContent='Tu proyecto aún está por definir.';
      $('noProjectPanel').querySelector('p').textContent='Tu ruta técnica existe, pero todavía debes confirmar un tema, producto, objetivo y herramientas concretas en Project Decision Center antes de registrar progreso de construcción.';
    }
    return;
  }
  $('workspacePanel').classList.remove('hidden');
  $('groupBadge').textContent=s.group_code;
  $('trackBadge').textContent=TRACK_NAMES[p.track_slug]||p.track_slug;
  $('modeBadge').textContent=p.project_mode==='fixed'?'Fixed individual project':'Guided individual project';
  $('projectTitle').textContent=p.project_title;
  $('projectSummary').textContent=p.project_summary;
  $('objective').textContent=p.objective;
  $('stackList').innerHTML=(p.stack||[]).map(x=>`<span>${esc(x)}</span>`).join('');
  $('safetyScope').textContent=p.safety_scope||'Use only the intended project scope and preserve auditable evidence.';
  $('safetyCard').classList.toggle('hidden',!p.safety_scope);
  $('progressPercent').textContent=`${progress.progress_percent||0}%`;
  $('progressBar').style.width=`${progress.progress_percent||0}%`;
  $('progressCopy').textContent=`${progress.completed_units||0} / ${progress.unit_count||0} ${projectUnitLabel().toLowerCase()}s completed`;
  $('identityLine').textContent=`${s.name} · ${s.group_code} · Supabase synchronized`;
  $('routeTitle').textContent=`${progress.unit_count} tracked ${projectUnitLabel().toLowerCase()}s · ${p.project_title}`;
  $('currentUnitBadge').textContent=progress.current_unit?`Current: ${projectUnitLabel()} ${progress.current_unit}`:'No units';

  const units=Array.isArray(p.sprints)?p.sprints:[];
  $('unitGrid').innerHTML=units.map((unit,index)=>{
    const n=index+1,row=progressRow(n),done=row.gate_passed,current=n===Number(progress.current_unit);
    const label=projectUnitLabel();
    return `<article class="unit-card ${done?'done':''} ${current?'current':''}">
      <div class="unit-top"><span class="unit-no">${esc(label.toUpperCase())} ${String(n).padStart(2,'0')}</span><span class="unit-state">${done?'GATE PASSED':row.status==='in_progress'?'IN PROGRESS':'NOT STARTED'}</span></div>
      <h4>${esc(unit.title||`${label} ${n}`)}</h4>
      <p>${esc(unit.goal||'Build and verify the next project increment.')}</p>
      <div class="deliverable"><strong>Evidence:</strong> ${esc(unit.deliverable||'Reproducible project evidence')}</div>
      <div class="unit-actions">
        <a href="unit.html?unit=${n}&mode=theory">Theory ${row.theory_viewed?'✓':''}</a>
        <a class="primary" href="unit.html?unit=${n}&mode=workshop">Workshop ${done?'✓':''}</a>
      </div>
    </article>`;
  }).join('');
  renderPlaybook('playbookGrid');
  renderResources();
}
function query(){
  const p=new URLSearchParams(location.search);
  const unit=Math.max(1,Number(p.get('unit')||1));
  const mode=p.get('mode')==='workshop'?'workshop':'theory';
  return {unit,mode};
}
function setUnitStatus(row){
  const text=row.gate_passed?'Completed · gate passed':row.status==='in_progress'?'In progress':'Not started';
  $('unitStatus').textContent=text;
}
function renderUnit(){
  const p=state.project,s=state.student,{unit,mode}=query();
  $('bootPanel').classList.add('hidden');
  if(!projectReady()){
    $('noProjectPanel').classList.remove('hidden');
    if(p?.is_defined&&p?.project_mode==='guided_definition'){
      $('noProjectPanel').querySelector('h2').textContent='Project definition required.';
      $('noProjectPanel').querySelector('p').textContent='Confirm the concrete project in Project Decision Center before opening tracked units.';
    }
    return;
  }
  const meta=unitMeta(unit);
  if(!meta){$('noProjectPanel').classList.remove('hidden');$('noProjectPanel').querySelector('h2').textContent='This project unit does not exist.';return}
  const row=progressRow(unit),guide=TRACK_GUIDANCE[p.track_slug]||TRACK_GUIDANCE.web,label=projectUnitLabel();
  $('unitPanel').classList.remove('hidden');
  $('groupBadge').textContent=s.group_code;
  $('trackBadge').textContent=TRACK_NAMES[p.track_slug]||p.track_slug;
  $('unitLabel').textContent=`${label} ${unit} / ${state.progress.unit_count}`;
  $('unitTitle').textContent=meta.title||`${label} ${unit}`;
  $('unitGoal').textContent=meta.goal||'Build and verify the next project increment.';
  $('projectNameMini').textContent=p.project_title;
  setUnitStatus(row);
  $('pageTitleTop').textContent=`${label} ${unit} · ${mode==='theory'?'Theory':'Workshop'}`;
  $('modeKicker').textContent=`${label.toUpperCase()} ${String(unit).padStart(2,'0')} · ${mode.toUpperCase()}`;

  if(mode==='theory'){
    $('theoryPanel').classList.remove('hidden');
    $('theoryObjective').textContent=meta.theory||meta.goal||p.objective;
    $('theoryDeliverable').textContent=meta.deliverable||'Reproducible project evidence';
    $('trackTheoryTitle').textContent=guide.title;
    $('trackTheoryList').innerHTML=guide.theory.map(x=>`<li>${esc(x)}</li>`).join('');
    renderPlaybook('theoryPlaybook');
    $('toWorkshop').href=`unit.html?unit=${unit}&mode=workshop`;
    const btn=$('markTheory');
    if(row.theory_viewed){btn.textContent='Theory reviewed ✓';btn.disabled=true;$('theoryStatus').textContent='Saved in Supabase.'}
    btn.addEventListener('click',async()=>{
      btn.disabled=true;$('theoryStatus').textContent='Saving…';
      try{
        const data=await saveUnit(unit,{theory_viewed:true});
        state.progress=data.progress;btn.textContent='Theory reviewed ✓';$('theoryStatus').textContent='Saved in Supabase.';
        setUnitStatus(progressRow(unit));
      }catch(error){btn.disabled=false;$('theoryStatus').textContent=friendlyError(error.code||error.message)}
    });
  }else{
    $('workshopPanel').classList.remove('hidden');
    $('workshopInstruction').textContent=meta.workshop||guide.workshop;
    $('workshopDeliverable').textContent=meta.deliverable||'Reproducible project evidence';
    $('toTheory').href=`unit.html?unit=${unit}&mode=theory`;
    document.querySelectorAll('[data-check]').forEach(input=>{
      input.checked=row.checklist?.[input.dataset.check]===true;
    });
    $('evidenceNote').value=row.evidence_note||'';
    $('evidenceUrl').value=row.evidence_url||'';
    $('repoRef').value=row.repo_ref||'';
    initCodeLab(unit);

    const previousLocked=unit>1&&!progressRow(unit-1).gate_passed;
    $('gateLock').classList.toggle('hidden',!previousLocked);
    if(row.gate_passed){
      $('passGate').disabled=true;$('passGate').textContent='Unit gate passed ✓';
    }else if(previousLocked){
      $('passGate').disabled=true;
    }

    $('saveProgress').addEventListener('click',()=>saveWorkshop(unit,false));
    $('passGate').addEventListener('click',()=>saveWorkshop(unit,true));
  }
}

const CODE_LANGUAGE_BY_EXT={
  html:'html',htm:'html',css:'css',js:'javascript',mjs:'javascript',
  py:'python',scad:'openscad',json:'json',md:'markdown',txt:'text'
};

function codeProfile(){
  return state.codeWorkspace||{enabled:false,required_for_gate:false,runtime_kind:'source',allowed_languages:[],starter_files:[],files:[],runtime:null};
}

function codeDisplayRuntime(kind){
  return ({web:'Web sandbox','python-browser':'Python · Pyodide','python-syntax':'Python syntax validator',source:'Source workspace'})[kind]||kind||'—';
}

function codeStarterContent(spec,unit){
  const title=state.project?.project_title||'Specific Project';
  const goal=unitMeta(unit)?.goal||state.project?.objective||'Build the next project increment.';
  if(spec.language==='html'){
    return '<!doctype html>\n<html lang="en">\n<head>\n  <meta charset="utf-8">\n  <meta name="viewport" content="width=device-width,initial-scale=1">\n  <title>'+title.replace(/[<>]/g,'')+'</title>\n</head>\n<body>\n  <main id="app">\n    <h1>'+title.replace(/[<>]/g,'')+'</h1>\n    <p id="status">Project workspace ready.</p>\n    <button id="primaryAction" type="button">Run project action</button>\n  </main>\n</body>\n</html>\n';
  }
  if(spec.language==='css'){
    return 'body {\n  font-family: system-ui, sans-serif;\n  margin: 0;\n  padding: 2rem;\n}\n\n#app {\n  max-width: 760px;\n  margin: 0 auto;\n}\n';
  }
  if(spec.language==='javascript'){
    return '/* TODO_BUILD: replace this starter behavior with the real Unit '+unit+' feature. */\nconst status = document.querySelector("#status");\nconst button = document.querySelector("#primaryAction");\n\nbutton?.addEventListener("click", () => {\n  status.textContent = "Build the real project behavior for: '+goal.replace(/\n/g,' ').replace(/"/g,'\\"')+'";\n  console.log("project action", { unit: '+unit+' });\n});\n';
  }
  if(spec.language==='python'){
    if(spec.key==='tests.py'){
      return '"""Project verification file. Add real assertions as the project grows."""\n\n# Example: import functions/classes from main.py and assert expected behavior.\nprint("tests.py loaded — add project-specific checks when required")\n';
    }
    return '"""'+title.replace(/"""/g,'')+'\nUnit '+unit+' project source.\n"""\n\nPROJECT_TITLE = '+JSON.stringify(title)+'\nUNIT_GOAL = '+JSON.stringify(goal)+'\n\n# TODO_BUILD: replace this starter function with the real project increment.\ndef build_increment():\n    print(PROJECT_TITLE)\n    print("Unit goal:", UNIT_GOAL)\n    return {"unit": '+unit+', "status": "starter"}\n\nif __name__ == "__main__":\n    result = build_increment()\n    print("result", result)\n';
  }
  if(spec.language==='openscad'){
    return '// '+title.replace(/\n/g,' ')+'\n// Unit '+unit+': '+goal.replace(/\n/g,' ')+'\n// TODO_BUILD: replace this starter geometry with the real parametric model.\nwidth = 40;\ndepth = 30;\nheight = 8;\n\ncube([width, depth, height]);\n';
  }
  if(spec.language==='markdown'){
    return '# '+title+'\n\n## Unit '+unit+'\n\n'+goal+'\n\nRecord design decisions, dimensions, assumptions and test evidence here.\n';
  }
  if(spec.language==='json')return '{\n  "project": '+JSON.stringify(title)+',\n  "unit": '+unit+'\n}\n';
  return title+'\nUnit '+unit+'\n'+goal+'\n';
}

function resetCodeLocal(unit){
  codeState.files.clear();
  codeState.dirty.clear();
  codeState.activeKey='';
  const workspace=codeProfile();
  const saved=Array.isArray(workspace.files)?workspace.files:[];
  if(saved.length){
    saved.forEach(row=>codeState.files.set(row.file_key,{
      file_key:row.file_key,language:row.language,content:row.content||'',revision:Number(row.revision||1),
      updated_at:row.updated_at||null,last_run_ok:row.last_run_ok===true,last_run_at:row.last_run_at||null
    }));
  }else{
    (workspace.starter_files||[]).forEach(spec=>{
      codeState.files.set(spec.key,{file_key:spec.key,language:spec.language,content:codeStarterContent(spec,unit),revision:0,updated_at:null,last_run_ok:false,last_run_at:null});
      codeState.dirty.add(spec.key);
    });
  }
  codeState.activeKey=codeState.files.keys().next().value||'';
}

function renderCodeTabs(){
  const wrap=$('codeFileTabs');if(!wrap)return;
  wrap.innerHTML=[...codeState.files.values()].map(file=>{
    const active=file.file_key===codeState.activeKey;
    const dirty=codeState.dirty.has(file.file_key);
    return '<button type="button" class="code-file-tab '+(active?'active':'')+'" data-code-file="'+esc(file.file_key)+'"><span>'+esc(file.file_key)+'</span><span class="dirty">'+(dirty?'unsaved':'r'+Number(file.revision||0))+'</span></button>';
  }).join('');
  wrap.querySelectorAll('[data-code-file]').forEach(btn=>btn.addEventListener('click',()=>selectCodeFile(btn.dataset.codeFile)));
}

function selectCodeFile(key){
  if(!codeState.files.has(key))return;
  codeState.activeKey=key;
  const file=codeState.files.get(key);
  $('projectCodeEditor').value=file.content||'';
  $('activeFileLabel').textContent=file.file_key;
  $('activeFileMeta').textContent=file.language+' · revision '+Number(file.revision||0)+(file.updated_at?' · saved '+new Date(file.updated_at).toLocaleTimeString('es-CO',{hour:'2-digit',minute:'2-digit'}):'');
  renderCodeTabs();
}

function setCodeBadge(message,kind=''){
  const el=$('codeSaveBadge');if(!el)return;
  el.textContent=message;
  el.className='runtime-badge soft'+(kind?' '+kind:'');
}

function setCodeOutput(message,status=''){
  const panel=$('codeOutputPanel'),pre=$('codeOutput');
  panel.classList.remove('error','success');
  if(status==='error')panel.classList.add('error');
  if(status==='success')panel.classList.add('success');
  pre.textContent=String(message||'');
  $('codeRunStatus').textContent=status==='success'?'PASS':status==='error'?'ERROR':'Ready';
}

function currentCodeFile(){
  return codeState.files.get(codeState.activeKey)||null;
}

async function saveCodeFile(key){
  const file=codeState.files.get(key);
  if(!file)return;
  setCodeBadge('Supabase: saving','warn');
  const result=await api({
    action:'save_code_file',
    email:state.email,
    unit_no:query().unit,
    file_key:file.file_key,
    language:file.language,
    content:file.content
  });
  const workspace=result.code_workspace;
  state.codeWorkspace=workspace;
  const saved=(workspace?.files||[]).find(row=>row.file_key===key);
  if(saved){
    file.revision=Number(saved.revision||file.revision||1);
    file.updated_at=saved.updated_at||new Date().toISOString();
    file.last_run_ok=saved.last_run_ok===true;
    file.last_run_at=saved.last_run_at||null;
  }
  codeState.dirty.delete(key);
  setCodeBadge('Supabase: saved','ok');
  if(codeState.activeKey===key)selectCodeFile(key);else renderCodeTabs();
}

async function saveAllCodeFiles(){
  const keys=[...codeState.dirty];
  for(const key of keys)await saveCodeFile(key);
}

function scheduleCodeSave(){
  clearTimeout(codeState.saveTimer);
  codeState.saveTimer=setTimeout(()=>{
    const key=codeState.activeKey;
    if(key&&codeState.dirty.has(key))saveCodeFile(key).catch(err=>setCodeBadge(friendlyError(err.code||err.message),'warn'));
  },1200);
}

function updateActiveCode(){
  const file=currentCodeFile();if(!file)return;
  file.content=$('projectCodeEditor').value;
  codeState.dirty.add(file.file_key);
  setCodeBadge('Supabase: unsaved','warn');
  renderCodeTabs();
  scheduleCodeSave();
}

function inferCodeLanguage(name){
  const ext=String(name||'').split('.').pop().toLowerCase();
  return CODE_LANGUAGE_BY_EXT[ext]||'text';
}

function addCodeFile(){
  const workspace=codeProfile();
  const name=(window.prompt('New project file name (example: utils.py, data.json, component.js)')||'').trim();
  if(!name)return;
  if(codeState.files.has(name)){selectCodeFile(name);return}
  const language=inferCodeLanguage(name);
  if(!(workspace.allowed_languages||[]).includes(language)){
    $('codeLabStatus').textContent='This file type is not enabled for this project runtime.';
    return;
  }
  const spec={key:name,language,label:name};
  codeState.files.set(name,{file_key:name,language,content:codeStarterContent(spec,query().unit),revision:0,updated_at:null,last_run_ok:false,last_run_at:null});
  codeState.dirty.add(name);
  codeState.activeKey=name;
  renderCodeTabs();
  selectCodeFile(name);
  setCodeBadge('Supabase: unsaved','warn');
}

async function ensurePyodide(){
  if(codeState.pyodide)return codeState.pyodide;
  if(codeState.runtimePromise)return codeState.runtimePromise;
  codeState.runtimePromise=(async()=>{
    $('codeRuntimeBadge').textContent='Runtime: loading Python…';
    if(typeof globalThis.loadPyodide!=='function'){
      await new Promise((resolve,reject)=>{
        const script=document.createElement('script');
        script.src='https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js';
        script.onload=resolve;script.onerror=()=>reject(new Error('Could not load Pyodide runtime.'));
        document.head.appendChild(script);
      });
    }
    codeState.pyodide=await globalThis.loadPyodide({indexURL:'https://cdn.jsdelivr.net/pyodide/v0.27.7/full/'});
    $('codeRuntimeBadge').textContent='Runtime: Python ready';
    return codeState.pyodide;
  })();
  try{return await codeState.runtimePromise}catch(err){codeState.runtimePromise=null;throw err}
}

function executableFiles(){
  return [...codeState.files.values()].filter(file=>['python','html','css','javascript','openscad'].includes(file.language));
}

function hasIncompleteMarker(){
  return executableFiles().some(file=>/TODO_BUILD|WRITE_HERE/.test(file.content||''));
}

async function runPythonWorkspace(kind){
  const py=await ensurePyodide();
  try{py.FS.mkdirTree('/project')}catch{}
  const pyFiles=[...codeState.files.values()].filter(file=>file.language==='python');
  pyFiles.forEach(file=>py.FS.writeFile('/project/'+file.file_key,file.content||''));
  const allSource=pyFiles.map(file=>file.content||'').join('\n');
  const stdout=[],stderr=[];
  py.setStdout({batched:text=>stdout.push(text)});
  py.setStderr({batched:text=>stderr.push(text)});
  try{
    if(kind==='python-browser'){
      if(typeof py.loadPackagesFromImports==='function')await py.loadPackagesFromImports(allSource);
      const main=pyFiles.find(file=>file.file_key==='main.py')||pyFiles[0];
      if(!main)throw new Error('No Python source file is available.');
      await py.runPythonAsync(
        'import sys, runpy, pathlib\n'+
        'root="/project"\n'+
        'sys.path.insert(0, root) if root not in sys.path else None\n'+
        'runpy.run_path("/project/'+main.file_key.replace(/"/g,'')+'", run_name="__main__")\n'+
        'tests=pathlib.Path("/project/tests.py")\n'+
        'runpy.run_path(str(tests), run_name="__main__") if tests.exists() and tests.read_text().strip() else None'
      );
    }else{
      await py.runPythonAsync(
        'import pathlib\n'+
        'files=sorted(pathlib.Path("/project").glob("*.py"))\n'+
        'assert files, "No Python files found"\n'+
        'for p in files:\n'+
        '    compile(p.read_text(), str(p), "exec")\n'+
        '    print("syntax OK", p.name)'
      );
    }
    return {ok:true,output:stdout.join('\n').trim()||'Python completed successfully.',error:''};
  }catch(err){
    stderr.push(String(err?.message||err));
    return {ok:false,output:stdout.join('\n').trim(),error:stderr.join('\n').trim()};
  }
}

function buildWebSrcdoc(channel){
  const get=(name)=>codeState.files.get(name)?.content||'';
  const html=get('index.html')||'<!doctype html><html><body><main id="app"></main></body></html>';
  const css=get('styles.css');
  const js=get('app.js');
  const guard='<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; img-src data: blob:; style-src \'unsafe-inline\'; script-src \'unsafe-inline\'; font-src data:;">';
  const instrument='<script>(function(){const channel='+JSON.stringify(channel)+';let errors=0;const logs=[];const send=(type,payload)=>parent.postMessage({channel,type,payload},"*");["log","warn","error"].forEach(k=>{const original=console[k];console[k]=(...args)=>{logs.push(k.toUpperCase()+" "+args.map(v=>{try{return typeof v==="string"?v:JSON.stringify(v)}catch{return String(v)}}).join(" "));original.apply(console,args)}});window.addEventListener("error",e=>{errors++;logs.push("ERROR "+e.message)});window.addEventListener("unhandledrejection",e=>{errors++;logs.push("ERROR "+String(e.reason))});setTimeout(()=>send("done",{ok:errors===0,output:logs.join("\\n"),errors}),900)})();<\/script>';
  const style='<style>'+css.replace(/<\/style/gi,'<\\/style')+'</style>';
  const app='<script>'+js.replace(/<\/script/gi,'<\\/script')+'<\/script>';
  const addon=guard+style+instrument+app;
  if(/<\/head>/i.test(html))return html.replace(/<\/head>/i,guard+style+'</head>').replace(/<\/body>/i,instrument+app+'</body>');
  return '<!doctype html><html><head>'+guard+style+'</head><body>'+html+instrument+app+'</body></html>';
}

async function runWebWorkspace(){
  const frame=$('webPreview');
  frame.classList.remove('hidden');
  const channel='ijr-project-'+Date.now()+'-'+Math.random().toString(16).slice(2);
  return await new Promise(resolve=>{
    let finished=false;
    const done=result=>{
      if(finished)return;finished=true;
      window.removeEventListener('message',listener);
      clearTimeout(timer);
      resolve(result);
    };
    const listener=event=>{
      if(event.source!==frame.contentWindow||event.data?.channel!==channel||event.data?.type!=='done')return;
      const payload=event.data.payload||{};
      done({ok:payload.ok===true,output:payload.output||'Preview rendered.',error:payload.ok===true?'':'Browser runtime reported an error.'});
    };
    window.addEventListener('message',listener);
    const timer=setTimeout(()=>done({ok:false,output:'',error:'Preview did not finish its validation handshake.'}),3500);
    frame.srcdoc=buildWebSrcdoc(channel);
  });
}

function runSourceWorkspace(){
  const files=executableFiles();
  if(!files.length)return {ok:false,output:'',error:'No source file is available.'};
  for(const file of files){
    const text=file.content||'';
    let braces=0,parens=0;
    for(const ch of text){if(ch==='{')braces++;if(ch==='}')braces--;if(ch==='(')parens++;if(ch===')')parens--}
    if(braces!==0||parens!==0)return {ok:false,output:'',error:file.file_key+': unbalanced braces or parentheses.'};
  }
  return {ok:true,output:files.map(file=>'source check OK '+file.file_key).join('\n'),error:''};
}

function currentChecklist(){
  const checklist={};
  document.querySelectorAll('[data-check]').forEach(input=>{checklist[input.dataset.check]=input.checked});
  return checklist;
}

async function runProjectCode(unit){
  const button=$('runCode');
  button.disabled=true;button.classList.add('working');
  setCodeOutput('Saving current project files before runtime…');
  $('codeLabStatus').textContent='Saving current files…';
  try{
    updateActiveCode();
    await saveAllCodeFiles();
    if(hasIncompleteMarker())throw Object.assign(new Error('project_code_incomplete'),{code:'project_code_incomplete'});
    const kind=codeProfile().runtime_kind;
    $('codeRuntimeBadge').textContent='Runtime: '+codeDisplayRuntime(kind)+' · running';
    let result;
    if(kind==='web')result=await runWebWorkspace();
    else if(kind==='python-browser'||kind==='python-syntax')result=await runPythonWorkspace(kind);
    else result=runSourceWorkspace();

    const recorded=await api({
      action:'record_code_run',
      email:state.email,
      unit_no:unit,
      runtime_kind:kind,
      run_ok:result.ok,
      output:result.output||'',
      error:result.error||''
    });
    state.codeWorkspace=recorded.code_workspace||state.codeWorkspace;
    setCodeOutput(result.ok?(result.output||'Validation passed.'):(result.error||result.output||'Runtime failed.'),result.ok?'success':'error');
    $('codeRuntimeBadge').textContent='Runtime: '+codeDisplayRuntime(kind)+(result.ok?' · PASS':' · ERROR');
    $('codeRuntimeBadge').className='runtime-badge '+(result.ok?'ok':'warn');
    $('codeLabStatus').textContent=result.ok?'Current code version executed/validated and recorded in Supabase.':'The failed run was recorded. Fix the code and run again.';
    if(result.ok){
      const built=document.querySelector('[data-check="built"]'),tested=document.querySelector('[data-check="tested"]');
      if(built)built.checked=true;if(tested)tested.checked=true;
      const partial=await saveUnit(unit,{
        workshop_started:true,
        checklist:currentChecklist(),
        evidence_note:$('evidenceNote').value.trim(),
        evidence_url:$('evidenceUrl').value.trim(),
        repo_ref:$('repoRef').value.trim()
      });
      state.progress=partial.progress||state.progress;
      state.codeWorkspace=partial.code_workspace||state.codeWorkspace;
      setUnitStatus(progressRow(unit));
      $('codeGateStatus').textContent='Build + Test validated by the current runtime.';
    }
  }catch(error){
    setCodeOutput(friendlyError(error.code||error.message),'error');
    $('codeLabStatus').textContent=friendlyError(error.code||error.message);
    $('codeRuntimeBadge').className='runtime-badge warn';
  }finally{
    button.disabled=false;button.classList.remove('working');
  }
}

function initCodeLab(unit){
  const panel=$('codeLabPanel');if(!panel)return;
  const workspace=codeProfile();
  panel.classList.toggle('hidden',!workspace.enabled);
  if(!workspace.enabled)return;
  resetCodeLocal(unit);
  $('codeRuntimeBadge').textContent='Runtime: '+codeDisplayRuntime(workspace.runtime_kind);
  $('codeSaveBadge').textContent='Supabase: synchronized';
  $('codeSaveBadge').className='runtime-badge soft ok';
  $('codeGateStatus').textContent=workspace.required_for_gate
    ?'A successful run/validation of the current saved code is required before the unit gate.'
    :'Source is saved continuously; external artifact verification remains part of the evidence gate.';
  $('runCode').textContent=workspace.runtime_kind==='web'?'Run live preview':workspace.runtime_kind==='python-browser'?'Run Python':workspace.runtime_kind==='python-syntax'?'Validate Python syntax':'Validate source';
  $('webPreview').classList.add('hidden');
  renderCodeTabs();
  if(codeState.activeKey)selectCodeFile(codeState.activeKey);
  if(!codeState.wired){
    codeState.wired=true;
    $('projectCodeEditor').addEventListener('input',updateActiveCode);
    $('saveCodeFile').addEventListener('click',()=>{const key=codeState.activeKey;if(key)saveCodeFile(key).catch(err=>$('codeLabStatus').textContent=friendlyError(err.code||err.message))});
    $('runCode').addEventListener('click',()=>runProjectCode(query().unit));
    $('addCodeFile').addEventListener('click',addCodeFile);
  }
}

function workshopPayload(){
  const checklist=currentChecklist();
  return {
    workshop_started:true,
    checklist,
    evidence_note:$('evidenceNote').value.trim(),
    evidence_url:$('evidenceUrl').value.trim(),
    repo_ref:$('repoRef').value.trim()
  };
}
async function saveUnit(unit,patch){
  const row=progressRow(unit);
  return api({
    action:'save_progress',
    email:state.email,
    unit_no:unit,
    theory_viewed:patch.theory_viewed??row.theory_viewed,
    workshop_started:patch.workshop_started??row.workshop_started,
    gate_passed:patch.gate_passed===true,
    checklist:patch.checklist??row.checklist,
    evidence_note:patch.evidence_note??row.evidence_note,
    evidence_url:patch.evidence_url??row.evidence_url,
    repo_ref:patch.repo_ref??row.repo_ref
  });
}
async function saveWorkshop(unit,pass){
  const status=$('workshopStatus'),save=$('saveProgress'),gate=$('passGate');
  save.disabled=true;if(pass)gate.disabled=true;status.textContent=pass?'Validating gate…':'Saving progress…';
  try{
    const data=await saveUnit(unit,{...workshopPayload(),gate_passed:pass});
    state.progress=data.progress;
    state.codeWorkspace=data.code_workspace||state.codeWorkspace;
    const row=progressRow(unit);
    setUnitStatus(row);
    status.textContent=pass?'Gate passed. Progress is visible in the teacher Master panel.':'Partial progress saved in Supabase.';
    if(row.gate_passed){gate.disabled=true;gate.textContent='Unit gate passed ✓'}else{gate.disabled=false}
  }catch(error){
    status.textContent=friendlyError(error.code||error.message);
    if(!progressRow(unit).gate_passed)gate.disabled=false;
  }finally{save.disabled=false}
}
async function boot(){
  try{
    await load();
    const page=document.body.dataset.projectWorkspacePage;
    if(page==='hub')renderHub();else renderUnit();
  }catch(error){
    setBoot(friendlyError(error.code||error.message));
    $('bootPanel')?.classList.add('error');
  }
}
boot();