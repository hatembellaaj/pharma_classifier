"""FastAPI entry point for the pharma classifier backend."""

from fastapi import FastAPI

app = FastAPI(title="Pharma Classifier API")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Basic liveness probe endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main_api:app", host="0.0.0.0", port=8000, reload=True)
