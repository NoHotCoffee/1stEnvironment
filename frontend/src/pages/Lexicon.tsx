import { useEffect, useState } from 'react';

interface LexiconEntry {
  strong_number: string;
  lemma: string;
  transliteration: string;
  gloss: string;
  language: string;
}

export default function Lexicon() {
  const [entries, setEntries] = useState<LexiconEntry[]>([]);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    fetch('/api/lexicon/H430')
      .then((r) => r.json())
      .then((entry) => setEntries([entry]));
  }, []);

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <input
          className="border rounded px-3 py-2 w-full"
          placeholder="Search Strong's number"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        />
        <button
          className="bg-indigo-600 text-white px-3 py-2 rounded"
          onClick={async () => {
            const res = await fetch(`/api/lexicon/${filter}`);
            if (res.ok) setEntries([await res.json()]);
          }}
        >
          Lookup
        </button>
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        {entries.map((e) => (
          <div key={e.strong_number} className="card">
            <div className="text-xs text-gray-500">Strong&apos;s {e.strong_number}</div>
            <div className="font-semibold">{e.lemma}</div>
            <div className="text-sm text-gray-600">{e.transliteration}</div>
            <div className="text-sm">{e.gloss}</div>
            <span className="text-xs uppercase text-gray-500">{e.language}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
