import os
import threading

import uvicorn

from communication.comm_manager import ComunicationManager
from difficulty.difficulty_manager import DifficultyManager
from activity.ActivityManager import ActivityManager
from vision.vision_module import VisionModule
from games.game_manager import GameManager
from audio.audio_manager import AudioManager
from stt.whisper_service import WhisperService
from web.server import (
    set_game_manager,
    set_vision_module,
    set_difficulty_manager
)
from voice.server import (
    app as voice_app,
    set_communication_manager as set_voice_communication_manager,
    set_game_manager as set_voice_game_manager,
    set_tts_manager as set_voice_tts_manager,
    set_whisper_service as set_voice_whisper_service
)


# ============================================================
# COMMUNICATION THREAD
# ============================================================

def communication_thread(communication_manager):

    communication_manager.run()

# ============================================================
# EMOTION THREAD
# ============================================================

# def emotion_thread():

#     camera = Camera()

#     vision = VisionModule(
#         "resources/models/custom_cnn_model.tflite"
#     )

#     while True:

#         frame = camera.read()

#         if frame is None:
#             break

#         vision.analyze_frame(frame)

#     camera.release()


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
    # Shared objects
    # --------------------------------------------------------

    difficulty = DifficultyManager()

    activity_manager = ActivityManager()

    set_difficulty_manager(
        difficulty
    )

    game_manager = GameManager(
        difficulty
    )

    set_game_manager(
        game_manager
    )

    vision_module = VisionModule(
        "resources/models/custom_cnn_model.tflite"
    )

    set_vision_module(
        vision_module
    )


    # --------------------------------------------------------
    # Communication Manager
    # --------------------------------------------------------

    communication_manager = ComunicationManager(
        difficulty,
        activity_manager,

    )


    # Facem CommunicationManager disponibil pentru
    # serverul web.

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
    # Web Server Thread
    # --------------------------------------------------------

    voice_server = threading.Thread(
        target=voice_server_thread,
        name="VoiceServerThread",
        daemon=True
    )


    # --------------------------------------------------------
    # Pornirea thread-urilor
    # --------------------------------------------------------

    communication.start()

    activity.start()

    voice_server.start()


    # --------------------------------------------------------
    # Așteptăm thread-urile
    # --------------------------------------------------------

    communication.join()

    activity.join()

    voice_server.join()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
