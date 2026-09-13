import os
import subprocess
import sys
import tempfile
import threading
import wave


class AudioManager:

    def __init__(self, model_path, device=None):
        self.model_path = model_path

        # ALSA device name for the USB-C -> jack DAC connected through the hub.
        # Can be overridden with the NOVA_AUDIO_DEVICE environment variable, e.g.:
        #   NOVA_AUDIO_DEVICE="plughw:CARD=Device,DEV=0"
        # Find the exact name by running: aplay -l  (look for the "USB Audio" card).
        self.device = device or os.getenv("NOVA_AUDIO_DEVICE", "default")

        self.audio_initialized = False

        # aplay can be called both from the LLM reply (chat background task)
        # and from the inactivity thread. This lock prevents two playbacks
        # from overlapping on the same speaker.
        self._playback_lock = threading.Lock()

    def _aplay(self, wav_path, suppress_output=False):
        command = ["aplay", "-D", self.device, wav_path]

        subprocess.run(
            command,
            stdout=subprocess.DEVNULL if suppress_output else None,
            stderr=subprocess.DEVNULL if suppress_output else None,
            check=True
        )

    def initialize_audio(self):
        """
        Initializes the audio device (USB DAC) before the first playback by
        playing a short burst of silence. Many USB sound cards clip the
        beginning of the first playback; this step avoids losing the first
        words of NOVA's first response.
        """

        if self.audio_initialized:
            return

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp_file:

            wav_path = temp_file.name

        try:
            sample_rate = 22050
            duration = 0.2
            num_samples = int(sample_rate * duration)

            silence = b"\x00\x00" * num_samples

            with wave.open(wav_path, "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(silence)

            self._aplay(wav_path, suppress_output=True)

            self.audio_initialized = True

        except Exception as error:
            print(f"[AUDIO] Could not initialize audio device "
                  f"({self.device}): {error}")

        finally:
            if os.path.exists(wav_path):
                os.remove(wav_path)

    def generate(self, text, output_path):

        if not text:
            raise ValueError("TTS text is empty")

        output_path = os.fspath(output_path)
        output_directory = os.path.dirname(output_path)
        if output_directory:
            os.makedirs(output_directory, exist_ok=True)

        subprocess.run(
            [
                sys.executable,
                "-m",
                "piper",
                "-m",
                self.model_path,
                "-f",
                output_path
            ],
            input=text,
            text=True,
            check=True
        )

        return output_path

    def speak(self, text):
        """
        Generates the response with Piper and plays it back on the speaker
        (through the USB DAC). Can be called both for LLM replies and for
        the inactivity reminder messages. Does not raise exceptions back to
        the calling thread, only logs them, because audio playback failing
        should not stop the rest of the application if the speaker is
        unavailable.
        """

        if not text:
            return

        with self._playback_lock:

            self.initialize_audio()

            with tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False
            ) as temp_file:
                wav_path = temp_file.name

            try:
                self.generate(text, wav_path)
                self._aplay(wav_path)

            except Exception as error:
                print(f"[AUDIO] Playback error ({self.device}): {error}")

            finally:
                if os.path.exists(wav_path):
                    os.remove(wav_path)