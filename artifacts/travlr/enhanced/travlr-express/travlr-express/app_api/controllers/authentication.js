const mongoose = require('mongoose');
const User = mongoose.model('users');

// Administrator accounts are provisioned offline; no public registration endpoint.
const login = async (req, res) => {
  const email = typeof req.body?.email === 'string' ? req.body.email.trim().toLowerCase() : '';
  const password = req.body?.password;
  if (!email || typeof password !== 'string' || !password) {
    return res.status(400).json({ message: 'Email and password are required' });
  }

  try {
    const user = await User.findOne({ email });
    if (!user || user.role !== 'admin' || !user.validPassword(password)) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }
    // Upgrade an existing 1,000-round legacy hash when a valid password is presented.
    if (!user.passwordIterations) {
      if (password.length < 12) {
        return res.status(403).json({ message: 'Administrator must reset a weak legacy password' });
      }
      user.setPassword(password);
      await user.save();
    }
    const token = user.generateJwt();
    return res.status(200).json({ token });
  } catch (_) {
    return res.status(500).json({ message: 'Authentication service unavailable' });
  }
};

module.exports = { login };
