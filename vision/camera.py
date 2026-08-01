import cv2

class Camera:
    def __init__(self, image_path):
        self.image_path = image_path
        print("Camera initializata cu imaginea:", self.image_path)

    def capture(self):
        image = cv2.imread(self.image_path)

        if image is None:
            print("Eroare la citirea imaginii:", self.image_path)
            return None

        print("Imagine incarcata cu succes.")

        return image