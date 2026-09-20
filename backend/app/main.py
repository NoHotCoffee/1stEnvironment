from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database import init_db
from .routers import auth, barcode, diary, recognize

app = FastAPI(title="CalBell", description="Self-hosted calorie tracker")

app.include_router(auth.router)
app.include_router(auth.users_router)
app.include_router(diary.router)
app.include_router(barcode.router)
app.include_router(recognize.router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
