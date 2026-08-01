import cv2

from vision.camera import Camera
from vision.face_detector import FaceDetector
from vision.emotion_detector import EmotionDetector


class VisionModule:
    def __init__(self, model_path):
        self.face_detector = FaceDetector()
        self.emotion_detector = EmotionDetector(model_path)

        print("VisionModule initializat.")

    def analyze_image(self, image_path):
        camera = Camera(image_path)

        image = camera.capture()

        if image is None:
            print("Nu s-a putut incarca imaginea.")
            return []

        faces = self.face_detector.detect(image)
        face_crops = self.face_detector.crop_faces(image, faces)

        results = []
        output = image.copy()

        for index, face in enumerate(face_crops):
            emotion, confidence, raw_predictions = self.emotion_detector.predict(face)

            x, y, w, h = faces[index]

            result = {
                "index": index,
                "box": [int(x), int(y), int(w), int(h)],
                "emotion": emotion,
                "confidence": float(confidence),
                "raw_predictions": raw_predictions.tolist()
            }

            results.append(result)

            label = f"{emotion} {confidence:.1%}"

            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 3)

            cv2.putText(
                output,
                label,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 0),
                2
            )

        cv2.imwrite("resources/images/result_emotions.jpg", output)

        return results