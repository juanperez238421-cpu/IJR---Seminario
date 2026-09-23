import {CourseStore} from '../js/course-store.js';

const cfg=window.IJR_SEMINAR_T3_CONFIG;
const data=window.IJR_OOP_UML_DATA;
const store=new CourseStore(cfg);
const $=id=>document.getElementById(id);
let attempt=null;

function esc(v=''){return String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function completeMode(mode){return ['solved','revealed','skipped'].includes(mode);}
function topicDone(topic){return !!attempt&&topic.modules.every(m=>completeMode(attempt.records?.[m]?.mode));}
function topicStarted(topic){return !!attempt&&topic.modules.some(m=>attempt.records?.[m]);}
function language(){return attempt?.language||'python';}
function status(topic){if(topicDone(topic))return {label:'Completed',cls:'done'};if(topicStarted(topic))return {label:'In progress',cls:''};return {label:'Available',cls:''};}
function normalizeEmail(v){return String(v||'').trim().toLowerCase();}
function institutionalEmail(v){return /^[^\s@]+@ijr\.edu\.co$/i.test(normalizeEmail(v));}
function registrationMessage(message,type=''){
  const el=$('registrationStatus');
  if(!el)return;
  el.textContent=message;
  el.className=type?('inline-status '+type):'inline-status';
}
function friendlyError(err){
  const raw=String(err?.message||'');
  if(raw.includes('institutional_email_not_registered'))return 'This institutional email is not linked to the official Grade 11 Seminar roster.';
  if(raw.includes('institutional_email_required'))return 'Use only your institutional @ijr.edu.co email.';
  if(raw.includes('invalid_student_group'))return 'Your institutional email was found, but the Grade 11 group could not be resolved.';
  return raw||'The institutional session could not be opened.';
}

function render(){
  const registered=!!attempt;
  $('registrationPanel').classList.toggle('hidden',registered);
  $('hubPanel').classList.toggle('hidden',!registered);
  $('sessionBadge').classList.toggle('hidden',!registered);
  $('switchButton').classList.toggle('hidden',!registered);
  if(!registered)return;

  const lang=language();
  const done=data.topics.filter(topicDone).length;
  const pct=Math.round(done/data.topics.length*100);
  $('sessionBadge').textContent=attempt.group+' · '+attempt.label;
  $('identitySummary').textContent=attempt.group+' · '+attempt.label+' · '+(lang==='python'?'Python':'Java')+' · '+(attempt.backend==='supabase'?'Supabase synchronized':'local recovery mode');
  $('languageLabel').textContent=lang==='python'?'Python':'Java';
  $('globalPercent').textContent=pct+'%';
  $('globalProgressBar').style.width=pct+'%';
  $('globalProgressCopy').textContent=done+' of '+data.topics.length+' sessions evidenced';
  $('topicGrid').innerHTML=data.topics.map(t=>{
    const st=status(t);
    const moduleText=t.modules.map(x=>x.toUpperCase()).join(' + ');
    return '<article class="topic-card">'+
      '<div class="topic-top"><span class="topic-index">SESSION '+String(t.n).padStart(2,'0')+'</span><span class="topic-status '+st.cls+'">'+st.label+'</span></div>'+
      '<div><h3>'+esc(t.title)+'</h3><p>'+esc(t.lead)+'</p></div>'+
      '<div class="topic-meta"><span>UML + OOP</span><span>'+moduleText+'</span><span>'+(lang==='python'?'Python':'Java')+'</span></div>'+
      '<div class="topic-actions"><a class="button button-light" href="theory.html?topic='+encodeURIComponent(t.slug)+'&lang='+lang+'">Theory</a><a class="button button-dark" href="workshop.html?topic='+encodeURIComponent(t.slug)+'&lang='+lang+'">Workshop</a></div>'+
      '</article>';
  }).join('');
}

async function openInstitutionalSession(){
  render();
  registrationMessage('Waiting for institutional email validation…');

  if(!window.IJRSeminarAccess?.ready){
    registrationMessage('Institutional email access gate is unavailable. Reload the page.','error');
    return;
  }

  try{
    const access=await window.IJRSeminarAccess.ready;
    const email=normalizeEmail(access?.email);
    if(!institutionalEmail(email))throw new Error('institutional_email_required');

    registrationMessage('Opening your official Seminar 11 profile…');

    let restored=await store.restore();
    if(restored&&normalizeEmail(restored.email)!==email){
      store.reset();
      restored=null;
    }

    attempt=restored||await store.startWithEmail({email,language:'python'});
    attempt={...attempt,email};
    render();
  }catch(err){
    attempt=null;
    render();
    registrationMessage(friendlyError(err),'error');
  }
}

function changeEmail(){
  store.reset();
  if(window.IJRSeminarAccess?.logout){
    window.IJRSeminarAccess.logout();
    return;
  }
  localStorage.removeItem('ijr-seminario-email-access-v1');
  location.reload();
}

$('switchButton').addEventListener('click',()=>{
  if(confirm('Switch institutional email on this computer? Saved Supabase records are not deleted.'))changeEmail();
});
$('retryEmailButton').addEventListener('click',changeEmail);

openInstitutionalSession();
