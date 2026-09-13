import cv2

from bluetooth_camera import BluetoothCamera


ESP32_MAC = "20:9B:A9:73:9C:F2"


camera = BluetoothCamera(
    mac_address=ESP32_MAC,
    rfcomm_channel=1
)

try:
    for i in range(5):
        frame = camera.read()

        print(
            f"Frame {i + 1}: "
            f"{frame.shape[1]}x{frame.shape[0]}"
        )

        filename = f"bt_frame_{i + 1}.jpg"

        cv2.imwrite(filename, frame)

        print(f"Salvat: {filename}")

finally:
    camera.release()