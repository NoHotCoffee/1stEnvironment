import { Router } from 'express';
import { data } from '../services/dataStore.js';

const router = Router();

router.get('/meta', (req, res) => {
  const translationQuery = req.query.translation as string | undefined;
  const translations = Array.from(new Set(data.verses.map((v) => v.translation)))
    .sort()
    .map((id) => ({ id, label: id }));

  const versesForTranslation = translationQuery
    ? data.verses.filter((v) => v.translation.toLowerCase() === translationQuery.toLowerCase())
    : data.verses;

  const books = versesForTranslation.reduce<Record<string, { chapters: Set<number> }>>((acc, v) => {
    if (!acc[v.book]) acc[v.book] = { chapters: new Set() };
    acc[v.book].chapters.add(v.chapter);
    return acc;
  }, {});

  const bookList = Object.entries(books).map(([book, info]) => ({
    book,
    chapters: Array.from(info.chapters).sort((a, b) => a - b),
  }));

  res.json({ translations, books: bookList });
});

router.get('/:translation/:book/:chapter', (req, res) => {
  const { translation, book, chapter } = req.params;
  const verses = data.verses.filter(
    (v) => v.translation.toLowerCase() === translation.toLowerCase() && v.book.toLowerCase() === book.toLowerCase() && v.chapter === Number(chapter)
  );
  const strongIds = new Set(verses.flatMap((v) => v.strong_refs?.map((s) => s.strong) ?? []));
  const lexicon = data.lexicon.filter((entry) => strongIds.has(entry.strong_number));
  res.json({ translation, book, chapter: Number(chapter), verses, lexicon });
});

router.get('/verse/:id', (req, res) => {
  const verse = data.verses.find((v) => v.id === Number(req.params.id));
  if (!verse) return res.status(404).json({ error: 'Not found' });
  const notes = data.studyNotes.find((n) => n.verse_id === verse.id);
  res.json({ verse, studyNotes: notes });
});

export default router;
