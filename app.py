import cv2

from vision.camera import Camera
from vision.vision_module import VisionModule


def main():

    camera = Camera()
    vision = VisionModule("resources/models/custom_cnn_model.tflite")

    while True:

        frame = camera.read()

        if frame is None:
            break

        results = vision.analyze_frame(frame)

        cv2.imshow("NOVA - Emotion Recognition", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()