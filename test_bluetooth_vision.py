import cv2

from bluetooth_camera import BluetoothCamera
from vision.vision_module import VisionModule


ESP32_MAC = "20:9B:A9:73:9C:F2"
MODEL_PATH = "resources/models/custom_cnn_model.tflite"


camera = BluetoothCamera(
    mac_address=ESP32_MAC,
    rfcomm_channel=1
)

vision = VisionModule(MODEL_PATH)


try:
    for i in range(10):
        frame = camera.read()

        results = vision.analyze_frame(frame)

        print(f"\n[FRAME {i + 1}]")

        if not results:
            print("Nu a fost detectata nicio fata.")
            continue

        for result in results:
            print(
                f"Fata {result['index']}: "
                f"emotie={result['emotion']}, "
                f"confidence={result['confidence']:.2%}, "
                f"box={result['box']}"
            )

        output = f"vision_frame_{i + 1}.jpg"
        cv2.imwrite(output, frame)

        print(f"Salvat: {output}")

finally:
    camera.release()
