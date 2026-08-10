from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="NOVA",
    version="1.0.0"
)


# ============================================================
# STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


# ============================================================
# HOME
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home():

    index_file = BASE_DIR / "templates" / "index.html"

    return index_file.read_text(encoding="utf-8")
