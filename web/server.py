from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pathlib import Path
from games.game_manager import GameManager


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="NOVA",
    version="1.0"
)


communication_manager = None
game_manager = None

def set_game_manager(manager):

    global game_manager

    game_manager = manager

# ============================================================
# COMMUNICATION MANAGER
# ============================================================

def set_communication_manager(manager):

    global communication_manager

    communication_manager = manager


# ============================================================
# STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


# ============================================================
# REQUEST MODEL
# ============================================================

class ChatRequest(BaseModel):

    text: str
    comm_level: int = 1


# ============================================================
# HOME
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home():

    index_file = (
        BASE_DIR /
        "templates" /
        "index.html"
    )

    return index_file.read_text(
        encoding="utf-8"
    )


# ============================================================
# STATUS
# ============================================================

@app.get("/api/status")
async def status():

    return {
        "status": "online",
        "name": "NOVA"
    }


# ============================================================
# CHAT
# ============================================================

@app.post("/api/chat")
async def chat(request: ChatRequest):

    if communication_manager is None:

        return {
            "error": "CommunicationManager is not initialized"
        }

    response = communication_manager.process_text(
        request.text
    )

    return response


# ============================================================
# MEMORY GAME
# ============================================================

class MemoryInput(BaseModel):

    index: int


@app.post("/api/games/memory/start")
async def start_memory_game():

    return game_manager.start_memory()


@app.post("/api/games/memory/select")
async def select_memory_card(request: MemoryInput):

    return game_manager.memory_input(
        request.index
    )


@app.post("/api/games/memory/hide")
async def hide_memory_cards():

    return game_manager.memory_hide()

@app.post("/api/games/memory/increase-level")
async def increase_memory_level():

    game_manager.increase_game_level()

    return game_manager.get_memory_state_with_difficulty()

@app.post("/api/games/memory/decrease-level")
async def decrease_memory_level():

    game_manager.decrease_game_level()

    return game_manager.get_memory_state_with_difficulty()