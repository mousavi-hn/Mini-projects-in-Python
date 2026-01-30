import sys
import requests

import os
import json

from records_dialog import RecordsDialog

from PySide6.QtGui import QFont, QAction
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSplitter, QTextEdit, QMessageBox, \
    QPushButton, QHBoxLayout, QInputDialog, QLineEdit, QMenuBar


class TypingSpeed(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Typing Speed Test")
        self.setFixedSize(1200, 800)

        self.layout = QVBoxLayout(self)
        splitter = QSplitter(Qt.Orientation.Vertical)

        self.text = ""
        font = QFont("Arial", 18)

        menu_bar = QMenuBar(self)
        file_menu = menu_bar.addMenu("&File")
        records_action = QAction("Records", self)
        records_action.triggered.connect(self.show_records_window)
        file_menu.addAction(records_action)
        self.layout.addWidget(menu_bar)

        self.sample_text_label = QLabel(self)
        self.sample_text_label.setText(self.text)
        self.sample_text_label.setWordWrap(True)
        self.sample_text_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.sample_text_label.setFont(font)

        self.input_text_field = QTextEdit(self)
        self.input_text_field.setPlaceholderText("Start typing here...")

        buttons_widget = QWidget()
        buttons_widget_layout = QHBoxLayout(buttons_widget)

        start_button = QPushButton("Start", buttons_widget)
        start_button.clicked.connect(self.start_session)

        stop_botton = QPushButton("Stop", buttons_widget)
        stop_botton.clicked.connect(self.stop_session)

        reset_button = QPushButton("Reset", buttons_widget)
        reset_button.clicked.connect(self.reset_session)

        self.milli_seconds_passed = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer_display)
        self.timer_label = QLabel(buttons_widget)

        buttons_widget_layout.addWidget(self.timer_label, Qt.AlignmentFlag.AlignLeft)
        buttons_widget_layout.addWidget(start_button, Qt.AlignmentFlag.AlignRight)
        buttons_widget_layout.addWidget(stop_botton, Qt.AlignmentFlag.AlignRight)
        buttons_widget_layout.addWidget(reset_button, Qt.AlignmentFlag.AlignRight)
        buttons_widget_layout.addStretch()

        splitter.addWidget(self.sample_text_label)
        splitter.addWidget(self.input_text_field)
        splitter.addWidget(buttons_widget)
        splitter.setStretchFactor(0, 100)
        splitter.setStretchFactor(1, 10)
        splitter.setStretchFactor(2, 1)

        self.layout.addWidget(splitter)

    def start_session(self):
        if self.timer.isActive():
            return

        self.text = self.get_random_text()
        self.sample_text_label.setText(self.text)
        self.input_text_field.clear()
        self.milli_seconds_passed = 0
        self.timer.start(10)

    def get_random_text(self):
        try:
            url = "http://metaphorpsum.com/paragraphs/2/4"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                return response.text
            else:
                self.pop_up_message("Error", "API is currently unavailable!")
        except Exception as e:
            self.pop_up_message("Error", f"Error connecting to the API!{e}")
        return "Fallback text. The API is unavailable right now."

    def update_timer_display(self):
        if not self.timer.isActive():
            return

        self.milli_seconds_passed += 10
        self.timer_label.setText(f"Time: {self.milli_seconds_passed/1000:.2f} s")

    def stop_session(self):
        self.timer.stop()
        speed = self.calculate_speed()

        reply = QMessageBox().question(self, "Save Record", "Do you want to save this record?",
                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                             QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return

        self.save_record(speed)

    def calculate_speed(self):
        sample_text_words = self.text.split()
        input_text_words = self.input_text_field.toPlainText().split()

        total_words_given = max(len(sample_text_words), 1)
        total_words_written = len(input_text_words)
        number_of_correct_words = 0

        for i in range(min(total_words_written, total_words_given)):
            if sample_text_words[i] == input_text_words[i]:
                number_of_correct_words += 1

        written_words_ratio = int(min(total_words_written / total_words_given * 100, 100))
        correct_words_ratio = int(number_of_correct_words / total_words_given * 100)
        time_taken = max(self.milli_seconds_passed, 1)
        speed = number_of_correct_words / time_taken * 1000 * 60

        self.pop_up_message("Statistics", f"Total words given: {total_words_given}"
                                          f"\n\nTotal words written: {total_words_written}"
                                          f"\nCorrect words: {number_of_correct_words}"
                                          f"\n\nWritten words ratio: {written_words_ratio}%"
                                          f"\nCorrect words ratio: {correct_words_ratio}%"
                                          f"\n\nTime taken: {time_taken/1000:.2f} s"
                                          f"\nSpeed: {speed:.2f} correct words/min")
        return speed

    def save_record(self, speed):
        file_path = "records.json"

        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = {}
        else:
            data = {}

        name, ok = QInputDialog.getText(self, "New Record!",
                                        "Enter your name:",
                                        QLineEdit.EchoMode.Normal)

        if ok and name:
            name = name.lower().strip().title()
            if name not in data or data[name] < speed :
                data[name] = speed

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def show_records_window(self):
        try:
            with open("records.json", "r") as file:
                data = json.load(file)
        except:
            data = {"No records yet": 0}

        dialog = RecordsDialog(data)
        dialog.exec()

    def reset_session(self):
        self.timer.stop()
        self.milli_seconds_passed = 0
        self.text = ""
        self.input_text_field.clear()
        self.timer_label.clear()
        self.sample_text_label.clear()

    def pop_up_message(self, caption, text):
        msg = QMessageBox()
        msg.setWindowTitle(caption)
        msg.setText(text)
        msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TypingSpeed()
    window.show()
    sys.exit(app.exec())