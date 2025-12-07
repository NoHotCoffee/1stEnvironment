import { Router } from 'express';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';

const router = Router();

const users = [
  { id: 1, email: 'admin@example.com', name: 'Admin', password_hash: bcrypt.hashSync('password', 10), role: 'admin' },
  { id: 2, email: 'teacher@example.com', name: 'Teacher', password_hash: bcrypt.hashSync('password', 10), role: 'teacher' },
  { id: 3, email: 'user@example.com', name: 'User', password_hash: bcrypt.hashSync('password', 10), role: 'user' },
];

router.post('/register', (req, res) => {
  const { email, name, password } = req.body;
  const id = users.length + 1;
  const password_hash = bcrypt.hashSync(password, 10);
  users.push({ id, email, name, password_hash, role: 'user' });
  const token = jwt.sign({ id, role: 'user' }, process.env.JWT_SECRET || 'dev-secret', { expiresIn: '1h' });
  res.json({ token });
});

router.post('/login', (req, res) => {
  const { email, password } = req.body;
  const user = users.find((u) => u.email === email);
  if (!user || !bcrypt.compareSync(password, user.password_hash)) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  const token = jwt.sign({ id: user.id, role: user.role }, process.env.JWT_SECRET || 'dev-secret', { expiresIn: '1h' });
  const refresh = jwt.sign({ id: user.id, role: user.role }, process.env.REFRESH_SECRET || 'refresh-secret', { expiresIn: '7d' });
  res.json({ token, refresh });
});

router.post('/refresh', (req, res) => {
  const { refresh } = req.body;
  try {
    const decoded = jwt.verify(refresh, process.env.REFRESH_SECRET || 'refresh-secret') as any;
    const token = jwt.sign({ id: decoded.id, role: decoded.role }, process.env.JWT_SECRET || 'dev-secret', { expiresIn: '1h' });
    res.json({ token });
  } catch (err) {
    res.status(401).json({ error: 'Invalid refresh token' });
  }
});

export default router;
