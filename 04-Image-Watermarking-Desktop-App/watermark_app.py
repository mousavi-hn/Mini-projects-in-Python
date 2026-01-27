import sys
from PySide6.QtGui import QPixmap, QPainter, QFont
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QSplitter, QLabel, QFrame, QVBoxLayout, QPushButton, \
    QFileDialog, QMessageBox, QSlider, QLineEdit

class WatermarkApp(QWidget):
    def __init__(self):
        super().__init__()
        self.base_pixmap = None
        self.watermark_pixmap = None
        self.watermark_text = ""
        self.rendered_pixmap = None

        self.setWindowTitle("Watermarking Desktop")
        self.setFixedSize(1200, 600)

        main_layout = QHBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)

        self.image_display_part = QLabel()
        self.image_display_part.setAlignment(Qt.AlignCenter)
        self.image_display_part.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        control_panel = QWidget()
        control_panel_layout = QVBoxLayout(control_panel)

        load_image_button = QPushButton("Load Base Image")
        load_image_button.clicked.connect(self.load_main_image)

        image_opacity_slider = QSlider(Qt.Orientation.Horizontal)
        image_opacity_slider.setMinimum(0)
        image_opacity_slider.setMaximum(100)
        image_opacity_slider.setValue(50)
        self.current_image_opacity = image_opacity_slider.value()
        image_opacity_slider.valueChanged.connect(self.choose_image_opacity)

        text_opacity_slider = QSlider(Qt.Orientation.Horizontal)
        text_opacity_slider.setMinimum(0)
        text_opacity_slider.setMaximum(100)
        text_opacity_slider.setValue(50)
        self.current_text_opacity = text_opacity_slider.value()
        text_opacity_slider.valueChanged.connect(self.choose_text_opacity)

        self.text_watermark = QLineEdit()
        self.text_watermark.setPlaceholderText("Put the text watermark here!")

        load_watermark_text_button = QPushButton("Load Watermark Text")
        load_watermark_text_button.clicked.connect(self.load_watermark_text)

        load_watermark_image_button = QPushButton("Load Watermark Image")
        load_watermark_image_button.clicked.connect(self.load_watermark_image)

        save_image_button = QPushButton("Save Image")
        save_image_button.clicked.connect(self.save_image)

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear)

        control_panel_layout.addWidget(load_image_button)
        control_panel_layout.addSpacing(100)

        control_panel_layout.addWidget(load_watermark_image_button)
        control_panel_layout.addWidget(QLabel("Choose the image opacity: "))
        control_panel_layout.addWidget(image_opacity_slider)
        control_panel_layout.addSpacing(100)

        control_panel_layout.addWidget(self.text_watermark)
        control_panel_layout.addWidget(load_watermark_text_button)
        control_panel_layout.addWidget(QLabel("Choose the text opacity: "))
        control_panel_layout.addWidget(text_opacity_slider)
        control_panel_layout.addStretch()

        control_panel_layout.addWidget(save_image_button)
        control_panel_layout.addWidget(clear_button)

        splitter.addWidget(self.image_display_part)
        splitter.addWidget(control_panel)
        splitter.setSizes([800, 400])

        main_layout.addWidget(splitter)

    def load_main_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", filter="Image Files (*.jpg *.png *.bmp)")

        if file_path:
            self.base_pixmap = QPixmap(file_path)
            self.image_display_part.setPixmap(self.base_pixmap.scaled(self.image_display_part.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def load_watermark_image(self):
        watermark_image_file_path = ""

        if self.base_pixmap is not None and self.watermark_pixmap is None:
            watermark_image_file_path, _ = QFileDialog.getOpenFileName(self, "Open File", filter="Image Files (*.jpg *.png *.bmp)")

        if watermark_image_file_path != "":
            self.watermark_pixmap = QPixmap(watermark_image_file_path)

        if self.watermark_pixmap is not None:
            base_image = self.base_pixmap.copy()

            painter = QPainter(base_image)
            painter.setOpacity(self.current_image_opacity)

            x = base_image.width() - self.watermark_pixmap.width() - 20
            y = base_image.height() - self.watermark_pixmap.height() - 20

            painter.drawPixmap(x, y, self.watermark_pixmap)
            painter.end()

            self.rendered_pixmap = base_image.copy()

            self.image_display_part.clear()
            self.image_display_part.setPixmap(
                base_image.scaled(self.image_display_part.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        if self.base_pixmap is None:
            self.show_message_box("Error!", "Please choose a base image!")

    def load_watermark_text(self):
        if self.base_pixmap is not None:
            self.watermark_text = self.text_watermark.text()
            base_image = self.base_pixmap.copy()

            painter = QPainter(base_image)
            font = QFont("Arial", 40, QFont.Bold)
            painter.setFont(font)
            painter.setOpacity(self.current_text_opacity)

            painter.drawText(base_image.rect(), Qt.AlignCenter, self.watermark_text)
            painter.end()

            self.rendered_pixmap = base_image.copy()

            self.image_display_part.clear()
            self.image_display_part.setPixmap(
                base_image.scaled(self.image_display_part.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.show_message_box("Error!", "Please choose a base image!")

    def save_image(self):
        if self.base_pixmap is None:
            self.show_message_box("Error!", "Please choose a base image!")
            return

        if self.watermark_pixmap is None and self.watermark_text == "":
            self.show_message_box("Error!", "Please choose a watermark!")
            return

        if self.rendered_pixmap is None:
            self.show_message_box("Error!", "Nothing to save yet. Apply a watermark first.")
            return

        self.rendered_pixmap.save("rendered_image.png")
        self.show_message_box("Success!", "Image saved successfully!")



    def clear(self):
        self.image_display_part.clear()
        self.base_pixmap = None
        self.watermark_pixmap = None
        self.watermark_text = ""
        self.rendered_pixmap = None
        self.text_watermark.clear()

    def show_message_box(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()

    def choose_image_opacity(self, opacity):
        self.current_image_opacity = opacity / 100.0
        self.load_watermark_image()

    def choose_text_opacity(self, opacity):
        self.current_text_opacity = opacity / 100.0
        self.load_watermark_text()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WatermarkApp()
    window.show()
    sys.exit(app.exec())