import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {solvedCredit,gradeFromPoints,projectedGrade,completedCount,analyzeJava} from '../t3/js/scoring-core.js';

const here=path.dirname(fileURLToPath(import.meta.url));
const payload=JSON.parse(fs.readFileSync(path.join(here,'../t3/data/course-index.json'),'utf8'));
const modules=payload.modules.map(meta=>JSON.parse(fs.readFileSync(path.join(here,'../t3/data',meta.path),'utf8')));
const route=['m01','m02','m03','m04','m05','m06','m07','m08','m09','m10','m13','m14','m11','m12','m15','m16'];

test('T3 manifest contains complete 16-module route',()=>{
  assert.equal(modules.length,16);
  assert.deepEqual([...modules].sort((a,b)=>a.routeOrder-b.routeOrder).map(m=>m.id),route);
  assert.equal(new Set(modules.map(m=>m.guide)).size,16);
  assert.deepEqual(
    ['basic','medium','advanced'].map(level=>modules.filter(m=>m.level===level).length),
    [8,4,4]
  );
});

test('every source topic preserves public instructional scaffolding without public answer material',()=>{
  for(const module of modules){
    for(const language of ['python','java']){
      const v=module[language];
      assert.ok(v.title);
      assert.ok(v.subtitle);
      assert.ok(v.objectives.length>=1);
      assert.ok(v.concept.length>=1);
      assert.ok(v.steps.length>=3);
      assert.ok(v.questions.length>=2);
      assert.ok(v.criteria.length>=2);
      assert.match(v.starter,/WRITE_HERE/);
      assert.ok(Array.isArray(v.checks));
      for(const privateField of ['hints','solution','expected','expectedPattern']){
        assert.equal(Object.hasOwn(v,privateField),false,`${module.id}/${language} must not publish ${privateField}`);
      }
    }
  }
});

test('formative scoring preserves maximum 5 and penalty floors',()=>{
  assert.equal(solvedCredit(0,0),1);
  assert.equal(solvedCredit(1,0),.8);
  assert.equal(solvedCredit(0,1),.9);
  assert.equal(solvedCredit(3,3),.25);
  assert.equal(gradeFromPoints(16),5);
  assert.equal(gradeFromPoints(0),1);
  assert.equal(projectedGrade({}),5);
  assert.equal(completedCount({m01:{mode:'solved'},m02:{mode:'revealed'},m03:{mode:'skipped'}}),3);
});

test('Java analyzer rejects unresolved scaffold and accepts structurally complete code',()=>{
  const variant={checks:['public class Main','public static void main','System.out.println',';','WRITE_HERE']};
  const starter='public class Main {\n  public static void main(String[] args) {\n    System.out.println(WRITE_HERE);\n  }\n}';
  const solved='public class Main {\n  public static void main(String[] args) {\n    System.out.println(2 + 3);\n  }\n}';
  assert.equal(analyzeJava(starter,variant).ok,false);
  const result=analyzeJava(solved,variant);
  assert.equal(result.ok,true,result.issues.join('; '));
});
