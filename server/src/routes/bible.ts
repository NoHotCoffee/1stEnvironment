import { Router } from 'express';
import { data } from '../services/dataStore.js';

const router = Router();

router.get('/:translation/:book/:chapter', (req, res) => {
  const { translation, book, chapter } = req.params;
  const verses = data.verses.filter(
    (v) => v.translation.toLowerCase() === translation.toLowerCase() && v.book.toLowerCase() === book.toLowerCase() && v.chapter === Number(chapter)
  );
  res.json({ translation, book, chapter: Number(chapter), verses });
});

router.get('/verse/:id', (req, res) => {
  const verse = data.verses.find((v) => v.id === Number(req.params.id));
  if (!verse) return res.status(404).json({ error: 'Not found' });
  const notes = data.studyNotes.find((n) => n.verse_id === verse.id);
  res.json({ verse, studyNotes: notes });
});

export default router;
