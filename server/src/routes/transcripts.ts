import { Router } from 'express';
import multer from 'multer';
import { addTranscript, data } from '../services/dataStore.js';

const upload = multer({ dest: 'uploads/' });
const router = Router();

router.get('/', (_req, res) => {
  res.json(data.transcripts);
});

router.get('/:id', (req, res) => {
  const transcript = data.transcripts.find((t) => t.id === Number(req.params.id));
  if (!transcript) return res.status(404).json({ error: 'Not found' });
  res.json(transcript);
});

router.post('/', (req, res) => {
  const { title, speaker, text } = req.body;
  const transcript = addTranscript({ title, speaker, text, created_by: req.user?.id });
  res.json(transcript);
});

router.post('/upload', upload.single('audio'), (req, res) => {
  const { title, speaker } = req.body;
  const transcript = addTranscript({ title, speaker, raw_audio_url: req.file?.path, created_by: req.user?.id });
  res.json({ status: 'queued', transcript });
});

export default router;
