import { useEffect, useState } from 'react';

interface Module {
  id: number;
  title: string;
  lessons: { id: string; title: string; body: string }[];
  quizzes: any[];
}

export default function Apologetics() {
  const [modules, setModules] = useState<Module[]>([]);
  const [feedback, setFeedback] = useState('');

  useEffect(() => {
    fetch('/api/apologetics/modules')
      .then((r) => r.json())
      .then(setModules);
  }, []);

  const answerQuiz = async (moduleId: number, quizId: string, answer: string) => {
    const res = await fetch('/api/apologetics/quiz/answer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ moduleId, quizId, answer }),
    });
    const json = await res.json();
    setFeedback(json.correct ? 'Correct!' : `Expected: ${json.expected}`);
  };

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Apologetics Lab</h1>
      {modules.map((m) => (
        <div key={m.id} className="card space-y-2">
          <h2 className="font-semibold text-lg">{m.title}</h2>
          {m.lessons.map((l) => (
            <div key={l.id}>
              <p className="text-sm font-semibold">{l.title}</p>
              <p className="text-sm text-gray-700">{l.body}</p>
            </div>
          ))}
          {m.quizzes.map((q) => (
            <div key={q.id} className="mt-2">
              <p className="text-sm">{q.question}</p>
              <input className="border rounded px-2 py-1" placeholder="Your answer" onBlur={(e) => answerQuiz(m.id, q.id, e.target.value)} />
            </div>
          ))}
        </div>
      ))}
      {feedback && <div className="text-sm text-green-700">{feedback}</div>}
    </div>
  );
}
