import socket
import struct
import time

import cv2
import numpy as np


class BluetoothCamera:

    MAX_IMAGE_SIZE = 2_000_000
    RECONNECT_DELAY = 3.0
    SOCKET_TIMEOUT = 2.0

    def __init__(self, mac_address, rfcomm_channel=1, stop_event=None):
        self.mac_address = mac_address
        self.rfcomm_channel = rfcomm_channel
        self.sock = None
        self.stop_event = stop_event

        self.connect()

    def connect(self):
        self.release()

        while not self._stopping():
            sock = None
            try:
                print(
                    f"[BT CAMERA] Incerc conectarea la "
                    f"{self.mac_address}..."
                )

                sock = socket.socket(
                    socket.AF_BLUETOOTH,
                    socket.SOCK_STREAM,
                    socket.BTPROTO_RFCOMM
                )

                sock.settimeout(self.SOCKET_TIMEOUT)

                sock.connect(
                    (self.mac_address, self.rfcomm_channel)
                )

                if self._stopping():
                    sock.close()
                    return

                self.sock = sock

                print(
                    "[BT CAMERA] Conectat la ESP32-CAM."
                )

                return

            except Exception as error:
                print(
                    f"[BT CAMERA] Conectarea a esuat: "
                    f"{error}"
                )

                try:
                    sock.close()
                except Exception:
                    pass

                if not self._stopping():
                    print(
                        f"[BT CAMERA] Reincerc in "
                        f"{self.RECONNECT_DELAY:.0f} secunde..."
                    )
                    self._wait(self.RECONNECT_DELAY)

        raise ConnectionError("Conexiunea Bluetooth a fost oprita.")

    def recv_exact(self, size):
        if self.sock is None:
            raise ConnectionError(
                "Nu exista conexiune Bluetooth."
            )

        data = bytearray()

        while len(data) < size:
            chunk = self.sock.recv(
                size - len(data)
            )

            if not chunk:
                raise ConnectionError(
                    "Conexiunea Bluetooth a fost inchisa."
                )

            data.extend(chunk)

        return bytes(data)

    def read(self):
        if self.sock is None:
            raise ConnectionError(
                "Camera Bluetooth nu este conectata."
            )

        try:
            # Primii 4 bytes contin dimensiunea JPEG-ului
            header = self.recv_exact(4)

            image_size = struct.unpack(
                "<I",
                header
            )[0]

            if (
                image_size <= 0
                or image_size > self.MAX_IMAGE_SIZE
            ):
                raise ValueError(
                    f"Dimensiune JPEG invalida: "
                    f"{image_size} bytes"
                )

            # Primim JPEG-ul complet in RAM
            image_data = self.recv_exact(
                image_size
            )

            # JPEG -> OpenCV image
            image_array = np.frombuffer(
                image_data,
                dtype=np.uint8
            )

            frame = cv2.imdecode(
                image_array,
                cv2.IMREAD_COLOR
            )

            if frame is None:
                raise RuntimeError(
                    "JPEG-ul primit nu a putut fi decodat."
                )

            return frame

        except socket.timeout as error:
            self.release()
            raise TimeoutError(
                "Timeout la receptionarea frame-ului Bluetooth."
            ) from error

        except (
            ConnectionError,
            OSError,
            ValueError,
            RuntimeError
        ) as error:

            print(
                f"[BT CAMERA] Eroare la receptionarea "
                f"frame-ului: {error}"
            )

            self.release()

            if self._stopping():
                raise ConnectionError(
                    "Conexiunea Bluetooth a fost oprita."
                ) from error

            self.connect()
            raise ConnectionError(
                "Conexiunea Bluetooth a fost resetata."
            ) from error

    def release(self):
        if self.sock is not None:
            try:
                self.sock.close()
            except Exception:
                pass

            self.sock = None

            print(
                "[BT CAMERA] Conexiunea Bluetooth "
                "a fost inchisa."
            )

    def _stopping(self):
        return (
            self.stop_event is not None
            and self.stop_event.is_set()
        )

    def _wait(self, seconds):
        if self.stop_event is None:
            time.sleep(seconds)
        else:
            self.stop_event.wait(seconds)