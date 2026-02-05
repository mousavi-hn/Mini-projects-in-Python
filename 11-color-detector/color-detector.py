import sys
from worker_thread import WorkerThread

from PySide6.QtCore import Qt, QThread, Slot
from PySide6.QtGui import QPixmap, QImage, QColor
from PySide6.QtWidgets import QWidget, QApplication, QSplitter, QPushButton, QLabel, QFileDialog, QVBoxLayout, \
    QHBoxLayout, QProgressBar


class ColorDetector(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Color Detector")
        self.showMaximized()

        self.detected_colors = []
        self.thread = None
        self.worker = None

        self.image = QImage()

        self.main_layout = QHBoxLayout(self)

        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Horizontal)

        self.image_display_part = QLabel()

        self.choose_image_button = QPushButton("Choose Image")
        self.choose_image_button.clicked.connect(self.choose_image)

        self.right_panel_layout = QVBoxLayout()
        self.right_panel_layout.addWidget(self.choose_image_button, alignment=Qt.AlignmentFlag.AlignTop)

        self.colors_widget = QWidget()
        self.colors_layout = QVBoxLayout()
        self.colors_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.colors_widget.setLayout(self.colors_layout)
        self.right_panel_layout.addWidget(self.colors_widget, alignment=Qt.AlignmentFlag.AlignTop)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setValue(0)
        self.right_panel_layout.addWidget(self.progress_bar, alignment=Qt.AlignmentFlag.AlignBottom)

        self.right_panel_widget = QWidget()
        self.right_panel_widget.setLayout(self.right_panel_layout)

        self.splitter.addWidget(self.image_display_part)
        self.splitter.addWidget(self.right_panel_widget)
        self.splitter.setSizes([1000, 200])

        self.main_layout.addWidget(self.splitter)

    def choose_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", filter="Image Files (*.jpg *.png *.bmp *.jpeg)")
        if file_path:
            self.image.load(file_path)
            self.image = self.image.convertToFormat(QImage.Format_RGB32)
            pixmap = QPixmap.fromImage(self.image)

            self.image_display_part.setPixmap(
                pixmap.scaled(self.image_display_part.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            self.clear_previous_results(self.colors_widget)
            self.find_colors()

    def find_colors(self):
        self.choose_image_button.setDisabled(True)
        self.detected_colors.clear()

        self.thread = QThread(self)
        self.worker = WorkerThread(self.image, self.progress_bar)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)

        self.worker.finished.connect(self.on_colors_ready)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    @Slot(list)
    def on_colors_ready(self, colors):
        self.detected_colors = colors
        self.show_colors_on_right_panel()
        self.choose_image_button.setDisabled(False)

    def show_colors_on_right_panel(self):
        self.clear_previous_results(self.colors_widget)

        description_label = QLabel("Most frequent colors in order:")
        self.colors_layout.addWidget(description_label, alignment=Qt.AlignmentFlag.AlignTop)

        for color in self.detected_colors:
            color_label = QLabel(color)
            self.colors_layout.addWidget(color_label, alignment=Qt.AlignmentFlag.AlignTop)

    def clear_previous_results(self, parent_widget):
        labels = parent_widget.findChildren(QLabel)
        for label in labels:
            label.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ColorDetector()
    window.show()
    sys.exit(app.exec())