// One configured signing secret for both JWT creation and verification.
function getJwtSecret() {
  const value = process.env.JWT_SECRET;
  if (typeof value !== 'string' || value.length < 32) {
    throw new Error('JWT_SECRET must be configured as a random value of at least 32 characters');
  }
  return value;
}

module.exports = { getJwtSecret };
