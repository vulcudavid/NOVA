import threading
import queue
import time

from communication.comm_manager import ComunicationManager
from difficulty.difficulty_manager import DifficultyManager
from activity.ActivityManager import ActivityManager
from audio.audio_manager import AudioManager

# from vision.camera import Camera
# from vision.vision_module import VisionModule

# from ui.ui_manager import UIManager


# ============================================================
# COMMUNICATION THREAD
# ============================================================

def communication_thread(
    difficulty,
    activity_manager,
    audio_queue
):

    manager = ComunicationManager(
        difficulty,
        activity_manager,
        audio_queue
    )

    manager.run()


# ============================================================
# EMOTION THREAD
# ============================================================

def emotion_thread():

    # Camera is currently unavailable.
    # This thread will be enabled when the camera is available.

    pass


# ============================================================
# ACTIVITY THREAD
# ============================================================

def activity_thread(
    activity_manager,
    audio_queue
):

    while True:

        if activity_manager.is_timeout():

            message = activity_manager.get_message()

            print(message)

            audio_queue.put(message)

        time.sleep(1)


# ============================================================
# AUDIO THREAD
# ============================================================

def audio_thread(audio_queue):

    audio_manager = AudioManager(
        "./ro_RO-mihai-medium.onnx"
    )

    while True:

        text = audio_queue.get()

        try:

            audio_manager.speak(text)

        finally:

            audio_queue.task_done()


# ============================================================
# UI THREAD
# ============================================================

# UI-ul va conține:
#
# - meniul
# - navigarea
# - state machine
# - GameManager
# - jocurile
# - touchscreen / butoane
#
# Jocurile NU vor avea thread separat.
#
# def ui_thread():
#
#     ui_manager = UIManager()
#
#     while True:
#         ui_manager.update()


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # Shared objects
    # --------------------------------------------------------

    difficulty = DifficultyManager()

    activity_manager = ActivityManager()

    audio_queue = queue.Queue()


    # --------------------------------------------------------
    # Communication Thread
    # --------------------------------------------------------

    communication = threading.Thread(
        target=communication_thread,
        args=(
            difficulty,
            activity_manager,
            audio_queue
        ),
        name="CommunicationThread",
        daemon=True
    )


    # --------------------------------------------------------
    # Emotion Thread
    # --------------------------------------------------------

    emotion = threading.Thread(
        target=emotion_thread,
        name="EmotionThread",
        daemon=True
    )


    # --------------------------------------------------------
    # Activity Thread
    # --------------------------------------------------------

    activity = threading.Thread(
        target=activity_thread,
        args=(
            activity_manager,
            audio_queue
        ),
        name="ActivityThread",
        daemon=True
    )


    # --------------------------------------------------------
    # Audio Thread
    # --------------------------------------------------------

    audio = threading.Thread(
        target=audio_thread,
        args=(audio_queue,),
        name="AudioThread",
        daemon=True
    )


    # --------------------------------------------------------
    # UI Thread
    # --------------------------------------------------------

    # ui = threading.Thread(
    #     target=ui_thread,
    #     name="UIThread",
    #     daemon=True
    # )


    # --------------------------------------------------------
    # Pornirea thread-urilor
    # --------------------------------------------------------

    communication.start()
    # Camera momentan nu este disponibilă.
    # emotion.start()
    activity.start()
    audio.start()
    # ui.start()


    # --------------------------------------------------------
    # Așteptăm thread-urile active
    # --------------------------------------------------------

    communication.join()
    # emotion.join()
    activity.join()
    audio.join()
    # ui.join()


if __name__ == "__main__":
    main()