import sys
import requests

from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QTimer, QElapsedTimer
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSplitter, QTextEdit, QMessageBox


class DisappearingText(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Disappearing Text")
        self.setFixedSize(1200, 800)

        self.layout = QVBoxLayout(self)
        splitter = QSplitter(Qt.Orientation.Vertical)

        self.text = ""
        font = QFont("Arial", 18)

        self.sample_text_label = QLabel(self)
        self.sample_text_label.setText(self.text)
        self.sample_text_label.setWordWrap(True)
        self.sample_text_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.sample_text_label.setFont(font)

        self.input_text_field = QTextEdit(self)
        self.input_text_field.setPlaceholderText("Start typing here...")

        splitter.addWidget(self.sample_text_label)
        splitter.addWidget(self.input_text_field)
        splitter.setStretchFactor(0, 100)
        splitter.setStretchFactor(1, 10)

        self.layout.addWidget(splitter)

        self.timer = QTimer()
        self.timer.timeout.connect(self.app_tick)

        self.elapse_timer = QElapsedTimer()
        self.input_text_field.textChanged.connect(lambda: self.elapse_timer.restart())

    def initialize_session(self):
        if not self.timer.isActive():
            self.timer.start(100)
            self.elapse_timer.start()

        self.elapse_timer.restart()

        self.text = self.get_random_text()
        self.sample_text_label.setText(self.text)
        self.input_text_field.clear()

    def app_tick(self):
        seconds_passed = self.elapse_timer.elapsed() / 1000.0

        if seconds_passed > 5 :
            self.input_text_field.clear()
            self.elapse_timer.restart()

        if self.is_similar(self.input_text_field.toPlainText(), self.text):
            self.initialize_session()

    def get_random_text(self):
        try:
            url = "http://metaphorpsum.com/paragraphs/1/1"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                return response.text
            else:
                self.pop_up_message("Error", "API is currently unavailable!")
        except Exception as e:
            self.pop_up_message("Error", f"Error connecting to the API!{e}")
        return "Fallback text. The API is unavailable right now."

    def is_similar(self, input_text, given_sample_text):
        input_text = input_text.lower()
        given_sample_text = given_sample_text.lower()

        input_text_list_of_words = input_text.split()
        given_sample_text_list_of_words = given_sample_text.split()

        number_of_matched_words = 0
        limit = min(len(input_text_list_of_words), len(given_sample_text_list_of_words))
        for i in range(limit):
            if input_text_list_of_words[i].strip() == given_sample_text_list_of_words[i].strip():
                number_of_matched_words += 1

        if (number_of_matched_words >= 0.7 * len(given_sample_text_list_of_words)
                and len(input_text_list_of_words) >= len(given_sample_text_list_of_words)):
            return True

        return False

    def pop_up_message(self, caption, text):
        msg = QMessageBox()
        msg.setWindowTitle(caption)
        msg.setText(text)
        msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DisappearingText()
    window.initialize_session()
    window.show()
    sys.exit(app.exec())