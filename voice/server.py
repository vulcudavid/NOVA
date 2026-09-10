import os
import uuid
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, Request
from pydantic import BaseModel


PROJECT_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="NOVA Voice Server",
    version="1.0"
)

communication_manager = None
whisper_service = None
tts_manager = None
game_manager = None


def set_communication_manager(manager):
    global communication_manager
    communication_manager = manager


def set_whisper_service(service):
    global whisper_service
    whisper_service = service


def set_tts_manager(manager):
    global tts_manager
    tts_manager = manager


def set_game_manager(manager):
    global game_manager
    game_manager = manager


def _create_tts_file(text):
    if tts_manager is None:
        raise RuntimeError("TTS manager is not initialized")

    output_directory = Path(
        os.getenv(
            "NOVA_AUDIO_OUTPUT_DIR",
            str(PROJECT_DIR / "resources" / "generated_audio")
        )
    )
    output_path = output_directory / f"response-{uuid.uuid4().hex}.wav"
    tts_manager.generate(text, output_path)
    return output_path


def _generate_tts_for_response(llm_response):
    try:
        response_text = (
            llm_response.get("response")
            if isinstance(llm_response, dict)
            else None
        )

        if response_text:
            _create_tts_file(response_text)
    except Exception as error:
        print(f"[VOICE] LLM/TTS processing failed: {error}")


class ChatRequest(BaseModel):
    text: str
    comm_level: int = 1


@app.get("/api/status")
async def status():
    return {
        "status": "online",
        "name": "NOVA Voice Server"
    }


@app.get("/api/settings")
async def settings():
    if game_manager is None:
        return {
            "error": "GameManager is not initialized"
        }

    return game_manager.get_settings()


@app.post("/api/chat")
async def chat(
    request: ChatRequest,
    background_tasks: BackgroundTasks
):
    if communication_manager is None:
        return {
            "error": "CommunicationManager is not initialized"
        }

    response = communication_manager.process_text(request.text)

    if isinstance(response, dict) and response.get("response"):
        background_tasks.add_task(
            _generate_tts_for_response,
            response
        )

    return response


@app.post("/api/stt")
async def speech_to_text(
    request: Request
):
    if whisper_service is None:
        return {
            "success": False,
            "text": "",
            "error": "Whisper service is not initialized"
        }

    wav_bytes = await request.body()

    try:
        text = whisper_service.transcribe(wav_bytes)
    except (RuntimeError, ValueError) as error:
        return {
            "success": False,
            "text": "",
            "error": str(error)
        }

    result = {
        "success": True,
        "text": text
    }

    return result


class TTSRequest(BaseModel):
    text: str


@app.post("/api/tts")
async def text_to_speech(request: TTSRequest):
    if not request.text.strip():
        return {
            "success": False,
            "error": "Textul TTS este gol"
        }

    try:
        audio_path = _create_tts_file(request.text)
    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }

    return {
        "success": True,
        "audio_file": str(audio_path),
        "format": "wav"
    }
