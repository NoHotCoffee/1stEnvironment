import { Router } from 'express';
import rateLimit from 'express-rate-limit';
import { authenticate } from '../middleware/auth.js';
import { buildDevotionalPrompt, callAI, buildApologeticsPrompt } from '../services/ai.js';
import { upsertDevotional } from '../services/dataStore.js';

const router = Router();

const limiter = rateLimit({
  windowMs: Number(process.env.RATE_LIMIT_WINDOW || 900000),
  max: Number(process.env.RATE_LIMIT_MAX || 20),
});

router.post('/devotional', authenticate, limiter, async (req, res) => {
  const { verse_refs, tone, length, audience, content } = req.body;
  const prompt = buildDevotionalPrompt({ verse_refs, tone, length, audience, content });
  const output = await callAI(prompt);
  const record = upsertDevotional({ title: `Devotional on ${verse_refs}`, verse_refs, content: output, tone, audience, length, author_id: req.user?.id });
  res.json({ prompt, content: output, record });
});

router.post('/apologetics', authenticate, limiter, async (req, res) => {
  const { topic, stance } = req.body;
  const prompt = buildApologeticsPrompt({ topic, stance });
  const output = await callAI(prompt);
  res.json({ prompt, content: output });
});

export default router;
