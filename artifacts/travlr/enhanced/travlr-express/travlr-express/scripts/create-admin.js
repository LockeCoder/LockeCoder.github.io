// Offline administrator provisioning, not exposed as an API endpoint.
const mongoose = require('mongoose');
const { getJwtSecret } = require('../app_api/config/auth');
require('../app_api/models/users');
const User = mongoose.model('users');

async function main() {
  getJwtSecret(); // Refuse incomplete auth configuration.
  const name = (process.env.ADMIN_NAME || '').trim();
  const email = (process.env.ADMIN_EMAIL || '').trim().toLowerCase();
  const password = process.env.ADMIN_PASSWORD || '';
  if (!name || !/^\S+@\S+\.\S+$/.test(email) || password.length < 12) {
    throw new Error('Set ADMIN_NAME, ADMIN_EMAIL, and an ADMIN_PASSWORD of at least 12 characters');
  }

  const uri = process.env.MONGO_URI || 'mongodb://127.0.0.1/travlr';
  await mongoose.connect(uri);
  const existing = await User.findOne({ email });
  if (existing) throw new Error('That account already exists; review it manually before granting administrator access');
  const user = new User({ name, email, role: 'admin' });
  user.setPassword(password);
  await user.save();
  console.log('Administrator account created.');
}

main()
  .catch((error) => { console.error(error.message); process.exitCode = 1; })
  .finally(async () => { await mongoose.disconnect(); });
