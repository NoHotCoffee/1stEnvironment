import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

interface Verse {
  id: number;
  book: string;
  chapter: number;
  verse: number;
  text: string;
  strong_refs: { word: string; strong: string }[];
}

interface LexiconEntry {
  strong_number: string;
  lemma: string;
  transliteration: string;
  gloss: string;
  language: string;
  morphology?: string;
  example_verses?: string;
  source_url?: string;
}

export default function Bible() {
  const params = useParams();
  const [verses, setVerses] = useState<Verse[]>([]);
  const [lexicon, setLexicon] = useState<LexiconEntry | null>(null);

  useEffect(() => {
    fetch(`/api/bible/KJV/${params.book}/${params.chapter}`)
      .then((r) => r.json())
      .then((d) => setVerses(d.verses));
  }, [params.book, params.chapter]);

  const handleLexicon = async (strong: string) => {
    const res = await fetch(`/api/lexicon/${strong}`);
    setLexicon(await res.json());
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold">
          {params.book} {params.chapter}
        </h1>
        <Link to="/devotional" className="text-indigo-600 text-sm">
          Generate devotional
        </Link>
      </div>
      <div className="space-y-3">
        {verses.map((v) => (
          <div key={v.id} className="card">
            <div className="flex justify-between items-start">
              <div>
                <div className="text-xs text-gray-500">{v.book} {v.chapter}:{v.verse}</div>
                <p className="leading-7">
                  {v.text}{' '}
                  {v.strong_refs?.map((s) => (
                    <sup
                      key={s.strong}
                      className="text-indigo-600 cursor-pointer ml-1"
                      onClick={() => handleLexicon(s.strong)}
                      aria-label={`Open lexicon for ${s.strong}`}
                    >
                      {s.strong}
                    </sup>
                  ))}
                </p>
              </div>
              <button className="text-xs bg-indigo-50 px-2 py-1 rounded">Share</button>
            </div>
          </div>
        ))}
      </div>

      {lexicon && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center" role="dialog" aria-modal="true">
          <div className="bg-white rounded shadow max-w-lg w-full p-4">
            <div className="flex justify-between items-center">
              <h2 className="font-semibold text-lg">Strong&apos;s {lexicon.strong_number}</h2>
              <button onClick={() => setLexicon(null)} aria-label="Close">✕</button>
            </div>
            <p className="mt-2 text-sm text-gray-700">
              {lexicon.lemma} ({lexicon.transliteration}) · {lexicon.language.toUpperCase()}
            </p>
            <p className="text-gray-600 text-sm">{lexicon.gloss}</p>
            <p className="text-xs text-gray-500">Morphology: {lexicon.morphology}</p>
            <a className="text-indigo-600 text-sm" href={lexicon.source_url} target="_blank" rel="noreferrer">
              Source
            </a>
          </div>
        </div>
      )}
    </div>
  );
}
