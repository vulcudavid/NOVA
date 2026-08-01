import cv2

from vision.face_detector import FaceDetector
from vision.emotion_detector import EmotionDetector


class VisionModule:

    def __init__(self, model_path):
        self.face_detector = FaceDetector()
        self.emotion_detector = EmotionDetector(model_path)

        print("VisionModule initializat.")

    def analyze_frame(self, frame):

        faces = self.face_detector.detect(frame)
        face_crops = self.face_detector.crop_faces(frame, faces)

        results = []

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

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                3
            )

            cv2.putText(
                frame,
                label,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 0),
                2
            )

        return results