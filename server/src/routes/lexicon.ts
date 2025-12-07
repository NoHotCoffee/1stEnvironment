import { Router } from 'express';
import { data } from '../services/dataStore.js';

const router = Router();

router.get('/:strong', (req, res) => {
  const entry = data.lexicon.find((l) => l.strong_number.toLowerCase() === req.params.strong.toLowerCase());
  if (!entry) return res.status(404).json({ error: 'Not found' });
  res.json(entry);
});

export default router;
