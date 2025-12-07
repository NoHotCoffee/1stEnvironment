INSERT INTO users (email, name, password_hash, role) VALUES
('admin@example.com', 'Admin', '$2b$10$samplehash', 'admin'),
('teacher@example.com', 'Teacher', '$2b$10$samplehash', 'teacher'),
('user@example.com', 'User', '$2b$10$samplehash', 'user');

INSERT INTO verses (book, chapter, verse, translation, text, strong_refs) VALUES
('Genesis', 1, 1, 'KJV', 'In the beginning God created the heaven and the earth.', '[{"word":"God","strong":"H430"}]'),
('John', 1, 1, 'KJV', 'In the beginning was the Word, and the Word was with God, and the Word was God.', '[{"word":"Word","strong":"G3056"}]'),
('John', 3, 16, 'KJV', 'For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.', '[{"word":"love","strong":"G25"}]');

INSERT INTO lexicon (strong_number, lemma, transliteration, language, morphology, gloss, example_verses, source_url) VALUES
('H430', 'אֱלֹהִים', 'Elohim', 'heb', 'plural noun', 'God, gods, judges', 'Gen 1:1', 'https://biblehub.com/hebrew/430.htm'),
('G3056', 'λόγος', 'logos', 'gre', 'noun', 'word, message, logic', 'John 1:1', 'https://biblehub.com/greek/3056.htm'),
('G25', 'ἀγαπάω', 'agapao', 'gre', 'verb', 'to love', 'John 3:16', 'https://biblehub.com/greek/25.htm');

INSERT INTO study_notes (verse_id, content, created_by) VALUES
(1, '{"historical": "Links to early Jewish cosmology notes.", "patristic": ["Origen on creation"], "commentary": "Focus on God as sole Creator."}', 1),
(2, '{"historical": "Early church fathers on Logos theology.", "patristic": ["Athanasius"], "commentary": "Eternity of the Word."}', 1);

INSERT INTO devotionals (title, verse_refs, content, tone, audience, length, author_id, published) VALUES
('God Creates', 'Genesis 1:1', 'Reflect on God as Creator today.', 'reflective', 'adult', 'short', 2, true),
('Love of God', 'John 3:16', 'Celebrate the depth of divine love.', 'pastoral', 'teen', 'medium', 2, false);

INSERT INTO apologetics_modules (title, lessons, quizzes) VALUES
('Reliability of Scripture', '[{"id":"l1","title":"Manuscript Evidence","body":"Overview of manuscripts"}]', '[{"id":"q1","question":"How many manuscripts?","type":"short","answer":"thousands"}]');

INSERT INTO flashcards (user_id, front, back) VALUES
(3, 'What does Logos mean?', 'Word, reason, message');

INSERT INTO annotations (user_id, verse_id, content, visibility) VALUES
(3, 2, 'This verse ties to Genesis 1:1', 'public');
