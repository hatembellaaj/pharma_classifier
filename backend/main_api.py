"""FastAPI entry point exposing the Pharma Classifier pipeline."""
from __future__ import annotations

import sys
from pathlib import Path
from io import BytesIO

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from config import settings  # noqa: E402
from core.pipeline import run_pipeline  # noqa: E402
from export.exporter import export_results  # noqa: E402
from export.update_history import update_history  # noqa: E402
from utils.progress_log import ProgressLog  # noqa: E402
from utils.history import normalize_history_dataframe  # noqa: E402

app = FastAPI(title="Pharma Classifier API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LATEST_OUTPUT = settings.OUTPUT_DIR / "resultat_v2.csv"
progress_log = ProgressLog(settings.LOG_PATH)


class RunRequest(BaseModel):
    file_path: str


@app.get("/")
def root() -> dict[str, str]:
    """Basic landing endpoint used for uptime checks."""

    return {
        "message": "Pharma Classifier API is running",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)) -> dict[str, str]:
    file_path = settings.UPLOAD_DIR / file.filename
    contents = await file.read()
    file_path.write_bytes(contents)
    return {"message": "Fichier reçu", "path": str(file_path)}


@app.post("/run")
def run_pipeline_endpoint(payload: RunRequest) -> dict[str, object]:
    file_path = Path(payload.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Fichier introuvable")
    df = pd.read_csv(file_path, dtype=str).fillna("")
    progress_log.reset()
    df_v2 = run_pipeline(df, progress_logger=progress_log)
    export_results(df_v2, LATEST_OUTPUT)
    update_history(df_v2, settings.HISTORY_PATH)
    return {
        "message": "Pipeline terminé",
        "output": str(LATEST_OUTPUT),
        "rows": len(df_v2),
        "logs": progress_log.read(),
    }


@app.get("/run/logs")
def get_run_logs() -> dict[str, object]:
    return {"lines": progress_log.read()}


@app.get("/results")
def get_results() -> dict[str, object]:
    if not LATEST_OUTPUT.exists():
        raise HTTPException(status_code=404, detail="Aucun fichier généré")
    df = pd.read_csv(LATEST_OUTPUT, dtype=str).fillna("")
    return {"records": df.to_dict(orient="records")}


@app.get("/download")
def download_result() -> FileResponse:
    if not LATEST_OUTPUT.exists():
        raise HTTPException(status_code=404, detail="Aucun fichier généré")
    return FileResponse(path=LATEST_OUTPUT, filename=LATEST_OUTPUT.name)


@app.get("/history")
def get_history() -> dict[str, object]:
    if not settings.HISTORY_PATH.exists():
        return {"records": []}
    df = pd.read_csv(settings.HISTORY_PATH, dtype=str).fillna("")
    df = normalize_history_dataframe(df)
    return {"records": df.to_dict(orient="records")}


@app.post("/history/upload")
async def upload_history(file: UploadFile = File(...)) -> dict[str, str]:
    settings.HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    contents = await file.read()
    try:
        df = pd.read_csv(BytesIO(contents), dtype=str).fillna("")
    except Exception as exc:  # pragma: no cover - defensive for malformed CSV
        raise HTTPException(status_code=400, detail=f"CSV invalide: {exc}")
    normalized = normalize_history_dataframe(df)
    try:
        normalized.to_csv(settings.HISTORY_PATH, index=False)
    except OSError as exc:
        raise HTTPException(status_code=500, detail=f"Impossible d'enregistrer l'historique: {exc}")
    return {
        "message": "Historique importé avec succès",
        "path": str(settings.HISTORY_PATH),
        "filename": file.filename,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main_api:app", host="0.0.0.0", port=8000, reload=True)
