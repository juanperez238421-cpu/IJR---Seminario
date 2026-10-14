import test from 'node:test';
import assert from 'node:assert/strict';
import {validateRecord, filterRecords} from '../t3/projects/user-admin-reference/model.js';
test('directory input normalization and synthetic contact boundary',()=>{
  assert.deepEqual(validateRecord({alias:'  Demo  ',contact:' DEMO@EXAMPLE.TEST ',category:' member '}),{alias:'Demo',contact:'demo@example.test',category:'member'});
  for(const contact of ['real@gmail.com','bad','a b@example.test','a@@example.test'])assert.throws(()=>validateRecord({alias:'Demo',contact,category:'member'}));
  assert.throws(()=>validateRecord({alias:'x',contact:'a@example.test',category:'member'}));
  assert.throws(()=>validateRecord({alias:'Demo',contact:'a@example.test',category:''}));
});
test('search handles case, empty results and status without mutating source',()=>{
  const rows=[{alias:'Ana',contact:'ana@example.test',status:'active'},{alias:'Luis',contact:'luis@example.test',status:'archived'}];
  assert.deepEqual(filterRecords(rows,'ANA','all'),[rows[0]]);
  assert.deepEqual(filterRecords(rows,'','archived'),[rows[1]]);
  assert.deepEqual(filterRecords(rows,'missing','all'),[]);
  assert.equal(rows.length,2);
});
