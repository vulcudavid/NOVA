import cv2

class Camera:

    def __init__(self, camera_index=0, width=640, height=480):
        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise RuntimeError("Camera nu a putut fi deschisă.")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        print("Camera initializata.")

    def read(self):
        success, frame = self.cap.read()

        if not success:
            print("Eroare la capturarea imaginii.")
            return None

        return frame

    def release(self):
        self.cap.release()