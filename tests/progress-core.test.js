import test from "node:test";
import assert from "node:assert/strict";

import {
  calculateProgress,
  calculateWeightedGrade,
  createEmptyCriteria,
  createEmptyMilestones,
  getCommitReviewState,
  normalizeRepository,
} from "../js/progress-core.js";

test("calcula la nota ponderada cuando la rúbrica está completa", () => {
  const grade = calculateWeightedGrade({
    functionality: 4,
    technical: 3.5,
    explanation: 4.5,
    liveChange: 4,
    gitDocs: 3,
  });

  assert.equal(grade, 3.88);
});

test("mantiene la nota pendiente si falta un criterio", () => {
  const criteria = createEmptyCriteria();
  criteria.functionality = 4;
  assert.equal(calculateWeightedGrade(criteria), null);
});

test("calcula porcentaje de metas", () => {
  const milestones = createEmptyMilestones();
  milestones.html = true;
  milestones.css = true;
  milestones.javascript = true;

  assert.deepEqual(calculateProgress(milestones), {
    completed: 3,
    total: 10,
    percentage: 30,
  });
});

test("normaliza URLs y nombres de repositorio", () => {
  assert.equal(
    normalizeRepository("https://github.com/usuario/proyecto.git"),
    "usuario/proyecto"
  );
});

test("detecta commits pendientes y revisados", () => {
  assert.equal(getCommitReviewState("abc123", "abc123"), "reviewed");
  assert.equal(getCommitReviewState("def456", "abc123"), "new");
  assert.equal(getCommitReviewState("def456", null), "new");
  assert.equal(getCommitReviewState(null, null), "unknown");
});
