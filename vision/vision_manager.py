import threading
import time

from vision.bluetooth_camera import BluetoothCamera
from vision.vision_module import VisionModule


class VisionManager:

    def __init__(
        self,
        vision_module: VisionModule,
        difficulty_manager,
        mac_address: str,
        rfcomm_channel: int = 1,
        frame_interval: float = 0.2
    ):
        self.vision_module = vision_module
        self.difficulty_manager = difficulty_manager

        self.mac_address = mac_address
        self.rfcomm_channel = rfcomm_channel
        self.frame_interval = frame_interval

        self.camera = None
        self.thread = None
        self.capture_thread = None

        self.running = False
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.frame_condition = threading.Condition(self.lock)
        self.latest_frame = None

        self.current_emotion = "neutral"
        self.current_confidence = 0.0

    def start(self):

        with self.lock:

            if self.running:
                print("[VISION] VisionManager este deja activ.")
                return

            print("[VISION] Pornire VisionManager...")

            self.stop_event.clear()

            self.running = True

            self.thread = threading.Thread(
                target=self._vision_loop,
                name="VisionThread",
                daemon=True
            )

            self.capture_thread = threading.Thread(
                target=self._capture_loop,
                name="VisionCaptureThread",
                daemon=True
            )

            self.thread.start()
            self.capture_thread.start()

            print("[VISION] VisionManager pornit.")

    def stop(self):

        with self.lock:
            was_running = self.running
            self.running = False
            self.stop_event.set()
            camera = self.camera
            self.frame_condition.notify_all()

        if not was_running and self.thread is None and camera is None:
            return

        print("[VISION] Oprire VisionManager...")

        if camera is not None:
            camera.release()

        for thread in (self.capture_thread, self.thread):

            if thread is not None and thread is not threading.current_thread():
                thread.join(timeout=2.0)

        self.capture_thread = None
        self.thread = None

        with self.lock:
            self.camera = None
            self.latest_frame = None

        with self.lock:
            self.current_emotion = "neutral"
            self.current_confidence = 0.0

        print("[VISION] VisionManager oprit.")

    def _capture_loop(self):

        camera = None

        try:
            camera = BluetoothCamera(
                mac_address=self.mac_address,
                rfcomm_channel=self.rfcomm_channel,
                stop_event=self.stop_event
            )

            with self.lock:
                if self.stop_event.is_set():
                    camera.release()
                    return
                self.camera = camera

            while not self.stop_event.is_set():
                try:
                    frame = camera.read()
                except TimeoutError:
                    continue
                except ConnectionError:
                    if self.stop_event.is_set():
                        break
                    continue

                with self.frame_condition:
                    self.latest_frame = frame
                    self.frame_condition.notify()

        except Exception as error:
            if not self.stop_event.is_set():
                print(f"[VISION] Eroare la capturare: {error}")
        finally:
            if camera is not None:
                camera.release()

            with self.lock:
                if self.camera is camera:
                    self.camera = None
                if not self.stop_event.is_set():
                    self.running = False
                self.frame_condition.notify_all()

    def _vision_loop(self):

        print("[VISION] Thread pornit.")

        try:
            while not self.stop_event.is_set():

                with self.frame_condition:
                    self.frame_condition.wait_for(
                        lambda: (
                            self.latest_frame is not None
                            or self.stop_event.is_set()
                        ),
                        timeout=self.frame_interval
                    )

                    if self.stop_event.is_set():
                        break

                    frame = self.latest_frame
                    self.latest_frame = None

                if frame is None:
                    continue

                results = self.vision_module.analyze_frame(
                    frame
                )

                if results:

                    # Pentru moment folosim prima fata detectata.
                    face = results[0]

                    emotion = face["emotion"]
                    confidence = face["confidence"]

                    with self.lock:
                        self.current_emotion = emotion
                        self.current_confidence = confidence

                    if self.difficulty_manager is not None:

                        self.difficulty_manager.emotion_manager(
                            emotion,
                            confidence
                        )

                    print(
                        f"[VISION] emotion={emotion} "
                        f"confidence={confidence:.2f}"
                    )

                else:

                    with self.lock:
                        self.current_emotion = "neutral"
                        self.current_confidence = 0.0

                self.stop_event.wait(self.frame_interval)

        except Exception as error:

            print(
                f"[VISION] Eroare in vision loop: {error}"
            )

            with self.lock:
                self.running = False

        finally:

            with self.lock:
                self.running = False

            print("[VISION] Thread oprit.")

    def get_current_emotion(self):

        with self.lock:

            return {
                "emotion": self.current_emotion,
                "confidence": self.current_confidence
            }

    def is_running(self):

        with self.lock:
            return self.running