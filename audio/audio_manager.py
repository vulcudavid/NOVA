import os
import subprocess
import sys
import tempfile
import wave


class AudioManager:

    def __init__(self, model_path):
        self.model_path = model_path
        self.audio_initialized = False

    def initialize_audio(self):
        """
        Initializează dispozitivul audio înainte de prima redare.
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

            subprocess.run(
                ["aplay", wav_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )

            self.audio_initialized = True

        finally:
            if os.path.exists(wav_path):
                os.remove(wav_path)

    def generate(self, text, output_path):

        if not text:
            raise ValueError("Textul TTS este gol")

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

        if not text:
            return

        self.initialize_audio()

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp_file:
            wav_path = temp_file.name

        try:
            self.generate(text, wav_path)
            subprocess.run(
                ["aplay", wav_path],
                check=True
            )

        finally:
            if os.path.exists(wav_path):
                os.remove(wav_path)