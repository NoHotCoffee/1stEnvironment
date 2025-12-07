import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import http from 'http';
import path from 'path';
import authRoutes from './routes/auth.js';
import bibleRoutes from './routes/bible.js';
import lexiconRoutes from './routes/lexicon.js';
import searchRoutes from './routes/search.js';
import transcriptRoutes from './routes/transcripts.js';
import aiRoutes from './routes/ai.js';
import apologeticsRoutes from './routes/apologetics.js';
import notesRoutes from './routes/notes.js';
import { setupTranscriptSocket } from './ws/transcript.js';

dotenv.config();

const app = express();
app.use(cors());
app.use(helmet());
app.use(express.json());

app.get('/health', (_req, res) => res.json({ status: 'ok' }));

app.use('/api/auth', authRoutes);
app.use('/api/bible', bibleRoutes);
app.use('/api/lexicon', lexiconRoutes);
app.use('/api/search', searchRoutes);
app.use('/api/transcripts', transcriptRoutes);
app.use('/api/ai', aiRoutes);
app.use('/api/apologetics', apologeticsRoutes);
app.use('/api/notes', notesRoutes);

const distPath = path.join(path.resolve(), 'frontend', 'dist');
app.use(express.static(distPath));
app.get('*', (_req, res) => {
  res.sendFile(path.join(distPath, 'index.html'));
});

const server = http.createServer(app);
setupTranscriptSocket(server);

const port = Number(process.env.PORT || 4000);
server.listen(port, () => {
  console.log(`Server listening on http://localhost:${port}`);
});
