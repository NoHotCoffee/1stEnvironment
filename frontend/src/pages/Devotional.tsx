import { useState } from 'react';

export default function Devotional() {
  const [form, setForm] = useState({ verse_refs: 'John 3:16', tone: 'reflective', length: 'short', audience: 'adult', content: '' });
  const [output, setOutput] = useState('');

  const generate = async () => {
    const res = await fetch('/api/ai/devotional', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer dummy` },
      body: JSON.stringify(form),
    });
    const data = await res.json();
    setOutput(data.content);
  };

  return (
    <div className="grid md:grid-cols-2 gap-4">
      <div className="card space-y-2">
        <h1 className="text-xl font-semibold">Generate Devotional</h1>
        <input
          className="border rounded px-3 py-2 w-full"
          value={form.verse_refs}
          onChange={(e) => setForm({ ...form, verse_refs: e.target.value })}
          placeholder="Verse refs (e.g., John 3:16)"
        />
        <div className="grid grid-cols-2 gap-2">
          <select className="border rounded px-3 py-2" value={form.tone} onChange={(e) => setForm({ ...form, tone: e.target.value })}>
            <option value="reflective">Reflective</option>
            <option value="pastoral">Pastoral</option>
            <option value="apologetic">Apologetic</option>
          </select>
          <select className="border rounded px-3 py-2" value={form.length} onChange={(e) => setForm({ ...form, length: e.target.value })}>
            <option value="short">Short</option>
            <option value="medium">Medium</option>
            <option value="long">Long</option>
          </select>
        </div>
        <select className="border rounded px-3 py-2" value={form.audience} onChange={(e) => setForm({ ...form, audience: e.target.value })}>
          <option value="teen">Teen</option>
          <option value="adult">Adult</option>
          <option value="scholarly">Scholarly</option>
        </select>
        <textarea
          className="border rounded px-3 py-2 w-full"
          rows={3}
          placeholder="Optional context"
          value={form.content}
          onChange={(e) => setForm({ ...form, content: e.target.value })}
        />
        <button className="bg-indigo-600 text-white px-3 py-2 rounded" onClick={generate}>
          Generate
        </button>
      </div>
      <div className="card">
        <h2 className="font-semibold mb-2">Result</h2>
        <pre className="whitespace-pre-wrap text-sm">{output}</pre>
      </div>
    </div>
  );
}
