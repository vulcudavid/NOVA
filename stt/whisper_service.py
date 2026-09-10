import os
import subprocess
import tempfile
from pathlib import Path


class WhisperService:

    def __init__(self):
        self.executable = Path(
            os.getenv(
                "NOVA_WHISPER_EXECUTABLE",
                "/home/arduino/projects/whisper.cpp/build/bin/whisper-cli"
            )
        )
        self.model = Path(
            os.getenv(
                "NOVA_WHISPER_MODEL",
                "/home/arduino/projects/whisper.cpp/models/ggml-tiny.bin"
            )
        )
        self.language = os.getenv("NOVA_WHISPER_LANGUAGE", "ro")
        self.threads = os.getenv("NOVA_WHISPER_THREADS", "4")
        self.timeout = int(os.getenv("NOVA_WHISPER_TIMEOUT", "120"))

    def transcribe(self, wav_bytes):
        if not wav_bytes:
            raise ValueError("Fișierul WAV este gol")

        self._check_configuration()

        with tempfile.TemporaryDirectory(prefix="nova-stt-") as temp_dir:
            temp_path = Path(temp_dir)
            wav_path = temp_path / "input.wav"
            output_prefix = temp_path / "transcription"
            wav_path.write_bytes(wav_bytes)

            command = [
                str(self.executable),
                "-m", str(self.model),
                "-f", str(wav_path),
                "-l", self.language,
                "-t", self.threads,
                "-otxt",
                "-of", str(output_prefix),
                "-np",
                "-nt"
            ]

            try:
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    check=False
                )
            except subprocess.TimeoutExpired as error:
                raise RuntimeError("Transcrierea Whisper a depășit limita de timp") from error

            if result.returncode != 0:
                details = (result.stderr or result.stdout).strip()
                raise RuntimeError(
                    f"whisper.cpp a eșuat{': ' + details if details else ''}"
                )

            output_path = output_prefix.with_suffix(".txt")
            if not output_path.exists():
                raise RuntimeError("whisper.cpp nu a generat fișierul text")

            return output_path.read_text(encoding="utf-8").strip()

    def _check_configuration(self):
        if not self.executable.is_file():
            raise RuntimeError(f"Executabil Whisper lipsă: {self.executable}")

        if not self.model.is_file():
            raise RuntimeError(f"Model Whisper lipsă: {self.model}")
