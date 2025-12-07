import lunr from 'lunr';
import { data } from './dataStore.js';

export const searchIndex = lunr(function () {
  this.ref('ref');
  this.field('type');
  this.field('content');
  data.verses.forEach((v) => {
    this.add({ ref: `verse-${v.id}`, type: 'verse', content: `${v.book} ${v.chapter}:${v.verse} ${v.text}` });
  });
  data.lexicon.forEach((l) => {
    this.add({ ref: `lex-${l.strong_number}`, type: 'lexicon', content: `${l.lemma} ${l.gloss}` });
  });
  data.devotionals.forEach((d) => {
    this.add({ ref: `dev-${d.id}`, type: 'devotional', content: `${d.title} ${d.content}` });
  });
});

export function runSearch(query: string) {
  const results = searchIndex.search(query);
  return results.map((r) => {
    const [type, id] = r.ref.split('-');
    if (type === 'verse') {
      return { type, data: data.verses.find((v) => v.id === Number(id)) };
    }
    if (type === 'lex') {
      return { type: 'lexicon', data: data.lexicon.find((l) => l.strong_number === id) };
    }
    if (type === 'dev') {
      return { type: 'devotional', data: data.devotionals.find((d) => d.id === Number(id)) };
    }
    return { type: 'unknown', data: null };
  });
}
