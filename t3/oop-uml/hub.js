import {CourseStore} from '../js/course-store.js';

const cfg=window.IJR_SEMINAR_T3_CONFIG;
const data=window.IJR_OOP_UML_DATA;
const store=new CourseStore(cfg);
const $=id=>document.getElementById(id);
const ACCESS_KEY='ijr-seminario-email-access-v1';
let attempt=null;

function esc(v=''){return String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function completeMode(mode){return ['solved','revealed','skipped'].includes(mode);}
function topicDone(topic){return !!attempt&&topic.modules.every(m=>completeMode(attempt.records?.[m]?.mode));}
function topicStarted(topic){return !!attempt&&topic.modules.some(m=>attempt.records?.[m]);}
function language(){return attempt?.language||'python';}
function status(topic){if(topicDone(topic))return {label:'Completed',cls:'done'};if(topicStarted(topic))return {label:'In progress',cls:''};return {label:'Available',cls:''};}
function normalizeEmail(v){return String(v||'').trim().toLowerCase();}
function institutionalEmail(v){return /^[^\s@]+@ijr\.edu\.co$/i.test(normalizeEmail(v));}
function savedAccessEmail(){
  try{
    const saved=JSON.parse(localStorage.getItem(ACCESS_KEY)||'null');
    return saved&&institutionalEmail(saved.email)?normalizeEmail(saved.email):'';
  }catch{return '';}
}
function saveAccessEmail(email){
  localStorage.setItem(ACCESS_KEY,JSON.stringify({email:normalizeEmail(email),validatedAt:Date.now()}));
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

async function submitRegistration(ev){
  ev.preventDefault();
  const email=normalizeEmail($('institutionalEmail').value);
  $('registrationStatus').className='inline-status';
  if(!institutionalEmail(email)){
    $('registrationStatus').classList.add('error');
    $('registrationStatus').textContent='Use only your institutional @ijr.edu.co email.';
    return;
  }
  $('registrationStatus').textContent='Validating institutional email…';
  $('registerButton').disabled=true;
  try{
    attempt=await store.startWithEmail({email,language:'python'});
    saveAccessEmail(email);
    $('registrationStatus').classList.add('ok');
    $('registrationStatus').textContent='Institutional identity verified.';
    render();
  }catch(err){
    $('registrationStatus').classList.add('error');
    const raw=String(err?.message||'');
    $('registrationStatus').textContent=raw.includes('institutional_email_not_registered')
      ? 'This institutional email is not linked to the official Grade 11 roster.'
      : raw.includes('institutional_email_required')
        ? 'Use only your institutional @ijr.edu.co email.'
        : (raw||'Registration failed.');
  }finally{
    $('registerButton').disabled=false;
  }
}

$('registrationForm').addEventListener('submit',submitRegistration);
$('switchButton').addEventListener('click',()=>{
  if(confirm('Switch institutional email on this computer? Saved Supabase records are not deleted.')){
    store.reset();
    localStorage.removeItem(ACCESS_KEY);
    attempt=null;
    $('institutionalEmail').value='';
    render();
  }
});

store.restore().then(a=>{
  const email=savedAccessEmail();
  if(a&&email){
    attempt={...a,email};
    render();
  }else{
    if(a&&!email)store.reset();
    attempt=null;
    render();
  }
}).catch(()=>render());
