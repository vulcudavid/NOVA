import cv2

class FaceDetector:
    def __init__(self):
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.detector = cv2.CascadeClassifier(cascade_path)

        if self.detector.empty():
            raise Exception("Nu s-a putut incarca clasificatorul Haar Cascade pentru detectarea feței.")
        print("FaceDetector initializat")
        print("Fisier detectat: " + cascade_path)

    def detect(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8, minSize=(120,120))
        return faces
    
    def draw_faces(self, image, faces):
        output = image.copy()
        for (x, y, w, h) in faces:
            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 3)
        return output
    
    def crop_faces(self, image, faces):
        cropped_faces = []
        for (x, y, w, h) in faces:
            face = image[y:y+h, x:x+w]
            cropped_faces.append(face)
        return cropped_faces
    