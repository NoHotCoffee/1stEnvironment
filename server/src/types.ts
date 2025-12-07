export interface Verse {
  id: number;
  book: string;
  chapter: number;
  verse: number;
  translation: string;
  text: string;
  strong_refs: { word: string; strong: string }[];
}

export interface LexiconEntry {
  id: number;
  strong_number: string;
  lemma: string;
  transliteration: string;
  language: string;
  morphology?: string;
  gloss?: string;
  example_verses?: string;
  source_url?: string;
}

export interface StudyNote {
  verse_id: number;
  content: Record<string, unknown>;
}

export interface Devotional {
  id: number;
  title: string;
  verse_refs: string;
  content: string;
  tone: string;
  audience: string;
  length?: string;
  author_id?: number;
  published?: boolean;
}

export interface Transcript {
  id: number;
  title?: string;
  speaker?: string;
  start_time?: string;
  end_time?: string;
  text?: string;
  raw_audio_url?: string;
  created_by?: number;
}

export interface ApologeticsModule {
  id: number;
  title: string;
  lessons: any[];
  quizzes: any[];
}

export interface Flashcard {
  id: number;
  user_id: number;
  front: string;
  back: string;
  efactor?: number;
  interval?: number;
  next_review?: string;
}
