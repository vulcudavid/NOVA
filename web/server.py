from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pathlib import Path
from games.game_manager import GameManager
from vision.vision_module import VisionModule
import cv2
import numpy as np


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="NOVA",
    version="1.0"
)


communication_manager = None
game_manager = None
vision_module = None
difficulty_manager = None

def set_difficulty_manager(manager):

    global difficulty_manager

    difficulty_manager = manager

def set_vision_module(module):

    global vision_module

    vision_module = module

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


# ============================================================
# REACTION GAME
# ============================================================

@app.post("/api/games/reaction/start")
async def start_reaction_game():

    return game_manager.start_reaction()


@app.get("/api/games/reaction/state")
async def get_reaction_state():

    return game_manager.get_reaction_state()


@app.post("/api/games/reaction/react")
async def react_reaction_game():

    return game_manager.reaction_input()


# ============================================================
# SETTINGS
# ============================================================

@app.get("/api/settings")
async def get_settings():

    return game_manager.get_settings()

# ============================================================
# CAMERA / EMOTION DETECTION
# ============================================================

@app.post("/api/vision/frame")
async def analyze_frame(file: UploadFile = File(...)):

    if vision_module is None:
        return {
            "error": "VisionModule is not initialized"
        }

    image_bytes = await file.read()

    np_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    frame = cv2.imdecode(
        np_array,
        cv2.IMREAD_COLOR
    )

    if frame is None:
        return {
            "error": "Frame invalid"
        }

    results = vision_module.analyze_frame(frame)

    return {
        "faces": results
    }
    

class EmotionRequest(BaseModel):
    emotion: str
    confidence: float


@app.post("/api/emotion")
async def analyze_emotion(
    frame: UploadFile = File(...)
):

    if vision_module is None:
        return {
            "error": "VisionModule is not initialized"
        }

    image_bytes = await frame.read()

    np_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    image = cv2.imdecode(
        np_array,
        cv2.IMREAD_COLOR
    )

    if image is None:
        return {
            "error": "Frame invalid"
        }

    results = vision_module.analyze_frame(
        image
    )

    if not results:

        return {
            "emotion": "neutral",
            "confidence": 0.0,
            "comm_level":
                difficulty_manager.get_current_comm_level()
                if difficulty_manager is not None
                else 1
        }

    face = results[0]

    emotion = face["emotion"]
    confidence = face["confidence"]

    if difficulty_manager is not None:

        difficulty_manager.emotion_manager(
            emotion,
            confidence
        )

    current_level = (
        difficulty_manager.get_current_comm_level()
        if difficulty_manager is not None
        else 1
    )

    print(
        f"[EMOTION] {emotion} "
        f"{confidence:.2f} "
        f"comm_level={current_level}"
    )

    return {
        "emotion": emotion,
        "confidence": confidence,
        "comm_level": current_level
    }