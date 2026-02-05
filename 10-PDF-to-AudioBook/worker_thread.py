import wave
from PySide6.QtCore import QObject
from PySide6.QtCore import QObject, Signal, Slot


class WorkerThread(QObject):
    def __init__(self, paragraphs, voice, config, progress_bar):
        super().__init__()
        self.paragraphs = paragraphs
        self.voice = voice
        self.config = config
        self.progress_bar = progress_bar
        self.finished = False

    @Slot()
    def run(self):
        with wave.open("audiobook.wav", "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.voice.config.sample_rate)

            for para in self.paragraphs:
                for audio_bytes in self.voice.synthesize(para, syn_config=self.config):
                    wav_file.writeframes(audio_bytes.audio_int16_bytes)
                self.progress_bar.setValue(self.progress_bar.value() + 1)
            self.finished = True