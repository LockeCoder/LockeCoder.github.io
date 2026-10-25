const jwt = require('jsonwebtoken');
const { getJwtSecret } = require('../config/auth');

function auth(req, res, next) {
  const tokenMatch = /^Bearer\s+(\S+)$/i.exec(req.headers.authorization || '');
  if (!tokenMatch) {
    return res.status(401).json({ message: 'Authorization token required' });
  }

  let secret;
  try {
    secret = getJwtSecret();
  } catch (_) {
    return res.status(503).json({ message: 'Authentication is not configured' });
  }

  try {
    const decoded = jwt.verify(tokenMatch[1], secret, { algorithms: ['HS256'] });
    if (!decoded || decoded.role !== 'admin' || !decoded._id) {
      return res.status(403).json({ message: 'Administrator access required' });
    }
    req.auth = decoded;
    return next();
  } catch (_) {
    return res.status(401).json({ message: 'Invalid or expired token' });
  }
}

module.exports = auth;
