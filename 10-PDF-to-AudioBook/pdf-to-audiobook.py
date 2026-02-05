import sys

import re

import pdfplumber
from PySide6.QtCore import Qt, QThread
from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, QSlider, QComboBox, QFileDialog, \
    QMessageBox, QProgressBar
from piper import SynthesisConfig

from piper.voice import PiperVoice
from worker_thread import WorkerThread


class PdfToAudioBook(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pdf to AudioBook")
        self.setFixedSize(400, 400)

        self.paragraphs = []
        self.model = "voices/amy/en_US-amy-medium.onnx"
        self.voice = PiperVoice.load(self.model)
        self.voice_speed = 10

        self.layout = QVBoxLayout(self)

        self.choose_pdf_button = QPushButton("Choose PDF")
        self.choose_pdf_button.clicked.connect(self.break_pdf_into_paragraphs)

        self.choose_voice_dropdown = QComboBox()
        self.choose_voice_dropdown.addItem("Amy")
        self.choose_voice_dropdown.addItem("Arctic")
        self.choose_voice_dropdown.addItem("Bryce")
        self.choose_voice_dropdown.addItem("Joe")
        self.choose_voice_dropdown.addItem("John")
        self.choose_voice_dropdown.addItem("Kathleen")
        self.choose_voice_dropdown.addItem("kristin")
        self.choose_voice_dropdown.addItem("Kusal")
        self.choose_voice_dropdown.currentIndexChanged.connect(self.choose_voice_model)

        self.voice_speed_slider = QSlider(Qt.Horizontal)
        self.voice_speed_slider.setMinimum(5)
        self.voice_speed_slider.setMaximum(20)
        self.voice_speed_slider.setValue(self.voice_speed)

        self.generate_audiobook_button = QPushButton("Generate Audiobook")
        self.generate_audiobook_button.clicked.connect(self.text_to_speech)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setValue(0)

        self.layout.addWidget(self.choose_pdf_button)
        self.layout.addWidget(self.choose_voice_dropdown)
        self.layout.addWidget(self.voice_speed_slider)
        self.layout.addWidget(self.generate_audiobook_button)
        self.layout.addWidget(self.progress_bar)


    def pdf_file_path(self):
        try:
            pdf_file_path = QFileDialog.getOpenFileName(None, "Select PDF", filter="(*.pdf)")[0]
            return pdf_file_path
        except Exception as e:
            self.pop_up_message("Error!", f"Couldn't load the file!!{e}")

    import re

    def extract_paragraphs_from_page(self, page) -> list[str]:
        text = page.extract_text(layout=True)
        if not text:
            return []

        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
        text = re.sub(r"\n(?!\s*\n)", " ", text)

        paras = re.split(r"\n\s*\n", text)
        paras = [re.sub(r"\s+", " ", p).strip() for p in paras]
        paras = [p for p in paras if len(p) > 0]

        return paras

    def break_pdf_into_paragraphs(self):
        self.progress_bar.setValue(0)
        pdf_file_path = self.pdf_file_path()
        paragraphs = []

        if not pdf_file_path:
            return

        with pdfplumber.open(pdf_file_path) as pdf:
            for page in pdf.pages:
                paragraphs.extend(self.extract_paragraphs_from_page(page))

        self.paragraphs = paragraphs
        self.progress_bar.setMaximum(len(self.paragraphs))

    def choose_voice_model(self):
        model_name = self.choose_voice_dropdown.currentText().lower()
        self.model = f"voices/{model_name}/en_US-{model_name}-medium.onnx"
        self.voice = PiperVoice.load(self.model)

    def text_to_speech(self):
        if (len(self.paragraphs)) == 0:
            self.pop_up_message("Error!", "Please choose a PDF!")
            return

        self.voice_speed = self.voice_speed_slider.value()
        config = SynthesisConfig(
            length_scale=10.0 / self.voice_speed,
            noise_scale=0.667,
            noise_w_scale=0.333
        )

        self.disable_buttons(True)
        self.pop_up_message("Starting...",
                            "Please be patient till the process is finished, it takes some time! "
                            "Press OK to start processing!")

        thread = QThread()
        worker = WorkerThread(self.paragraphs, self.voice, config, self.progress_bar)

        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        thread.start()
        while not worker.finished:
            thread.wait(1)
        thread.quit()
        thread.deleteLater()

        self.pop_up_message("Done!", "Conversion was finished successfully!")
        self.disable_buttons(False)

    def disable_buttons(self, boolean):
        self.choose_pdf_button.disabled = boolean
        self.choose_voice_dropdown.disabled = boolean
        self.voice_speed_slider.disabled = boolean
        self.generate_audiobook_button.disabled = boolean

    def pop_up_message(self, caption, text):
        msg = QMessageBox()
        msg.setWindowTitle(caption)
        msg.setText(text)
        msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PdfToAudioBook()

    window.show()
    sys.exit(app.exec())
