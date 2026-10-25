const test = require('node:test');
const assert = require('node:assert/strict');
const { getJwtSecret } = require('../app_api/config/auth');

test('authentication refuses an absent or short JWT secret', () => {
  const original = process.env.JWT_SECRET;
  try {
    delete process.env.JWT_SECRET;
    assert.throws(() => getJwtSecret(), /JWT_SECRET/);
    process.env.JWT_SECRET = 'short';
    assert.throws(() => getJwtSecret(), /JWT_SECRET/);
  } finally {
    if (original === undefined) delete process.env.JWT_SECRET;
    else process.env.JWT_SECRET = original;
  }
});

test('authentication accepts an explicitly configured secret', () => {
  const original = process.env.JWT_SECRET;
  try {
    process.env.JWT_SECRET = 'this-is-a-local-test-value-with-32-chars';
    assert.equal(getJwtSecret(), process.env.JWT_SECRET);
  } finally {
    if (original === undefined) delete process.env.JWT_SECRET;
    else process.env.JWT_SECRET = original;
  }
});
