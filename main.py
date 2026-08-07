import threading
import cv2
import time

from communication.comm_manager import ComunicationManager
from difficulty.difficulty_manager import DifficultyManager
from activity.ActivityManager import ActivityManager
from vision.camera import Camera
from vision.vision_module import VisionModule

# from activity.activity_manager import ActivityManager
# from audio.audio_manager import AudioManager
# from ui.ui_manager import UIManager


# ============================================================
# COMMUNICATION THREAD
# ============================================================

def communication_thread(difficulty, activity_manager):

    manager = ComunicationManager(
        difficulty,
        activity_manager
    )

    manager.run()


# ============================================================
# EMOTION THREAD
# ============================================================

def emotion_thread():

    camera = Camera()

    vision = VisionModule(
        "resources/models/custom_cnn_model.tflite"
    )

    while True:

        frame = camera.read()

        if frame is None:
            break

        vision.analyze_frame(frame)

        # cv2.imshow(
        #     "NOVA - Emotion Recognition",
        #     frame
        # )

        # if cv2.waitKey(1) & 0xFF == ord("q"):
        #     break

    camera.release()
    # cv2.destroyAllWindows()


# ============================================================
# ACTIVITY THREAD
# ============================================================

def activity_thread(activity_manager):

    while True:

        if activity_manager.is_timeout():

            message = activity_manager.get_message()

            print(message)

        time.sleep(1)


# ============================================================
# AUDIO THREAD
# ============================================================

# Va fi implementat când introducem partea audio.
#
# def audio_thread():
#
#     audio_manager = AudioManager()
#
#     while True:
#         audio_manager.process()


# ============================================================
# UI THREAD
# ============================================================

# UI-ul va conține:
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

    difficulty = DifficultyManager()
    activity_manager = ActivityManager()   

    # --------------------------------------------------------
    # Communication Thread
    # --------------------------------------------------------

    communication = threading.Thread(
        target=communication_thread,
        args=(difficulty, activity_manager),
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
        args=(activity_manager,),
        name="ActivityThread",
        daemon=True
    )

    # --------------------------------------------------------
    # Audio Thread
    # --------------------------------------------------------

    # audio = threading.Thread(
    #     target=audio_thread,
    #     name="AudioThread",
    #     daemon=True
    # )

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
    # emotion.start() - camera lipsa
    activity.start()

    # --------------------------------------------------------
    # Așteptăm thread-urile active
    # --------------------------------------------------------

    communication.join()
    # emotion.join() - camera lipsa
    activity.join()

    # audio.join()
    # ui.join()


if __name__ == "__main__":
    main()