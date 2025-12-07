import { useEffect, useMemo, useState } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';

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

interface TranslationMeta {
  id: string;
  label: string;
}

interface BookMeta {
  book: string;
  chapters: number[];
}

export default function Bible() {
  const params = useParams();
  const navigate = useNavigate();
  const [translation, setTranslation] = useState(params.translation || 'KJV');
  const [verses, setVerses] = useState<Verse[]>([]);
  const [translations, setTranslations] = useState<TranslationMeta[]>([]);
  const [books, setBooks] = useState<BookMeta[]>([]);
  const [lexicon, setLexicon] = useState<LexiconEntry | null>(null);
  const [lexiconCache, setLexiconCache] = useState<Record<string, LexiconEntry>>({});

  const book = params.book || 'John';
  const chapter = Number(params.chapter || 1);

  useEffect(() => {
    setTranslation(params.translation || 'KJV');
  }, [params.translation]);

  useEffect(() => {
    fetch(`/api/bible/meta?translation=${translation}`)
      .then((r) => r.json())
      .then((d) => {
        setTranslations(d.translations);
        setBooks(d.books);
      });
  }, [translation]);

  useEffect(() => {
    fetch(`/api/bible/${translation}/${book}/${chapter}`)
      .then((r) => r.json())
      .then((d) => {
        setVerses(d.verses);
        const cache: Record<string, LexiconEntry> = {};
        (d.lexicon as LexiconEntry[] | undefined)?.forEach((entry) => {
          cache[entry.strong_number] = entry;
        });
        setLexiconCache(cache);
      });
  }, [translation, book, chapter]);

  const handleLexicon = async (strong: string) => {
    if (lexiconCache[strong]) {
      setLexicon(lexiconCache[strong]);
      return;
    }
    const res = await fetch(`/api/lexicon/${strong}`);
    const record = await res.json();
    setLexiconCache((prev) => ({ ...prev, [strong]: record }));
    setLexicon(record);
  };

  const renderLinkedText = (v: Verse) => {
    const escapeRegExp = (text: string) => text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

    return v.strong_refs?.reduce<(string | JSX.Element)[]>((nodes, ref, index) => {
      const pattern = new RegExp(`(\\b${escapeRegExp(ref.word)}\\b)`, 'i');
      const nextNodes: (string | JSX.Element)[] = [];
      nodes.forEach((segment) => {
        if (typeof segment !== 'string') {
          nextNodes.push(segment);
          return;
        }
        const parts = segment.split(pattern);
        if (parts.length === 1) {
          nextNodes.push(segment);
          return;
        }
        let replaced = false;
        parts.forEach((part) => {
          if (!replaced && pattern.test(part)) {
            replaced = true;
            nextNodes.push(
              <button
                key={`${v.id}-${ref.strong}-${index}-${part}`}
                className="text-indigo-700 font-semibold underline decoration-dotted underline-offset-4 focus:outline-none focus:ring focus:ring-indigo-200"
                onClick={() => handleLexicon(ref.strong)}
                aria-label={`Open lexicon for ${ref.strong}`}
              >
                {part}
                <sup className="ml-0.5 text-xs align-super">{ref.strong}</sup>
              </button>
            );
          } else if (part) {
            nextNodes.push(part);
          }
        });
      });
      return nextNodes;
    }, [v.text]) ?? v.text;
  };

  const handleTranslationChange = (value: string) => {
    const safeBook = book || 'John';
    const safeChapter = chapter || 1;
    navigate(`/bible/${value}/${safeBook}/${safeChapter}`);
  };

  const handleBookChange = (value: string) => {
    const safeChapter = books.find((b) => b.book === value)?.chapters?.[0] ?? 1;
    navigate(`/bible/${translation}/${value}/${safeChapter}`);
  };

  const chapterOptions = useMemo(() => {
    const entry = books.find((b) => b.book === book);
    return entry?.chapters ?? [chapter];
  }, [books, book, chapter]);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold">
          {params.book} {params.chapter}
        </h1>
        <div className="flex items-center gap-2">
          <Link to="/devotional" className="text-indigo-600 text-sm">
            Generate devotional
          </Link>
        </div>
      </div>

      <div className="grid gap-3 sm:grid-cols-3">
        <label className="text-sm font-medium text-gray-700 flex flex-col">
          Translation
          <select
            className="border rounded px-2 py-2 mt-1"
            value={translation}
            onChange={(e) => handleTranslationChange(e.target.value)}
          >
            {translations.map((t) => (
              <option key={t.id} value={t.id}>
                {t.label}
              </option>
            ))}
          </select>
        </label>

        <label className="text-sm font-medium text-gray-700 flex flex-col">
          Book
          <select
            className="border rounded px-2 py-2 mt-1"
            value={book}
            onChange={(e) => handleBookChange(e.target.value)}
          >
            {books.map((b) => (
              <option key={b.book} value={b.book}>
                {b.book}
              </option>
            ))}
          </select>
        </label>

        <label className="text-sm font-medium text-gray-700 flex flex-col">
          Chapter
          <select
            className="border rounded px-2 py-2 mt-1"
            value={chapter}
            onChange={(e) => navigate(`/bible/${translation}/${book}/${Number(e.target.value)}`)}
          >
            {chapterOptions.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </label>
      </div>
      <div className="space-y-3">
        {verses.map((v) => (
          <div key={v.id} className="card">
            <div className="flex justify-between items-start">
              <div>
                <div className="text-xs text-gray-500">{v.book} {v.chapter}:{v.verse}</div>
                <p className="leading-7 space-x-1 flex flex-wrap text-lg">{renderLinkedText(v)}</p>
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
