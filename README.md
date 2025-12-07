# Scripture Studio

A production-ready scaffold for a one-stop Christianity study experience featuring a full Bible viewer, lexicon integration, sermon transcription, AI-generated devotionals, historical study references, and apologetics training tools.

## Features
- **Bible viewer** with verse-level routing, notes/highlights, and Strong's lexicon links.
- **Interlinear references** with Greek/Hebrew lexicon modal.
- **Global search** powered by Lunr.js with Postgres full-text fallback.
- **Live sermon transcription** via Web Speech API and collaborative WebSocket streaming.
- **AI devotionals & apologetics** endpoint with prompt templates and rate limiting.
- **Historical study notes** and admin editing UI.
- **Apologetics Lab** with lessons, quizzes, flashcards, and debate simulator.
- **JWT auth** with roles (user, teacher/admin) and refresh tokens.
- **PWA** basics with offline caching for recently viewed passages.
- **Docker + docker-compose** for local development with Postgres; SQLite fallback for quick start.

## Project Structure
- `frontend/` – React + Vite + TypeScript + Tailwind UI.
- `server/` – Express + TypeScript REST + WebSocket services.
- `db/` – SQL schema and seed data (KJV sample, lexicon, study notes, etc.).
- `docker-compose.yml` – App + Postgres for dev.

## Quickstart (SQLite)
1. Install Node.js 18+.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Seed SQLite with sample data:
   ```bash
   npm run db:seed
   ```
4. Run dev servers (frontend + backend concurrently):
   ```bash
   npm run dev
   ```
   - Frontend on http://localhost:5173
   - Backend on http://localhost:4000

## Running with Postgres
1. Ensure Docker and docker-compose are installed.
2. Copy `.env.example` to `.env` and set `DATABASE_URL` (Postgres) and `AI_API_KEY`.
3. Start services:
   ```bash
   docker-compose up --build
   ```
4. Apply schema and seed:
   ```bash
   npm run db:migrate && npm run db:seed
   ```

## Deployment
- Build frontend:
  ```bash
  cd frontend && npm run build
  ```
- Build backend:
  ```bash
  cd server && npm run build
  ```
- Use the provided `Dockerfile` to produce a production image bundling both server and built frontend.

## Environment Variables
- `PORT` (default 4000)
- `DATABASE_URL` (Postgres connection string)
- `SQLITE_PATH` (fallback SQLite path; defaults to `./data.sqlite`)
- `JWT_SECRET`
- `REFRESH_SECRET`
- `AI_API_KEY` (LLM provider key)
- `AI_PROVIDER_URL` (URL for the LLM; stubbed by default)
- `RATE_LIMIT_WINDOW` / `RATE_LIMIT_MAX`

## Database Scripts
- `db/schema.sql` – table definitions for users, verses, lexicon, devotionals, transcripts, annotations, flashcards, and apologetics modules.
- `db/seed.sql` – inserts sample KJV verses, lexicon entries, study notes, devotionals, and apologetics content.
- Scripts are compatible with PostgreSQL; SQLite-compatible variants are included in comments.

## Tests & Linting
- `npm run lint` (frontend) – ESLint + TypeScript.
- `npm test` (server) – placeholder for API tests.

## Notes
- Web Speech API support varies by browser. The UI offers an audio upload fallback that hits `/api/transcripts/upload`.
- LLM endpoints are abstracted to allow any provider; ensure `AI_API_KEY` is set in production.
- Include Eruda debug console on mobile during development; it is disabled in production builds.

