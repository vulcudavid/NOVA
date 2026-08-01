import cv2
import numpy as np
from ai_edge_litert.interpreter import Interpreter


class EmotionDetector:

    EMOTION_LABELS = [
        "angry",
        "disgust",
        "fear",
        "happy",
        "sad",
        "surprise",
        "neutral"
    ]

    def __init__(self, model_path):
        self.model_path = model_path

        print("Emotion Detector initializat")
        print("Model:", self.model_path)

        self.interpreter = Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        print("Input details:", self.input_details)
        print("Output details:", self.output_details)

    def preprocess(self, face_image):
        gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)

        resized = cv2.resize(gray, (48, 48))

        normalized = resized.astype(np.float32) / 255.0

        input_data = np.expand_dims(normalized, axis=0)
        input_data = np.expand_dims(input_data, axis=-1)

        return input_data

    def interpret_emotion(self, predictions):

        scores = {
            label: float(predictions[index])
            for index, label in enumerate(self.EMOTION_LABELS)
        }

        emotion = max(scores, key=scores.get)
        confidence = scores[emotion]

        return emotion, confidence

    def predict(self, face_image):

        input_data = self.preprocess(face_image)

        input_index = self.input_details[0]["index"]
        output_index = self.output_details[0]["index"]

        self.interpreter.set_tensor(input_index, input_data)
        self.interpreter.invoke()

        predictions = self.interpreter.get_tensor(output_index)[0]
        print(predictions)

        emotion, confidence = self.interpret_emotion(predictions)

        return emotion, confidence, predictions