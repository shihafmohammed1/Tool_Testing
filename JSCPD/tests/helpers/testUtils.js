const { test } = require('node:test');
const assert = require('node:assert/strict');

function assertThrows(fn, expectedMessage) {
  assert.throws(fn, (error) => error.message.includes(expectedMessage));
}

function assertValidId(record) {
  assert.match(record.id, /^[0-9a-f-]{36}$/i);
  assert.ok(record.createdAt);
}

module.exports = {
  test,
  assert,
  assertThrows,
  assertValidId,
};
