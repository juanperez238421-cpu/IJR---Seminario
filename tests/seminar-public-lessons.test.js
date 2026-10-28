import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import vm from 'node:vm';

const source=await readFile('t3/access-gate.js','utf8');

async function simulate(pathname){
  const css=new Set();
  let gateMounted=false;
  let gateElement=null;
  const element=()=>({
    style:{},innerHTML:'',value:'',disabled:false,
    setAttribute(){},addEventListener(){},focus(){},remove(){},
    querySelector(){return element()}
  });
  const document={
    readyState:'complete',
    documentElement:{classList:{add(v){css.add(v)},remove(v){css.delete(v)}},dataset:{}},
    createElement(){return element()},
    head:{appendChild(){}},
    body:{appendChild(el){gateMounted=true;gateElement=el}},
    getElementById(id){return id==='ijrSeminarAccessGate'&&gateMounted?gateElement:null}
  };
  const window={location:{pathname},dispatchEvent(){}};
  const localStorage={getItem(){return null},removeItem(){},setItem(){}};
  vm.runInNewContext(source,{window,document,localStorage,
    requestAnimationFrame(fn){fn()},
    CustomEvent:class {},
    fetch(){throw new Error('No network required for public lessons')}
  },{filename:'access-gate.js'});
  await new Promise(resolve=>setImmediate(resolve));
  return {gateMounted,pending:css.has('ijr-seminar-access-pending'),access:window.IJRSeminarAccess};
}

test('public learning material works without any code or email',async()=>{
  const paths=[
    '/IJR---Seminario/t3/',
    '/IJR---Seminario/t3/index.html',
    '/IJR---Seminario/t3/common/',
    '/IJR---Seminario/t3/lab.html',
    '/IJR---Seminario/t3/oop-logic-01/',
    '/IJR---Seminario/t3/oop-uml/',
    '/IJR---Seminario/t3/oop-uml/theory.html',
    '/IJR---Seminario/t3/oop-uml/workshop.html',
    '/IJR---Seminario/t3/studio/',
    '/IJR---Seminario/t3/tracks/robotics/',
    '/IJR---Seminario/t3/projects/cyber-cases/case-01-http-flood.html',
    '/IJR---Seminario/t3/projects/student-workshops/rico-paramo/workshop.html'
  ];
  for(const path of paths){
    const result=await simulate(path);
    assert.equal(result.gateMounted,false,'unexpected gate: '+path);
    assert.equal(result.pending,false,'hidden content: '+path);
    assert.equal((await result.access.ready).publicContent,true,'missing ready state: '+path);
  }
});

test('personal projects and teacher routes keep their access gates',async()=>{
  const paths=[
    '/IJR---Seminario/t3/projects/',
    '/IJR---Seminario/t3/projects/workspace/',
    '/IJR---Seminario/t3/projects/workspace/unit.html',
    '/IJR---Seminario/t3/studio/projects/',
    '/IJR---Seminario/t3/teacher.html'
  ];
  for(const path of paths){
    const result=await simulate(path);
    assert.equal(result.gateMounted,true,'missing gate: '+path);
    assert.equal(result.pending,true,'private route unexpectedly visible: '+path);
  }
});
