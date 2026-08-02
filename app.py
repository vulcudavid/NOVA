import cv2
from vision.camera import Camera
from vision.vision_module import VisionModule
from games.game_manager import GameManager


def main():

    manager = GameManager()

    manager.start()
    camera = Camera()
    vision = VisionModule("resources/models/custom_cnn_model.tflite")

    while True:

        frame = camera.read()

        if frame is None:
            break

        vision.analyze_frame(frame)

        cv2.imshow("NOVA - Emotion Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
