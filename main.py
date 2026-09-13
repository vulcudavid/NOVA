import os
import threading

import uvicorn

from communication.comm_manager import ComunicationManager
from difficulty.difficulty_manager import DifficultyManager
from activity.ActivityManager import ActivityManager
from vision.vision_module import VisionModule
from vision.vision_manager import VisionManager
from games.game_manager import GameManager
from audio.audio_manager import AudioManager
from stt.whisper_service import WhisperService

from voice.server import (
    app as voice_app,
    set_communication_manager as set_voice_communication_manager,
    set_game_manager as set_voice_game_manager,
    set_tts_manager as set_voice_tts_manager,
    set_whisper_service as set_voice_whisper_service,
    set_vision_manager as set_voice_vision_manager
)


# ============================================================
# COMMUNICATION THREAD
# ============================================================

def communication_thread(communication_manager):

    communication_manager.run()


# ============================================================
# ACTIVITY THREAD
# ============================================================

def activity_thread(activity_manager):

    while True:

        if activity_manager.is_timeout():

            message = activity_manager.get_message()

            print(message)

        import time
        time.sleep(1)


# ============================================================
# WEB SERVER THREAD
# ============================================================

def voice_server_thread():

    uvicorn.run(
        voice_app,
        host="0.0.0.0",
        port=int(os.getenv("NOVA_VOICE_PORT", "5000"))
    )


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # Difficulty Manager
    # --------------------------------------------------------

    difficulty = DifficultyManager()

    # --------------------------------------------------------
    # Activity Manager
    # --------------------------------------------------------

    activity_manager = ActivityManager()


    # --------------------------------------------------------
    # Game Manager
    # --------------------------------------------------------

    game_manager = GameManager(
        difficulty
    )

    # --------------------------------------------------------
    # Vision Module
    # --------------------------------------------------------

    vision_module = VisionModule(
        "resources/models/custom_cnn_model.tflite"
    )

    vision_manager = VisionManager(
        vision_module=vision_module,
        difficulty_manager=difficulty,
        mac_address="20:9B:A9:73:9C:F2",
        rfcomm_channel=1,
        frame_interval=0.2
    )

    set_voice_vision_manager(
        vision_manager
    )


    # --------------------------------------------------------
    # Communication Manager
    # --------------------------------------------------------

    communication_manager = ComunicationManager(
        difficulty,
        activity_manager
    )


    # --------------------------------------------------------
    # Shared objects for Voice Server
    # --------------------------------------------------------

    set_voice_communication_manager(
        communication_manager
    )

    set_voice_game_manager(
        game_manager
    )

    set_voice_whisper_service(
        WhisperService()
    )

    set_voice_tts_manager(
        AudioManager(
            "resources/audio_voice/ro_RO-mihai-medium.onnx"
        )
    )


    # --------------------------------------------------------
    # Communication Thread
    # --------------------------------------------------------

    communication = threading.Thread(
        target=communication_thread,
        args=(communication_manager,),
        name="CommunicationThread",
        daemon=True
    )


    # --------------------------------------------------------
    # Activity Thread
    # --------------------------------------------------------

    activity = threading.Thread(
        target=activity_thread,
        args=(activity_manager,),
        name="ActivityThread",
        daemon=True
    )


    # --------------------------------------------------------
    # Voice Server Thread
    # --------------------------------------------------------

    voice_server = threading.Thread(
        target=voice_server_thread,
        name="VoiceServerThread",
        daemon=True
    )


    # --------------------------------------------------------
    # Start threads
    # --------------------------------------------------------

    communication.start()

    activity.start()

    voice_server.start()


    # --------------------------------------------------------
    # Wait for threads
    # --------------------------------------------------------

    communication.join()

    activity.join()

    voice_server.join()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()