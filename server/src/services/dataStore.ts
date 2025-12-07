import fs from 'fs';
import path from 'path';
import { Verse, LexiconEntry, StudyNote, Devotional, Transcript, ApologeticsModule, Flashcard } from '../types.js';

export interface DataContext {
  verses: Verse[];
  lexicon: LexiconEntry[];
  studyNotes: StudyNote[];
  devotionals: Devotional[];
  transcripts: Transcript[];
  apologeticsModules: ApologeticsModule[];
  flashcards: Flashcard[];
}

function loadJson<T>(file: string): T {
  const filepath = path.join(path.resolve(), 'server', 'src', 'data', file);
  const fallbackPath = path.join(path.resolve(), 'src', 'data', file);
  const actual = fs.existsSync(filepath) ? filepath : fallbackPath;
  return JSON.parse(fs.readFileSync(actual, 'utf-8')) as T;
}

export function buildDataContext(): DataContext {
  return {
    verses: loadJson<Verse[]>('verses.json'),
    lexicon: loadJson<LexiconEntry[]>('lexicon.json'),
    studyNotes: loadJson<StudyNote[]>('studyNotes.json'),
    devotionals: loadJson<Devotional[]>('devotionals.json'),
    transcripts: [],
    apologeticsModules: loadJson<ApologeticsModule[]>('apologeticsModules.json'),
    flashcards: loadJson<Flashcard[]>('flashcards.json'),
  };
}

export const data = buildDataContext();

export function addTranscript(record: Omit<Transcript, 'id'>) {
  const id = data.transcripts.length + 1;
  const transcript: Transcript = { id, ...record };
  data.transcripts.push(transcript);
  return transcript;
}

export function upsertDevotional(dev: Omit<Devotional, 'id'> & { id?: number }) {
  if (dev.id) {
    const idx = data.devotionals.findIndex((d) => d.id === dev.id);
    if (idx >= 0) {
      data.devotionals[idx] = { ...data.devotionals[idx], ...dev } as Devotional;
      return data.devotionals[idx];
    }
  }
  const id = data.devotionals.length + 1;
  const newDev: Devotional = { id, ...dev } as Devotional;
  data.devotionals.push(newDev);
  return newDev;
}
