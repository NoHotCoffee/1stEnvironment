import { Router } from 'express';
import { runSearch } from '../services/search.js';

const router = Router();

router.post('/', (req, res) => {
  const { q } = req.body;
  if (!q) return res.json([]);
  const results = runSearch(q);
  res.json(results);
});

export default router;
