# Rooted Bible Study Hub

A comprehensive, single-page Bible study workspace that blends planning, study, memorization, journaling, and storyline context. Built with plain HTML/CSS/JS—no build step required.

## Features
- **Reading plan builder** with focus presets (Gospels, wisdom, Pauline letters, prophets), adjustable pace, and duration preview.
- **Passage study suite** showing curated passages, cross-references, keywords, and application prompts.
- **Memorization tools** including flashcards with reveal/next controls and a quick multiple-choice quiz.
- **Journal & prayer tracker** for saving notes and requests to local storage, with tabbed viewing.
- **Character explorer & timeline** to survey key people and redemptive-history milestones at a glance.
- **Daily anchor** card that rotates reflective verses/themes to start a session.

## Getting started
Open `index.html` in a browser, or run the lightweight preview server to host the page locally:

```bash
npm install
npm start
```

The server defaults to `http://localhost:4173` and falls back to `index.html` for unknown routes, making the experience previewable in hosted environments. All data is stored locally in `localStorage`; no backend or build tools are needed.
