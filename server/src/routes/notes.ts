import { Router } from 'express';
import { data } from '../services/dataStore.js';
import { authenticate } from '../middleware/auth.js';

const router = Router();

router.get('/annotations/:verseId', (req, res) => {
  const verseId = Number(req.params.verseId);
  const annotations = data.studyNotes
    .filter((n) => n.verse_id === verseId)
    .map((n) => ({ content: n.content, visibility: 'public' }));
  res.json(annotations);
});

router.post('/annotations/:verseId', authenticate, (req, res) => {
  const verseId = Number(req.params.verseId);
  const annotation = { verse_id: verseId, content: req.body.content, visibility: req.body.visibility || 'private' };
  data.studyNotes.push(annotation);
  res.json(annotation);
});

export default router;
