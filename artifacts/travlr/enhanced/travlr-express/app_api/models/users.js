const mongoose = require('mongoose');
const crypto = require('crypto');
const jwt = require('jsonwebtoken');
const { getJwtSecret } = require('../config/auth');

const MODERN_ITERATIONS = 210000;
const LEGACY_ITERATIONS = 1000; // Existing CS 465 users may use this count.

const userSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true, lowercase: true, trim: true },
  role: { type: String, enum: ['admin'], required: true },
  hash: { type: String, required: true },
  salt: { type: String, required: true },
  passwordIterations: { type: Number }
});

userSchema.methods.setPassword = function (password) {
  if (typeof password !== 'string' || password.length < 12) {
    throw new Error('Administrator passwords must contain at least 12 characters');
  }
  this.salt = crypto.randomBytes(32).toString('hex');
  this.passwordIterations = MODERN_ITERATIONS;
  this.hash = crypto.pbkdf2Sync(password, this.salt, MODERN_ITERATIONS, 64, 'sha512').toString('hex');
};

userSchema.methods.validPassword = function (password) {
  if (typeof password !== 'string' || !this.salt || !this.hash) return false;
  const rounds = this.passwordIterations || LEGACY_ITERATIONS;
  if (!Number.isSafeInteger(rounds) || rounds < LEGACY_ITERATIONS) return false;
  try {
    const expected = Buffer.from(this.hash, 'hex');
    if (expected.length !== 64) return false;
    const calculated = crypto.pbkdf2Sync(password, this.salt, rounds, 64, 'sha512');
    return crypto.timingSafeEqual(expected, calculated);
  } catch (_) {
    return false;
  }
};

userSchema.methods.generateJwt = function () {
  if (this.role !== 'admin') throw new Error('Administrator role required');
  return jwt.sign(
    { _id: String(this._id), email: this.email, role: 'admin' },
    getJwtSecret(),
    { algorithm: 'HS256', expiresIn: '2h' }
  );
};

mongoose.model('users', userSchema);
