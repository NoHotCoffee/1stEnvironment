# CalBell

A self-hosted calorie tracker, in the spirit of apps like Cal AI, with:

- **Barcode scanning** — scan a product with your phone camera and look up its nutrition from [Open Food Facts](https://world.openfoodfacts.org/), a free/open food database.
- **Photo-based food recognition** — take a photo of a meal and get a nutrition estimate from a self-hosted, open-source image classification model. No photo or data is ever sent to a third-party API.
- **Food diary** — log meals, track calories/protein/carbs/fat against daily goals, and browse history.
- **Mobile-first installable PWA** — works like a native app on your phone's home screen, no app store required.

Everything runs on your own server: your data never leaves your machine except for the barcode lookup, which calls the public Open Food Facts API (see [Data sources](#data-sources--limitations) below).

## Architecture

- **Backend**: FastAPI (Python), SQLite storage, JWT auth. Serves both the REST API (`/api/*`) and the frontend static files from one process/container.
- **Frontend**: a dependency-free vanilla JS PWA (`frontend/`) — installable, works offline for the app shell, camera access via the browser's native `getUserMedia`/`BarcodeDetector` APIs and file input for photo capture.
- **Photo recognition**: a Hugging Face `image-classification` pipeline running a food image classifier (default: [`nateraw/food`](https://huggingface.co/nateraw/food), a ViT fine-tuned on the Food-101 dataset — 101 food categories). Runs entirely on your server/CPU; no external API calls at inference time. Nutrition per class comes from a bundled approximate nutrition table (`backend/app/data/food101_nutrition.json`).
- **Barcode lookup**: proxies to the public Open Food Facts API by barcode number.

## Running with Docker (recommended)

```bash
docker compose up --build
```

Then open `http://localhost:8000` (or your server's address) on your phone/browser and "Add to Home Screen" to install it as an app.

Set a real secret before exposing this beyond localhost:

```bash
CALBELL_SECRET_KEY="$(openssl rand -hex 32)" docker compose up --build
```

Data (the SQLite database and the downloaded model weights) persists in the `calbell_data` Docker volume, so it survives container restarts/rebuilds.

### First-time model download

The food recognition model (a few hundred MB) is downloaded from Hugging Face the first time a photo is analyzed, and cached in the persisted volume from then on — so the container needs outbound internet access at least once. After that, recognition works fully offline.

## Running locally without Docker

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000`.

## Configuration

All settings are environment variables prefixed with `CALBELL_` (see `backend/app/config.py`):

| Variable | Default | Purpose |
|---|---|---|
| `CALBELL_SECRET_KEY` | `change-me-in-production` | JWT signing secret — **set this** before exposing the server. |
| `CALBELL_DATABASE_URL` | `sqlite:///./data/calbell.db` | SQLite database location. |
| `CALBELL_FOOD_MODEL_NAME` | `nateraw/food` | Hugging Face model used for photo recognition. |
| `CALBELL_FOOD_MODEL_TOP_K` | `3` | Number of food candidates returned per photo. |
| `CALBELL_DEFAULT_SERVING_GRAMS` | `150` | Default serving size suggested after photo recognition. |
| `CALBELL_ACCESS_TOKEN_EXPIRE_MINUTES` | `10080` (7 days) | Login session length. |

## Data sources & limitations

- **Barcode nutrition data** comes from [Open Food Facts](https://world.openfoodfacts.org/), a free, collaborative, open database — no API key required. Coverage varies by region/brand; some barcodes won't be found.
- **Photo recognition** classifies the food into one of 101 Food-101 categories (mixed dishes, not raw ingredients) and estimates calories/macros from a fixed **per-100g average**, not the actual portion in your photo — it does not do portion-size estimation from the image. Always double-check and adjust the serving size before logging. Nutrition values in `food101_nutrition.json` are reasonable estimates, not lab-measured figures.
- Barcode scanning uses the browser's native `BarcodeDetector` API, available in Chromium-based browsers (Chrome/Edge on Android and desktop). Safari/Firefox don't support it yet — those browsers fall back to manual barcode entry.

## Project layout

```
backend/
  app/
    main.py           FastAPI app, mounts API + static frontend
    models.py          SQLModel tables (User, FoodEntry)
    routers/            auth, diary, barcode, recognize endpoints
    services/            Open Food Facts client, food classifier
    data/                Food-101 -> nutrition mapping
  Dockerfile
frontend/
  index.html, css/, js/, manifest.webmanifest, sw.js, icons/
docker-compose.yml
```
