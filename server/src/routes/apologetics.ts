import { Router } from 'express';
import { data } from '../services/dataStore.js';

const router = Router();

router.get('/modules', (_req, res) => {
  res.json(data.apologeticsModules);
});

router.post('/quiz/answer', (req, res) => {
  const { moduleId, quizId, answer } = req.body;
  const module = data.apologeticsModules.find((m) => m.id === Number(moduleId));
  const quiz = module?.quizzes.find((q: any) => q.id === quizId);
  const correct = quiz?.answer ? quiz.answer.toLowerCase().trim() === String(answer).toLowerCase().trim() : false;
  res.json({ correct, expected: quiz?.answer });
});

export default router;
