INSERT INTO users (email, name, password_hash, role) VALUES
('admin@example.com', 'Admin', '$2b$10$samplehash', 'admin'),
('teacher@example.com', 'Teacher', '$2b$10$samplehash', 'teacher'),
('user@example.com', 'User', '$2b$10$samplehash', 'user');

INSERT INTO verses (book, chapter, verse, translation, text, strong_refs) VALUES
('Genesis', 1, 1, 'KJV', 'In the beginning God created the heaven and the earth.', '[{"word":"beginning","strong":"H7225"},{"word":"God","strong":"H430"},{"word":"created","strong":"H1254"}]'),
('Genesis', 1, 1, 'ESV', 'In the beginning, God created the heavens and the earth.', '[{"word":"beginning","strong":"H7225"},{"word":"God","strong":"H430"},{"word":"created","strong":"H1254"}]'),
('John', 1, 1, 'KJV', 'In the beginning was the Word, and the Word was with God, and the Word was God.', '[{"word":"beginning","strong":"G746"},{"word":"Word","strong":"G3056"},{"word":"God","strong":"G2316"}]'),
('John', 1, 1, 'ESV', 'In the beginning was the Word, and the Word was with God, and the Word was God.', '[{"word":"beginning","strong":"G746"},{"word":"Word","strong":"G3056"},{"word":"God","strong":"G2316"}]'),
('John', 1, 1, 'WEB', 'In the beginning was the Word, and the Word was with God, and the Word was God.', '[{"word":"beginning","strong":"G746"},{"word":"Word","strong":"G3056"},{"word":"God","strong":"G2316"}]'),
('John', 3, 16, 'KJV', 'For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.', '[{"word":"God","strong":"G2316"},{"word":"loved","strong":"G25"},{"word":"world","strong":"G2889"},{"word":"life","strong":"G2222"}]'),
('John', 3, 16, 'ESV', 'For God so loved the world, that he gave his only Son, that whoever believes in him should not perish but have eternal life.', '[{"word":"God","strong":"G2316"},{"word":"loved","strong":"G25"},{"word":"world","strong":"G2889"},{"word":"life","strong":"G2222"}]');

INSERT INTO lexicon (strong_number, lemma, transliteration, language, morphology, gloss, example_verses, source_url) VALUES
('H430', 'אֱלֹהִים', 'Elohim', 'heb', 'plural noun', 'God, gods, judges', 'Gen 1:1', 'https://biblehub.com/hebrew/430.htm'),
('G3056', 'λόγος', 'logos', 'gre', 'noun', 'word, message, logic', 'John 1:1', 'https://biblehub.com/greek/3056.htm'),
('G25', 'ἀγαπάω', 'agapao', 'gre', 'verb', 'to love', 'John 3:16', 'https://biblehub.com/greek/25.htm'),
('H7225', 'רֵאשִׁית', 'reshith', 'heb', 'feminine noun', 'beginning, first, chief', 'Gen 1:1', 'https://biblehub.com/hebrew/7225.htm'),
('H1254', 'בָּרָא', 'bara', 'heb', 'verb', 'to create, shape, form', 'Gen 1:1', 'https://biblehub.com/hebrew/1254.htm'),
('G746', 'ἀρχή', 'archē', 'gre', 'noun', 'beginning, origin, first cause', 'John 1:1', 'https://biblehub.com/greek/746.htm'),
('G2316', 'θεός', 'theos', 'gre', 'noun', 'God, deity', 'John 1:1', 'https://biblehub.com/greek/2316.htm'),
('G2889', 'κόσμος', 'kosmos', 'gre', 'noun', 'world, universe, order', 'John 3:16', 'https://biblehub.com/greek/2889.htm'),
('G2222', 'ζωή', 'zoe', 'gre', 'noun', 'life, both physical and spiritual', 'John 3:16', 'https://biblehub.com/greek/2222.htm');

INSERT INTO study_notes (verse_id, content, created_by) VALUES
(1, '{"historical": "Links to early Jewish cosmology notes.", "patristic": ["Origen on creation"], "commentary": "Focus on God as sole Creator."}', 1),
(3, '{"historical": "Early church fathers on Logos theology.", "patristic": ["Athanasius"], "commentary": "Eternity of the Word."}', 1);

INSERT INTO devotionals (title, verse_refs, content, tone, audience, length, author_id, published) VALUES
('God Creates', 'Genesis 1:1', 'Reflect on God as Creator today.', 'reflective', 'adult', 'short', 2, true),
('Love of God', 'John 3:16', 'Celebrate the depth of divine love.', 'pastoral', 'teen', 'medium', 2, false);

INSERT INTO apologetics_modules (title, lessons, quizzes) VALUES
('Reliability of Scripture', '[{"id":"l1","title":"Manuscript Evidence","body":"Overview of manuscripts"}]', '[{"id":"q1","question":"How many manuscripts?","type":"short","answer":"thousands"}]');

INSERT INTO flashcards (user_id, front, back) VALUES
(3, 'What does Logos mean?', 'Word, reason, message');

INSERT INTO annotations (user_id, verse_id, content, visibility) VALUES
(3, 2, 'This verse ties to Genesis 1:1', 'public');
